// SR Detailing Garage: menú móvil, sección activa, galería y cotizador por WhatsApp.
(function () {
  "use strict";

  var WHATSAPP = "56945700131";

  // Menú móvil
  var nav = document.getElementById("nav");
  var toggle = document.getElementById("nav-toggle");

  function setMenu(open) {
    nav.classList.toggle("is-open", open);
    toggle.setAttribute("aria-expanded", String(open));
    toggle.setAttribute("aria-label", open ? "Cerrar menú" : "Abrir menú");
  }

  toggle.addEventListener("click", function () {
    setMenu(toggle.getAttribute("aria-expanded") !== "true");
  });
  nav.addEventListener("click", function (e) {
    if (e.target.closest("a")) setMenu(false);
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && nav.classList.contains("is-open")) {
      setMenu(false);
      toggle.focus();
    }
  });

  // Marca en el menú la sección visible
  var links = nav.querySelectorAll('a[href^="#"]');
  if ("IntersectionObserver" in window) {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        links.forEach(function (link) {
          if (link.getAttribute("href") === "#" + entry.target.id) {
            link.setAttribute("aria-current", "true");
          } else {
            link.removeAttribute("aria-current");
          }
        });
      });
    }, { rootMargin: "-45% 0px -50% 0px" });
    links.forEach(function (link) {
      var section = document.querySelector(link.getAttribute("href"));
      if (section) observer.observe(section);
    });
  }

  // Galería: abre la foto grande en un diálogo (sin JS, el enlace abre la imagen directamente)
  var lightbox = document.getElementById("lightbox");
  if (lightbox && typeof lightbox.showModal === "function") {
    var lightboxImg = lightbox.querySelector("img");

    document.addEventListener("click", function (e) {
      var shot = e.target.closest(".shot");
      if (!shot) return;
      e.preventDefault();
      var thumb = shot.querySelector("img");
      lightboxImg.src = shot.getAttribute("href");
      lightboxImg.alt = thumb ? thumb.alt : "";
      lightbox.showModal();
    });

    lightbox.querySelector(".lightbox__close").addEventListener("click", function () {
      lightbox.close();
    });
    // Cerrar al tocar fuera de la foto
    lightbox.addEventListener("click", function (e) {
      if (e.target === lightbox) lightbox.close();
    });
    lightbox.addEventListener("close", function () {
      lightboxImg.removeAttribute("src");
    });
  }

  // Cotizador: arma el mensaje y abre WhatsApp
  var form = document.getElementById("quote-form");
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var data = new FormData(form);
    var notes = String(data.get("comentarios") || "").trim();

    var message =
      "¡Hola SR Detailing Garage! Quiero cotizar:\n\n" +
      "🚘 Vehículo: " + String(data.get("modelo")).trim() + " (" + data.get("anio") + ")\n" +
      "⚙️ Servicio: " + data.get("servicio") + "\n" +
      (notes ? "📝 Comentarios: " + notes + "\n" : "") +
      "\n¿Me podrían indicar precio y disponibilidad?";

    window.open("https://wa.me/" + WHATSAPP + "?text=" + encodeURIComponent(message), "_blank", "noopener");
  });

  var year = document.getElementById("year");
  if (year) year.textContent = new Date().getFullYear();
})();
