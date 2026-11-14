/* Formulario de contacto (DEMO): valida en el cliente y muestra éxito, pero NO envía ni guarda datos.
   Técnicas mostradas: validación accesible, teléfono ecuatoriano, honeypot, tiempo mínimo de llenado,
   límite de envíos por sesión y salida segura con textContent. */
(function () {
  'use strict';

  var form = document.getElementById('contact-form');
  if (!form) return;
  var btn = document.getElementById('enviar');
  var errBox = document.getElementById('form-errors');
  var errList = document.getElementById('form-errors-list');
  var ok = document.getElementById('form-success');
  var okText = document.getElementById('success-text');
  var okTitle = document.getElementById('success-title');
  var msg = document.getElementById('mensaje');
  var msgCount = document.getElementById('mensaje-count');
  var MAX_ENVIOS = 3;
  var KEY = 'rh-demo-envios';
  var startedAt = Date.now();

  btn.disabled = false; // con JS activo el formulario funciona

  function envios() {
    try { return parseInt(sessionStorage.getItem(KEY) || '0', 10) || 0; } catch (e) { return 0; }
  }
  function sumarEnvio() {
    try { sessionStorage.setItem(KEY, String(envios() + 1)); } catch (e) {}
  }

  // Normaliza teléfonos: quita espacios/guiones y convierte +593 / 593 al formato local con 0.
  function normTel(v) {
    var t = String(v).replace(/[\s\-().]/g, '');
    if (/^\+?593/.test(t)) t = '0' + t.replace(/^\+?593/, '');
    return t;
  }

  var rules = {
    nombre: function (v) {
      v = v.trim();
      if (!v) return 'Escribe tu nombre.';
      if (v.length < 3) return 'El nombre debe tener al menos 3 caracteres.';
      if (!/^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ' .-]+$/.test(v)) return 'Usa solo letras y espacios.';
      return '';
    },
    telefono: function (v) {
      var t = normTel(v);
      if (!t) return 'Escribe un teléfono de contacto.';
      // Celular: 09 + 8 dígitos. Fijo: 0 + código de provincia (2–7) + 7 dígitos.
      if (!/^09\d{8}$/.test(t) && !/^0[2-7]\d{7}$/.test(t)) return 'Usa un celular (09XXXXXXXX) o un fijo con código de provincia (04XXXXXXX).';
      return '';
    },
    correo: function (v) {
      v = v.trim();
      if (!v) return 'Escribe tu correo electrónico.';
      if (!/^[^\s@]+@[^\s@]+\.[A-Za-z]{2,}$/.test(v)) return 'Revisa el formato del correo (ej.: tu@correo.com).';
      return '';
    },
    motivo: function (v) { return v ? '' : 'Selecciona el motivo de tu mensaje.'; },
    mensaje: function (v) {
      v = v.trim();
      if (!v) return 'Escribe tu mensaje.';
      if (v.length < 10) return 'Cuéntanos un poco más (mínimo 10 caracteres).';
      return '';
    },
    consentimiento: function (_, el) { return el.checked ? '' : 'Debes aceptar el aviso de privacidad para continuar.'; }
  };

  var labels = { nombre: 'Nombre', telefono: 'Teléfono', correo: 'Correo', motivo: 'Motivo', mensaje: 'Mensaje', consentimiento: 'Aviso de privacidad' };

  function check(name) {
    var el = form.elements[name];
    var err = rules[name](el.value, el);
    var out = document.getElementById(name + '-err');
    out.textContent = err;
    el.setAttribute('aria-invalid', err ? 'true' : 'false');
    el.closest('.field').classList.toggle('has-error', !!err);
    return err;
  }

  // Valida al salir del campo y, si ya tenía error, mientras se corrige.
  Object.keys(rules).forEach(function (name) {
    var el = form.elements[name];
    var evt = (el.type === 'checkbox' || el.tagName === 'SELECT') ? 'change' : 'blur';
    el.addEventListener(evt, function () { check(name); });
    el.addEventListener('input', function () { if (el.getAttribute('aria-invalid') === 'true') check(name); });
  });

  msg.addEventListener('input', function () { msgCount.textContent = msg.value.length + ' / 600'; });

  function showSuccess(title, text) {
    form.hidden = true;
    errBox.hidden = true;
    okTitle.textContent = title;
    okText.textContent = text; // textContent: nada de lo que escribe el usuario se interpreta como HTML
    ok.hidden = false;
    ok.focus();
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();

    // Límite de envíos por sesión
    if (envios() >= MAX_ENVIOS) {
      errList.textContent = '';
      var li = document.createElement('li');
      li.textContent = 'Alcanzaste el límite de ' + MAX_ENVIOS + ' mensajes en esta sesión. Si necesitas algo más, escríbenos por WhatsApp.';
      errList.appendChild(li);
      errBox.hidden = false;
      errBox.focus();
      return;
    }

    // Honeypot o envío demasiado rápido (menos de 3 s): se simula éxito sin procesar nada.
    var esBot = form.elements.empresa.value !== '' || (Date.now() - startedAt) < 3000;

    var errores = [];
    Object.keys(rules).forEach(function (name) {
      var err = check(name);
      if (err) errores.push({ name: name, err: err });
    });

    if (errores.length) {
      errList.textContent = '';
      errores.forEach(function (x) {
        var li = document.createElement('li');
        var a = document.createElement('a');
        a.href = '#' + x.name;
        a.textContent = labels[x.name] + ': ' + x.err;
        a.addEventListener('click', function (ev) { ev.preventDefault(); form.elements[x.name].focus(); });
        li.appendChild(a);
        errList.appendChild(li);
      });
      errBox.hidden = false;
      errBox.focus();
      return;
    }

    errBox.hidden = true;
    if (esBot) {
      showSuccess('Mensaje recibido', 'Gracias por escribirnos.');
      return;
    }

    sumarEnvio();
    var nombre = form.elements.nombre.value.trim().split(/\s+/)[0];
    var restantes = MAX_ENVIOS - envios();
    showSuccess('¡Gracias, ' + nombre + '!',
      'Tu mensaje pasó todas las validaciones. Como este es un sitio demo, no se envió ni se guardó ningún dato. ' +
      'En la versión real, el mensaje llegaría al correo del negocio y te responderíamos en menos de 24 horas. ' +
      '(Envíos de prueba restantes en esta sesión: ' + restantes + ').');
  });

  document.getElementById('otro-mensaje').addEventListener('click', function () {
    form.reset();
    msgCount.textContent = '0 / 600';
    Object.keys(rules).forEach(function (n) {
      form.elements[n].removeAttribute('aria-invalid');
      form.elements[n].closest('.field').classList.remove('has-error');
      document.getElementById(n + '-err').textContent = '';
    });
    startedAt = Date.now();
    ok.hidden = true;
    form.hidden = false;
    form.elements.nombre.focus();
  });

  /* ---------- Mapa bajo demanda ---------- */
  var mapBtn = document.getElementById('load-map');
  if (mapBtn) {
    mapBtn.addEventListener('click', function () {
      var f = document.createElement('iframe');
      f.src = 'https://www.openstreetmap.org/export/embed.html?bbox=-79.9200%2C-2.1800%2C-79.8900%2C-2.1550&layer=mapnik&marker=-2.1675%2C-79.9050';
      f.title = 'Mapa de ubicación referencial en Guayaquil';
      f.loading = 'lazy';
      f.referrerPolicy = 'no-referrer';
      f.width = '600';
      f.height = '320';
      var holder = document.getElementById('map');
      holder.textContent = '';
      holder.appendChild(f);
    });
  }
})();
