# Demo: Sitio web de negocio — Refri House

Sitio completo para **Refri House**, una tienda **ficticia** de repuestos de línea blanca y servicio técnico en Guayaquil. Forma parte del portafolio de Carlos Romero y sirve para mostrar el servicio **"Diseño de páginas web"**, junto con las demos de citas/facturación e inventario/POS.

- **Ruta en el portafolio:** `public/demos/sitio-web-negocio/` → `/demos/sitio-web-negocio/`
- **Tecnología:** HTML5 + CSS + JavaScript vanilla. No necesita build ni dependencias para publicarse.
- **Fecha:** noviembre de 2026

## Estructura del repositorio

```
index.html, catalogo.html, servicio-tecnico.html, nosotros.html,
blog.html, contacto.html, 404.html, robots.txt, sitemap.xml
css/styles.css
js/        theme.js, main.js, catalogo.js, galeria.js, contacto.js
img/       ícono, sprite de íconos, ilustraciones, galería, avatares, imagen OG y capturas WebP
fuente/    plantilla para regenerar las páginas (build.py, pages/, productos.json)
docs/      ficha del proyecto (ES/EN), capturas y reporte Lighthouse
```

## Vista previa local

```bash
python3 -m http.server 8000
# abrir http://localhost:8000/
```

## Páginas y funciones

| Página | Qué incluye |
|---|---|
| Inicio | Hero con buscador, 5 categorías, 4 productos más pedidos, beneficios, cifras animadas, pasos de compra, marcas compatibles (solo texto), testimonios rotulados como ficticios, FAQ y llamado final |
| Catálogo | 24 repuestos con búsqueda sin tildes, filtros por categoría (`?cat=`), búsqueda por URL (`?q=`), orden por precio o nombre y botón "Cotizar" con mensaje de WhatsApp prellenado. Sin JavaScript, el catálogo completo sigue visible |
| Servicio técnico | 6 servicios con precio y duración; "Agendar" enlaza a `/demos/citas-facturacion/?servicio=…` |
| Nosotros | Historia, valores, equipo con avatares ilustrados y galería con lightbox (`<dialog>`, flechas del teclado, Esc, retorno de foco) |
| Blog | 3 artículos cortos con datos estructurados `BlogPosting` |
| Contacto | Formulario validado, datos de contacto, mapa bajo demanda y aviso de privacidad de ejemplo |
| 404 | Página personalizada con buscador; usa rutas absolutas para funcionar desde cualquier URL |

Todas las páginas comparten: barra "Sitio demo", header sticky, menú móvil accesible, modo oscuro (sigue al sistema y tiene un botón), WhatsApp flotante y footer con "Sitio demo — negocio ficticio".

## Resultados de calidad

### Lighthouse 12 (Chrome headless, servidor local)

| Página | Rendimiento | Accesibilidad | Buenas prácticas | SEO* |
|---|---|---|---|---|
| Inicio | 100 | 100 | 100 | 66 |
| Catálogo | 100 | 100 | 100 | 63 |
| Servicio técnico | 100 | 100 | 100 | 63 |
| Nosotros | 100 | 100 | 100 | 66 |
| Blog | 99 | 100 | 100 | 63 |
| Contacto | 100 | 100 | 100 | 63 |
| 404 | 100 | 100 | 100 | 63 |

Medido en móvil. En escritorio salió 100 / 100 / 100 en las tres primeras categorías para todas las páginas.

**\*SEO:** la demo lleva `<meta name="robots" content="noindex, nofollow">` **a propósito**, para no competir con el portafolio en Google. Por eso Lighthouse marca la única falla de SEO ("la página no se puede indexar"). Con una copia sin `noindex`, **el SEO da 100** en Inicio, Catálogo y Contacto. Es el puntaje que tendría el sitio de un cliente real.

Las sugerencias de caché, compresión y minificado salen porque se midió con un servidor local simple. Vercel aplica compresión y caché automáticamente.

### Otras verificaciones
- **HTML válido** en las 7 páginas (`html-validate`, reglas recomendadas).
- **Sin errores en consola** en 360, 768, 1280 y 1920 px, en modo claro y oscuro.
- **Sin enlaces internos rotos.** El enlace a `../citas-facturacion/` apunta a la otra demo.
- **Pruebas automáticas (Playwright):**
  - filtros y búsqueda del catálogo; código HTML en la búsqueda se muestra como texto;
  - lightbox: apertura, flechas, Esc y retorno de foco;
  - formulario: errores, éxito, honeypot y límite de envíos;
  - mapa bajo demanda y menú móvil con Esc.
