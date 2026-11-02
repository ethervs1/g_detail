# Estado del proyecto: sitio web SR Detailing Garage

**Última actualización:** 2 de noviembre de 2026
**Sitio publicado:** https://ethervs1.github.io/g_detail/
**Repositorio:** https://github.com/ethervs1/g_detail (público)

## Resumen

Primera versión del sitio **publicada y funcionando**. Es una landing de una sola página para SR Detailing Garage, un taller de estética y mecánica automotriz en San Joaquín, Santiago. Parte del diseño generado con Google Stitch, reescrito en HTML, CSS y JavaScript puro, con fotos reales del taller.

| Área | Estado |
|---|---|
| Diseño y maquetación (escritorio y móvil) | ✅ Listo |
| Fotos del taller (patentes tapadas, optimizadas) | ✅ Listo |
| Funciones interactivas | ✅ Listo y probado |
| Publicación en GitHub Pages | ✅ En línea |
| Contenido y datos del negocio | ⚠️ Pendiente de validar con el taller |
| Dominio propio | ⏳ No definido |
| Analítica | ⏳ No implementada |

## Qué tiene el sitio

1. **Header fijo:** logo circular (estilo foto de perfil de Instagram), menú y botón a WhatsApp. En móvil, el menú se abre con el botón ☰.
2. **Inicio:** título de marca, texto de presentación, botones a WhatsApp y a servicios, cifras destacadas y foto del taller.
3. **Pilares:** calidad, confianza, profesionales y ubicación.
4. **Servicios y precios:** 6 servicios con un desplegable **"Qué incluye +"** y botón para cotizar cada uno por WhatsApp. Al final, una franja de "También hacemos".
5. **Trabajos realizados:** galería de 15 fotos reales, 4 visibles y el resto en **"Ver más trabajos +"**. Cada foto se amplía al tocarla. Incluye una tarjeta hacia Instagram.
6. **Reseñas:** botones para ver y dejar reseñas en Google.
7. **Preguntas frecuentes:** 4 preguntas desplegables.
8. **Contacto:** dirección, horario, WhatsApp, mapa de Google y cotizador que arma el mensaje y abre WhatsApp.
9. **Footer** y **botón flotante de WhatsApp**.

### Precios publicados

| Servicio | Precio |
|---|---|
| Lavado de tapiz | Desde $80.000 |
| Estética y pulido (sellado cerámico) | Desde $150.000 |
| Mantención automotriz | Desde $110.000 ⚠️ |
| Mecánica y encendido | A cotizar |
| Frenos y suspensión | A cotizar |
| Pintura de calipers | Desde $60.000 |

## Pendientes

### Por confirmar con el taller

