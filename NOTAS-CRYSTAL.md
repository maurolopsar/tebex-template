# Plantilla Tebex — Crystal Network (notas para continuar)

Base: tema "Siro" de Ipolotech (ver `README.txt`; hay que mantener su crédito, ya está en el pie). Rediseñada por completo con el estilo de `crystal_web` (`app/globals.css`).

## Estructura
- `layout.html`: configuración arriba (IP, Discord, menús, textos, footer), cabecera sticky, tarjetas de servidor/Discord, menú lateral de categorías (se genera solo desde Tebex), módulos, footer con marca de agua. Las páginas rellenan `{% block content %}`; `checkout.html` quita el menú lateral con `{% block sidebar %}`.
- `index / category / checkout / options / username / orderstatus / complete / cms-page / instructions` y `module.*.html`: contenido de cada página. Las categorías y paquetes salen de lo que crees en el panel de Tebex; no hay nada fijo.
- `style.css`: se pega en Webstore > Design > Appearance > **Theme**.
- Los includes y hooks propios de Tebex (`data-remote`, `.toggle-modal`, `/templates/209/js/*`, `checkout/buttons.html`…) se mantienen igual que en el original.

## Cambios respecto al tema original
- Eliminado el script externo `diplt.js` de Ipolotech, la API key de Rust y su ID de Google Analytics (el tema original enviaba estadísticas a su cuenta). Solo se usa el `googleAnalytics` de tu tienda.
- Contadores de jugadores: `api.mcsrvstat.us` (Minecraft) y el widget de Discord (hay que activarlo en Ajustes del servidor de Discord y poner `widget_id`).

## Preview local
`python preview/build.py --serve` → http://localhost:8000/ (ver `preview/README.md`).

## Pendiente
- Probar en una tienda Tebex real (la preview usa Bootstrap 3 como aproximación del tema Flat).
- Rellenar los textos/enlaces de `layout.html` con los datos reales y subir el logo desde el panel de Tebex.
- No se pudo leer https://docs.tebex.io desde el entorno (bloqueado): comprobar contra la documentación oficial que no falte ninguna variable.
