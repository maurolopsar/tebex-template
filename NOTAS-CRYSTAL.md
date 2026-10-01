# Adaptación Crystal Network (notas para continuar)

Base: tema "Siro" de Ipolotech (ver README.txt; mantener su copyright). Los cambios no tocan la estructura HTML ni las variables Twig de Tebex.

## Hecho
- `style.css`: bloque "CRYSTAL NETWORK" añadido al final (sobrescribe el original). Paleta/tarjetas/botones/fondo vórtice tomados de `crystal_web` (`app/globals.css`).
- `layout.html`: `dark_mode='yes'`, partículas desactivadas, fuente Inter, `<div class="bg-glow">`, JS protegido cuando el switch de tema está desactivado.

## Preview local
Ver `preview/README.md` (`python preview/build.py --serve`).

## Pendiente
- Revisar visualmente cada página (index, category, checkout, options, username, orderstatus, complete, módulos) en una tienda Tebex real.
- Rellenar textos/enlaces de la zona de configuración de `layout.html` (nombre, IP, Discord, menús, footer).
- Subir el logo desde el panel de Tebex (Webstore > Design) para `store.logo`.

## Instalación (resumen)
Pegar los .html en Webstore > Design > Appearance > Template (tema Flat) y `style.css` en Appearance > Theme.