- [ ] **Usuario de Instagram.** El sitio usa `sr_detailing.garage`, que es el que aparece en las capturas. El banner dice `@sr.detailing_garage` y el diseño de Stitch usaba `sr_detailing_garage`.
- [ ] **Enlace a la ficha de Google** para los botones de reseñas. Hoy es una búsqueda genérica (en Google Maps: ficha del taller → "Compartir").
- [ ] **Precio de la mantención:** $110.000 o $120.000 (aparecen ambos en Instagram).
- [ ] **Dirección** (Arquitecto Brunelleschi #3509) y **horario** (lunes a domingo, con reserva).
- [ ] **Precio del sellado cerámico** ($150.000) y lista de servicios de "Estética y pulido", que vienen del diseño de Stitch.
- [ ] **Cifra "+500 autos atendidos"** del inicio: es un dato de ejemplo del prototipo.
- [ ] **Modelos de algunos autos** en los textos alternativos de las fotos (el Peugeot y el Chery se identificaron a ojo).
- [ ] Revisar en el navegador que el **mapa** marque el lugar correcto.

### Mejoras posibles

- [ ] **Reseñas destacadas:** copiar 3 a 6 reseñas reales de Google al sitio. En `index.html` hay una plantilla comentada en la sección de reseñas.
- [ ] **Dominio propio** (por ejemplo `srdetailing.cl`, en NIC Chile). Al conectarlo hay que actualizar en `index.html` las URLs de `og:url`, `og:image` y del bloque JSON-LD, que hoy apuntan a `ethervs1.github.io/g_detail/`.
- [ ] **Analítica de visitas** (GoatCounter, Cloudflare Web Analytics o GA4).
- [ ] **Fotos de antes y después:** son las que más venden un servicio de detailing.

## Estructura del repositorio

```
index.html                  Página completa (contenido y precios se editan aquí)
css/styles.css              Estilos; paleta de colores como variables al inicio
js/main.js                  Menú móvil, foto ampliada, cotizador → WhatsApp
tools/optimizar_fotos.py    Script para procesar fotos nuevas
assets/images/trabajos/     Fotos de trabajos en WebP (1200 px y 640 px) + manifest.json
assets/images/logos/        Logo, banner y favicons
assets/g_stitch/            Diseño original de Google Stitch (solo referencia)
assets/paleta_colores.png   Paleta de marca
.nojekyll                   Indica a GitHub Pages que no procese el sitio con Jekyll
```

No fuera del repo (en `.gitignore`): `assets/baseIG/`, capturas de Instagram usadas como referencia de contenido, que contienen patentes y personas.

## Cómo mantener el sitio

### Ver cambios en local
Abrir `index.html` directamente en el navegador. Para simular un celular en Chrome: `Cmd + Opción + I` y luego `Cmd + Shift + M`.

### Publicar
Cada `git push` a `main` actualiza el sitio en uno o dos minutos. El estado del despliegue se ve en la pestaña **Actions** del repositorio.

### Cambiar un precio o un texto
Editar `index.html`. Si es un precio, revisar también las opciones del cotizador (`<select id="service">`), que repiten los precios.

### Agregar fotos de trabajos
1. Procesar la foto (requiere Pillow: `pip install pillow`):
   ```bash
   python tools/optimizar_fotos.py foto.jpg --nombre toyota-hilux-pulido --tapar x1,y1,x2,y2
   ```
   `--tapar` recibe las coordenadas de la patente en píxeles de la foto original. **Revisar siempre el resultado antes del push:** el repo es público.
2. Copiar un bloque `<li>` de la galería en `index.html` y cambiar el nombre, las medidas (están en `manifest.json`), el texto alternativo y la etiqueta.
3. Las fotos horizontales llevan la clase `shot--wide` y ocupan dos columnas. Para que no queden filas incompletas, cada lista de la galería debe sumar un múltiplo de 3 casillas (las anchas cuentan como 2).

## Detalles técnicos

- **Sin frameworks ni compilación:** HTML, CSS y JavaScript puro. Las rutas son relativas, así que funciona igual en GitHub Pages y en un dominio propio.
- **Fuentes:** Rajdhani (títulos) y Chivo (texto), desde Google Fonts. Los íconos van dentro del HTML como SVG, estilo Lucide.
- **Imágenes:** WebP en dos tamaños con `srcset` y carga diferida. La galería descarga unos 1,1 MB en total.
- **SEO local:** título y descripción, vista previa para compartir (Open Graph) y datos estructurados `AutoRepair` (schema.org).
- **Accesibilidad:** navegable con teclado, enlace "Saltar al contenido", textos alternativos en las fotos y respeto por la opción de "reducir movimiento".
- **Sin backend:** el cotizador no guarda datos, solo arma un mensaje y abre WhatsApp al número +56 9 4570 0131.

## Historial

| Fecha | Cambio |
|---|---|
| 2026-11-02 | Análisis del diseño de Google Stitch y definición del alcance |
| 2026-11-02 | Patentes tapadas en las fotos; optimización a WebP y nombres descriptivos |
| 2026-11-02 | Primera versión del sitio; repo público y publicación en GitHub Pages |
