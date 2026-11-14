#!/usr/bin/env python3
"""Genera las páginas estáticas de la demo Refri House a partir de una plantilla común.
El resultado es HTML plano (sin build en el sitio publicado)."""
import json, html, urllib.parse, pathlib

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent  # raíz del repositorio = carpeta del sitio
PAGES = HERE / 'pages'
SITE = 'https://tu-dominio.com/demos/sitio-web-negocio/'  # cambia por el dominio real del portafolio
WA = '593900000000'
PRODUCTOS = json.loads((HERE / 'productos.json').read_text())
CATS = {
    'refrigeracion': 'Refrigeración', 'lavado': 'Lavado', 'coccion': 'Cocción',
    'aire': 'Aire acondicionado', 'pequenos': 'Microondas y pequeños',
}
STOCK = {'ok': ('stock--ok', 'En stock'), 'low': ('stock--low', 'Últimas unidades'), 'pedido': ('stock--order', 'Bajo pedido (3–5 días)')}

NAV = [('index.html', 'Inicio'), ('catalogo.html', 'Catálogo'), ('servicio-tecnico.html', 'Servicio técnico'),
       ('nosotros.html', 'Nosotros'), ('blog.html', 'Blog'), ('contacto.html', 'Contacto')]

e = html.escape

def wa(msg):
    return f'https://wa.me/{WA}?text=' + urllib.parse.quote(msg, safe='')

def card(p, lazy=False):
    cls, label = STOCK[p['stock']]
    search = f"{p['nombre']} {p['cod']} {CATS[p['cat']]} {p['compat']}".lower()
    msg = f"Hola Refri House, quiero cotizar: {p['nombre']} ({p['cod']})"
    return f'''          <article class="prod-card reveal" data-cat="{p['cat']}" data-precio="{p['precio']}" data-search="{e(search)}">
            <div class="prod-media">
              <span class="tag">{e(CATS[p['cat']])}</span>
              <svg aria-hidden="true"><use href="img/icons.svg#p-{p['icon']}"/></svg>
            </div>
            <div class="prod-body">
              <h3>{e(p['nombre'])}</h3>
              <span class="prod-code">Cód. {p['cod']}</span>
              <p class="prod-compat">{e(p['compat'])}</p>
              <span class="stock {cls}">{label}</span>
              <div class="prod-foot">
                <span class="price"><small>Desde</small>${p['precio']}</span>
                <a class="btn btn--primary btn--sm" href="{e(wa(msg))}" target="_blank" rel="noopener noreferrer" aria-label="Cotizar {e(p['nombre'])} por WhatsApp">Cotizar</a>
              </div>
            </div>
          </article>'''

