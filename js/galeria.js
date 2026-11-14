/* Galería con lightbox accesible: <dialog> nativo (Esc y foco atrapado), flechas del teclado,
   botones anterior/siguiente, clic fuera para cerrar y retorno del foco a la miniatura. */
(function () {
  'use strict';
  var dlg = document.getElementById('lightbox');
  if (!dlg || typeof dlg.showModal !== 'function') return; // sin soporte: las miniaturas siguen visibles
  var items = Array.prototype.slice.call(document.querySelectorAll('.gal-item'));
  var img = document.getElementById('lb-img');
  var cap = document.getElementById('lb-caption');
  var cnt = document.getElementById('lb-count');
  var idx = 0, opener = null;

  function show(i) {
    idx = (i + items.length) % items.length;
    var it = items[idx];
    var thumb = it.querySelector('img');
    img.src = it.getAttribute('data-full');
    img.alt = thumb ? thumb.alt : '';
    cap.textContent = it.getAttribute('data-caption') || '';
    cnt.textContent = 'Imagen ' + (idx + 1) + ' de ' + items.length;
  }

  items.forEach(function (it, i) {
    it.addEventListener('click', function () {
      opener = it;
      show(i);
      dlg.showModal();
      document.body.classList.add('no-scroll');
      dlg.querySelector('.lb-close').focus();
    });
  });

  dlg.querySelector('.lb-prev').addEventListener('click', function () { show(idx - 1); });
  dlg.querySelector('.lb-next').addEventListener('click', function () { show(idx + 1); });
  dlg.querySelector('.lb-close').addEventListener('click', function () { dlg.close(); });
  dlg.addEventListener('click', function (e) { if (e.target === dlg) dlg.close(); }); // clic en el fondo
  dlg.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowLeft') { e.preventDefault(); show(idx - 1); }
    if (e.key === 'ArrowRight') { e.preventDefault(); show(idx + 1); }
  });
  dlg.addEventListener('close', function () {
    document.body.classList.remove('no-scroll');
    if (opener) opener.focus();
  });
})();
