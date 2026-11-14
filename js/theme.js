/* Se carga en <head> para aplicar el tema guardado antes del primer pintado (evita parpadeo). */
(function () {
  var root = document.documentElement;
  root.classList.remove('no-js');
  try {
    var saved = localStorage.getItem('rh-theme');
    if (saved === 'light' || saved === 'dark') root.setAttribute('data-theme', saved);
  } catch (e) { /* almacenamiento no disponible */ }
})();