STORE_LD = {
    "@context": "https://schema.org", "@type": "Store", "@id": SITE + "#negocio",
    "name": "Refri House",
    "description": "Tienda de repuestos de línea blanca y servicio técnico (negocio ficticio, sitio demo).",
    "url": SITE, "logo": SITE + "img/favicon.svg", "image": SITE + "img/og-refri-house.png",
    "telephone": "+593-4-000-0000", "priceRange": "$$", "currenciesAccepted": "USD",
    "paymentAccepted": "Efectivo, transferencia, tarjeta",
    "address": {"@type": "PostalAddress", "streetAddress": "Av. Ficticia 123 y Calle Demo",
                "addressLocality": "Guayaquil", "addressRegion": "Guayas", "addressCountry": "EC"},
    "openingHoursSpecification": [
        {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "08:30", "closes": "18:30"},
        {"@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "09:00", "closes": "14:00"}],
    "areaServed": "Ecuador"}

def ld(obj):
    return '<script type="application/ld+json">\n' + json.dumps(obj, ensure_ascii=False, indent=2) + '\n</script>'

def breadcrumb_ld(name, file):
    return ld({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Inicio", "item": SITE},
        {"@type": "ListItem", "position": 2, "name": name, "item": SITE + file}]})

def page(file, title, desc, body, extra_head='', scripts=(), frame_src='', crumb=None, noindex_extra=False):
    url = SITE + ('' if file == 'index.html' else file)
    csp = ("default-src 'self'; img-src 'self' data:; script-src 'self'; style-src 'self'; connect-src 'self'; "
           f"font-src 'self'; object-src 'none'; base-uri 'self'; form-action 'self';{(' frame-src ' + frame_src + ';') if frame_src else ''} upgrade-insecure-requests")
    nav = '\n'.join(
        f'          <li><a href="{f}"{" aria-current=\"page\"" if f == file else ""}>{t}</a></li>' for f, t in NAV)
    scr = '\n'.join(f'  <script src="js/{s}" defer></script>' for s in scripts)
    full_title = title if file == 'index.html' else f'{title} | Refri House'
    crumbs = ''
    if crumb:
        crumbs = f'''      <nav class="breadcrumb container" aria-label="Ruta de navegación">
        <ol><li><a href="index.html">Inicio</a></li><li aria-current="page">{e(crumb)}</li></ol>
      </nav>\n'''
        extra_head = breadcrumb_ld(crumb, file) + '\n' + extra_head
    return f'''<!DOCTYPE html>
<html lang="es" class="no-js">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta http-equiv="Content-Security-Policy" content="{csp}">
  <meta name="referrer" content="strict-origin-when-cross-origin">
  <title>{e(full_title)}</title>
  <meta name="description" content="{e(desc)}">
  <meta name="robots" content="noindex, nofollow">
  <link rel="canonical" href="{url}">
  <meta name="theme-color" content="#0B4F8A">
  <link rel="icon" href="img/favicon.svg" type="image/svg+xml">

  <meta property="og:type" content="website">
  <meta property="og:locale" content="es_EC">
  <meta property="og:site_name" content="Refri House (demo)">
  <meta property="og:title" content="{e(full_title)}">
  <meta property="og:description" content="{e(desc)}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{SITE}img/og-refri-house.png">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{e(full_title)}">
  <meta name="twitter:description" content="{e(desc)}">
  <meta name="twitter:image" content="{SITE}img/og-refri-house.png">

  <link rel="stylesheet" href="css/styles.css">
  <script src="js/theme.js"></script>
  <script src="js/main.js" defer></script>
{scr}
{ld(STORE_LD)}
{extra_head}
</head>
<body>
  <a class="skip-link" href="#contenido">Saltar al contenido</a>

  <p class="demo-bar"><strong>Sitio demo:</strong> Refri House es un negocio ficticio creado para mostrar el servicio de diseño de páginas web.</p>

  <header class="site-header">
    <div class="container header-inner">
      <a class="brand" href="index.html" aria-label="Refri House, ir al inicio">
        <svg aria-hidden="true"><use href="img/icons.svg#i-logo"/></svg>
        <span>Refri <b>House</b></span>
      </a>

      <nav class="nav" id="site-nav" aria-label="Principal">
        <ul>
{nav}
        </ul>
      </nav>

      <div class="header-actions">
        <button class="icon-btn theme-toggle" type="button" aria-label="Cambiar a modo oscuro" aria-pressed="false">
          <svg class="i-moon" aria-hidden="true"><use href="img/icons.svg#i-moon"/></svg>
          <svg class="i-sun" aria-hidden="true"><use href="img/icons.svg#i-sun"/></svg>
        </button>
        <a class="btn btn--accent btn--sm header-cta" href="catalogo.html">Buscar repuesto</a>
        <button class="icon-btn menu-toggle" type="button" aria-controls="site-nav" aria-expanded="false" aria-label="Abrir menú">
          <svg aria-hidden="true"><use href="img/icons.svg#i-menu"/></svg>
        </button>
      </div>
    </div>
  </header>

  <main id="contenido">
{crumbs}{body}
  </main>

  <footer class="site-footer">
    <div class="container footer-grid">
      <div>
        <a class="brand" href="index.html" aria-label="Refri House, ir al inicio">
          <svg aria-hidden="true"><use href="img/icons.svg#i-logo"/></svg>
          <span>Refri <b>House</b></span>
        </a>
        <p>Repuestos de línea blanca y servicio técnico en Guayaquil.</p>
        <div class="social">
          <a href="https://www.facebook.com/" target="_blank" rel="noopener noreferrer" aria-label="Facebook (enlace de ejemplo)"><svg aria-hidden="true"><use href="img/icons.svg#i-facebook"/></svg></a>
          <a href="https://www.instagram.com/" target="_blank" rel="noopener noreferrer" aria-label="Instagram (enlace de ejemplo)"><svg aria-hidden="true"><use href="img/icons.svg#i-instagram"/></svg></a>
          <a href="https://www.tiktok.com/" target="_blank" rel="noopener noreferrer" aria-label="TikTok (enlace de ejemplo)"><svg aria-hidden="true"><use href="img/icons.svg#i-tiktok"/></svg></a>
        </div>
      </div>
      <div>
        <h2>Tienda</h2>
        <ul>
          <li><a href="catalogo.html">Catálogo</a></li>
          <li><a href="servicio-tecnico.html">Servicio técnico</a></li>
          <li><a href="blog.html">Blog</a></li>
        </ul>
      </div>
      <div>
        <h2>Empresa</h2>
        <ul>
          <li><a href="nosotros.html">Nosotros</a></li>
          <li><a href="contacto.html">Contacto</a></li>
          <li><a href="contacto.html#privacidad">Aviso de privacidad</a></li>
        </ul>
      </div>
      <div>
        <h2>Visítanos</h2>
        <ul>
          <li>Av. Ficticia 123 y Calle Demo, Guayaquil</li>
          <li>Lun–Vie 08:30–18:30 · Sáb 09:00–14:00</li>
          <li><a href="tel:+59340000000">(04)&nbsp;000&#8209;0000</a></li>
        </ul>
      </div>
    </div>
    <div class="container footer-bottom">
      <span>© <span id="year">2026</span> Refri House. Todos los derechos reservados.</span>
      <span class="demo-note">Sitio demo — negocio ficticio</span>
    </div>
  </footer>

  <a class="wa-float" href="{e(wa('Hola Refri House, necesito ayuda con un repuesto.'))}" target="_blank" rel="noopener noreferrer">
    <svg aria-hidden="true"><use href="img/icons.svg#i-whatsapp"/></svg>
    <span>¿Te ayudamos?</span><span class="sr-only"> Escríbenos por WhatsApp</span>
  </a>
</body>
</html>
'''

def read(name):
    p = PAGES / name
    return p.read_text() if p.exists() else ''

def build():
    out = {}
    dest = '\n'.join(card(p) for p in PRODUCTOS if p.get('dest'))
    out['index.html'] = page('index.html', 'Refri House | Repuestos de línea blanca en Guayaquil',
        'Repuestos para refrigeradoras, lavadoras, cocinas y aires acondicionados en Guayaquil. Garantía de 90 días, asesoría técnica gratis y envíos a todo Ecuador. Sitio demo.',
        read('index.body.html').replace('{{DESTACADOS}}', dest), extra_head=read('index.ld.html'))

    if (PAGES / 'catalogo.body.html').exists():
        todos = '\n'.join(card(p) for p in PRODUCTOS)
        chips = '\n'.join(
            f'            <button type="button" class="chip" data-cat="{k}" aria-pressed="false">{v} <span class="chip-n">{sum(1 for p in PRODUCTOS if p["cat"] == k)}</span></button>'
            for k, v in CATS.items())
        itemlist = ld({"@context": "https://schema.org", "@type": "ItemList", "name": "Catálogo de repuestos Refri House",
            "numberOfItems": len(PRODUCTOS), "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "item": {
                    "@type": "Product", "name": p['nombre'], "sku": p['cod'], "category": CATS[p['cat']],
                    "description": p['compat'], "image": SITE + "img/og-refri-house.png",
                    "offers": {"@type": "Offer", "priceCurrency": "USD", "price": p['precio'],
                               "availability": "https://schema.org/" + ("PreOrder" if p['stock'] == 'pedido' else "InStock"),
                               "seller": {"@id": SITE + "#negocio"}}}}
                for i, p in enumerate(PRODUCTOS)]})
        out['catalogo.html'] = page('catalogo.html', 'Catálogo de repuestos',
            'Catálogo de repuestos para refrigeradoras, lavadoras, cocinas, aires acondicionados y microondas: precios referenciales, código y compatibilidad. Sitio demo.',
            read('catalogo.body.html').replace('{{PRODUCTOS}}', todos).replace('{{CHIPS}}', chips).replace('{{TOTAL}}', str(len(PRODUCTOS))),
            extra_head=itemlist, scripts=['catalogo.js'], crumb='Catálogo')

    if (PAGES / 'servicio-tecnico.body.html').exists():
        out['servicio-tecnico.html'] = page('servicio-tecnico.html', 'Servicio técnico a domicilio',
            'Servicio técnico a domicilio en Guayaquil: mantenimiento e instalación de aire acondicionado, reparación de refrigeradoras, lavadoras y cocinas. Agenda en línea. Sitio demo.',
            read('servicio-tecnico.body.html'), extra_head=read('servicio-tecnico.ld.html'), crumb='Servicio técnico')

    for extra in ['nosotros', 'blog', 'contacto', '404']:
        cfg = json.loads(read(extra + '.json') or 'null')
        if cfg:
            out[extra + '.html'] = page(extra + '.html', cfg['title'], cfg['desc'], read(extra + '.body.html'),
                extra_head=read(extra + '.ld.html'), scripts=cfg.get('scripts', []), frame_src=cfg.get('frame_src', ''),
                crumb=cfg.get('crumb'))
    # 404: rutas absolutas para que funcione desde cualquier URL inexistente
    if '404.html' in out:
        import re
        base = '/demos/sitio-web-negocio/'
        c = out['404.html']
        c = re.sub(r'(href|src|action)="(?!https?:|#|tel:|mailto:|/)([^"]+)"', lambda m: f'{m.group(1)}="{base}{m.group(2)}"', c)
        c = re.sub(r'  <link rel="canonical"[^\n]*\n', '', c)
        out['404.html'] = c
    for name, content in out.items():
        (ROOT / name).write_text(content)
        print('ok', name, len(content))

if __name__ == '__main__':
    build()
