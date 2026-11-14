/* Catálogo: búsqueda, filtro por categoría y orden sobre tarjetas ya renderizadas en el HTML.
   Sin JS, el catálogo completo sigue visible. Nunca se inserta HTML con datos del usuario (solo textContent). */
(function () {
  'use strict';

  var grid = document.getElementById('prod-grid');
  if (!grid) return;
  var cards = Array.prototype.slice.call(grid.querySelectorAll('.prod-card'));
  var original = cards.slice();
  var input = document.getElementById('q');
  var form = document.getElementById('cat-search');
  var select = document.getElementById('orden');
  var chips = Array.prototype.slice.call(document.querySelectorAll('.chip'));
  var count = document.getElementById('result-count');
  var empty = document.getElementById('empty');
  var emptyWa = document.getElementById('empty-wa');

  var CAT_NAMES = {
    refrigeracion: 'Refrigeración', lavado: 'Lavado', coccion: 'Cocción',
    aire: 'Aire acondicionado', pequenos: 'Microondas y pequeños'
  };

  // Normaliza: minúsculas y sin tildes, para que "desague" encuentre "desagüe".
  function norm(s) {
    return String(s || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').trim();
  }

  var params = new URLSearchParams(window.location.search);
  var state = {
    q: (params.get('q') || '').slice(0, 60),
    cat: CAT_NAMES[params.get('cat')] ? params.get('cat') : '',
    orden: 'relevancia'
  };

  function syncUrl() {
    var p = new URLSearchParams();
    if (state.q) p.set('q', state.q);
    if (state.cat) p.set('cat', state.cat);
    var qs = p.toString();
    history.replaceState(null, '', qs ? '?' + qs : window.location.pathname);
  }

  function apply() {
    var terms = norm(state.q).split(/\s+/).filter(Boolean);
    var visible = [];
    original.forEach(function (c) {
      var okCat = !state.cat || c.getAttribute('data-cat') === state.cat;
      var hay = norm(c.getAttribute('data-search'));
      var okQ = terms.every(function (t) { return hay.indexOf(t) !== -1; });
      var show = okCat && okQ;
      c.hidden = !show;
      if (show) visible.push(c);
    });

    var sorted = visible.slice();
    if (state.orden === 'precio-asc') sorted.sort(function (a, b) { return a.dataset.precio - b.dataset.precio; });
    if (state.orden === 'precio-desc') sorted.sort(function (a, b) { return b.dataset.precio - a.dataset.precio; });
    if (state.orden === 'nombre') sorted.sort(function (a, b) {
      return a.querySelector('h3').textContent.localeCompare(b.querySelector('h3').textContent, 'es');
    });
    if (state.orden === 'relevancia') sorted = original.filter(function (c) { return !c.hidden; });
    sorted.forEach(function (c) { grid.appendChild(c); });

    chips.forEach(function (ch) { ch.setAttribute('aria-pressed', String(ch.getAttribute('data-cat') === state.cat)); });

    var n = visible.length;
    var txt = 'Mostrando ' + n + (n === 1 ? ' repuesto' : ' repuestos');
    if (state.cat) txt += ' en ' + CAT_NAMES[state.cat];
    if (state.q) txt += ' para “' + state.q + '”';
    count.textContent = txt; // textContent: el término del usuario nunca se interpreta como HTML

    empty.hidden = n !== 0;
    if (n === 0 && emptyWa && window.RH) {
      emptyWa.href = window.RH.waLink('Hola Refri House, busco este repuesto: ' + (state.q || '(sin nombre)') + '. ¿Lo tienen?');
    }
    syncUrl();
  }

  input.value = state.q;
  var t;
  input.addEventListener('input', function () {
    clearTimeout(t);
    t = setTimeout(function () { state.q = input.value.slice(0, 60); apply(); }, 150);
  });
  form.addEventListener('submit', function (e) { e.preventDefault(); state.q = input.value.slice(0, 60); apply(); });
  select.addEventListener('change', function () { state.orden = select.value; apply(); });
  chips.forEach(function (ch) {
    ch.addEventListener('click', function () { state.cat = ch.getAttribute('data-cat'); apply(); });
  });

  // Las tarjetas del catálogo se muestran sin animación de entrada para que los filtros respondan al instante.
  original.forEach(function (c) { c.classList.remove('reveal'); });

  apply();
})();