- **Contraste AA** verificado; el verde de WhatsApp se oscureció a `#0F7A41` (5,4:1).

## Seguridad en la demo
- **CSP por meta tag:** solo recursos propios, sin scripts ni estilos en línea, `object-src 'none'` y `frame-src` solo para OpenStreetMap en Contacto.
- Todo dato del usuario se inserta con `textContent`; nunca con `innerHTML`.
- El formulario **no envía ni guarda datos**: valida y muestra un mensaje de éxito que lo explica.
- **Anti-spam de muestra:** campo honeypot oculto, tiempo mínimo de 3 s y límite de 3 envíos por sesión (`sessionStorage`).
- Enlaces externos con `rel="noopener noreferrer"`.
- No hay claves, analítica ni scripts de terceros.
- El mapa solo se carga si el visitante lo pide.
- Ilustraciones 100 % propias en SVG. No se usan fotos de personas ni logos de marcas; las marcas compatibles aparecen solo en texto, con aviso de no afiliación.

## Diferencias con la versión de producción

| Tema | Demo | Producción (cliente real) |
|---|---|---|
| Framework | HTML estático | Next.js (App Router) en Vercel |
| Formulario | Solo valida en el navegador | Server Action o API route con validación en el servidor (Zod), envío por **Resend** y **Cloudflare Turnstile**; claves en variables de entorno de Vercel |
| Anti-spam | Honeypot, tiempo mínimo y límite en `sessionStorage` | Lo mismo, más Turnstile y límite por IP en el servidor (por ejemplo, Upstash Ratelimit) |
| Cabeceras | CSP por meta tag | Cabeceras en `next.config`: CSP (con `frame-ancestors`), HSTS, X-Content-Type-Options, Referrer-Policy y Permissions-Policy |
| Contenido | Escrito en el HTML (generado con `fuente/build.py`) | **Payload CMS**: el cliente edita repuestos, precios, stock, servicios, blog y testimonios reales con permiso |
| Catálogo | 24 productos de ejemplo | Sincronizado con el inventario real (por ejemplo, la demo de Inventario + POS) |
| Indexación | `noindex` | `index`, sitemap enviado a Google Search Console y perfil de Google Business |
| Privacidad | Aviso de ejemplo | Política de privacidad redactada según la **LOPDP Ecuador**, con registro de consentimientos |
| Analítica | Ninguna | Analítica sin cookies (Vercel Analytics o Plausible), o banner de consentimiento |
| Dominio | Subruta del portafolio | Dominio propio con HTTPS |
| Imágenes | SVG ilustrados | Fotos reales del negocio en WebP/AVIF con `next/image` |

## Cómo publicarlo en el portafolio
1. Copia los archivos del sitio (todo excepto `fuente/` y `docs/`) a `public/demos/sitio-web-negocio/` del proyecto Next.js.
2. Reemplaza `https://tu-dominio.com` por el dominio real. Puedes cambiar `SITE` en `fuente/build.py` y ejecutar `python3 fuente/build.py`, o buscar y reemplazar en los `.html`.
3. Opcional, pero recomendado: agrega en `next.config` la cabecera `X-Robots-Tag: noindex` para `/demos/:path*`, y `Disallow: /demos/` en el `robots` del portafolio.
4. Next.js sirve `public/` como archivos estáticos. Para la 404 personalizada de la demo, puedes agregar en `next.config` un rewrite de `/demos/sitio-web-negocio/:path*` que no exista hacia `404.html`. Si no lo haces, se mostrará la 404 del portafolio.
5. Importa `docs/ficha-sitio-web-negocio.json` en la colección de proyectos o servicios.

## Cómo editar el contenido (`fuente/`)
- `productos.json`: repuestos del catálogo (los marcados con `"dest": true` aparecen en el Inicio).
- `pages/*.body.html`: contenido de cada página. `pages/*.json`: título y descripción SEO.
- `build.py`: genera las páginas con header, footer, SEO y JSON-LD comunes. Ejecuta `python3 fuente/build.py` desde la raíz del repositorio (Python 3.8+, sin dependencias). Las páginas se regeneran en la raíz.

## Datos ficticios a reemplazar si se reutiliza para un cliente
Número de WhatsApp `593900000000`, teléfono `(04) 000-0000`, correo `hola@refrihouse.example`, dirección "Av. Ficticia 123", redes sociales, personas del equipo, testimonios y precios.
