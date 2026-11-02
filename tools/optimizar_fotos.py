#!/usr/bin/env python3
"""Optimiza fotos para el sitio: genera WebP en dos tamaños y actualiza manifest.json.

Requisito: Pillow (pip install pillow).

Uso:
    python tools/optimizar_fotos.py FOTO [FOTO ...] [--nombre NOMBRE] [--tapar x1,y1,x2,y2 ...]

Ejemplos:
    # El nombre de salida sale del nombre del archivo (en minúsculas y con guiones)
    python tools/optimizar_fotos.py ~/Descargas/toyota-hilux-pulido.jpg

    # Nombre explícito y patente tapada (coordenadas en píxeles de la foto original)
    python tools/optimizar_fotos.py "WhatsApp Image.jpeg" --nombre toyota-hilux-pulido \\
        --tapar 455,1190,762,1292

Por cada foto se generan, en assets/images/trabajos/:
    NOMBRE.webp     hasta 1200 px de ancho (vista ampliada)
    NOMBRE-sm.webp  640 px de ancho (galería / móvil)

Revisa siempre el resultado de --tapar antes de hacer commit: el repo es público.
"""
import argparse
import json
import re
import unicodedata
from pathlib import Path

from PIL import Image, ImageFilter, ImageOps

DESTINO = Path(__file__).resolve().parent.parent / "assets" / "images" / "trabajos"
LARGE_W = 1200
SMALL_W = 640
QUALITY = 80
QUALITY_SM = 72
# Tapado de patentes: pixelado grueso + desenfoque, para que no quede legible
TAPAR_MARGEN = 6
TAPAR_BLOQUE = 30
TAPAR_BLUR = 18


def slug(texto):
    texto = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", texto.lower()).strip("-")


def parse_caja(valor):
    try:
        x1, y1, x2, y2 = (int(v) for v in valor.split(","))
    except ValueError:
        raise argparse.ArgumentTypeError(f"caja inválida '{valor}', usa x1,y1,x2,y2")
    if x2 <= x1 or y2 <= y1:
        raise argparse.ArgumentTypeError(f"caja inválida '{valor}', x2/y2 deben ser mayores que x1/y1")
    return x1, y1, x2, y2


def tapar(im, caja):
    x1, y1, x2, y2 = caja
    caja = (max(0, x1 - TAPAR_MARGEN), max(0, y1 - TAPAR_MARGEN),
            min(im.width, x2 + TAPAR_MARGEN), min(im.height, y2 + TAPAR_MARGEN))
    zona = im.crop(caja)
    w, h = zona.size
    zona = zona.resize((max(1, w // TAPAR_BLOQUE), max(1, h // TAPAR_BLOQUE)), Image.BILINEAR)
    zona = zona.resize((w, h), Image.NEAREST).filter(ImageFilter.GaussianBlur(TAPAR_BLUR))
    im.paste(zona, caja)


def ajustar(im, ancho):
    if im.width <= ancho:
        return im
    return im.resize((ancho, round(im.height * ancho / im.width)), Image.LANCZOS)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("fotos", nargs="+", type=Path)
    parser.add_argument("--nombre", help="nombre de salida (solo si se procesa una foto)")
    parser.add_argument("--tapar", nargs="+", type=parse_caja, default=[], metavar="x1,y1,x2,y2",
                        help="zonas a tapar (solo si se procesa una foto)")
    args = parser.parse_args()
    if len(args.fotos) > 1 and (args.nombre or args.tapar):
        parser.error("--nombre y --tapar se usan con una sola foto a la vez")

    DESTINO.mkdir(parents=True, exist_ok=True)
    ruta_manifest = DESTINO / "manifest.json"
    manifest = json.loads(ruta_manifest.read_text()) if ruta_manifest.exists() else {}

    for foto in args.fotos:
        nombre = slug(args.nombre or foto.stem)
        im = ImageOps.exif_transpose(Image.open(foto)).convert("RGB")
        for caja in args.tapar:
            tapar(im, caja)
        grande = ajustar(im, LARGE_W)
        chica = ajustar(grande, SMALL_W)
        grande.save(DESTINO / f"{nombre}.webp", "WEBP", quality=QUALITY, method=6)
        chica.save(DESTINO / f"{nombre}-sm.webp", "WEBP", quality=QUALITY_SM, method=6)
        manifest[nombre] = {"w": grande.width, "h": grande.height, "sm_w": chica.width, "sm_h": chica.height}
        print(f"{foto.name} -> {nombre}.webp ({grande.width}x{grande.height}), {nombre}-sm.webp")

    ruta_manifest.write_text(json.dumps(dict(sorted(manifest.items())), indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
