# Preview local (sin tienda Tebex)

Renderiza las plantillas con Jinja2 (casi idéntico a Twig) y datos de mentira.

    pip install jinja2
    python preview/build.py --serve     # abre http://localhost:8000/  (menú de páginas en /_index.html)

Genera `preview/out/*.html` (uno por plantilla). Cada vez que cambies un `.html` o `style.css`, vuelve a ejecutar el comando.

Limitaciones: el CSS/JS base de Tebex (tema Flat) no está disponible, así que se usa Bootstrap 3 por CDN como aproximación. Los includes propios de Tebex (checkout/buttons, package_options…) salen vacíos. Verifica el resultado final en una tienda real.
