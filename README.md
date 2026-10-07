# Dashboard Ejecutivo — Pacientes de Subrogación (Fertilidad Integral)

Sitio estático: un solo `index.html`, sin librerías externas. Corte de datos: 30-sep-2026.

**Privacidad:** no contiene nombres completos ni datos de contacto. La sección «Revisión de pacientes — Grupos 2 y 3» muestra Nº de historia e iniciales. Se recomienda un repo **privado** (Pages privado requiere plan Pro/Team/Enterprise); si es público, cualquiera con el link verá las cifras.

## Publicar en GitHub Pages
1. Crea el repo `fertilidad-subrogacion-dashboard`.
2. Sube `index.html`, `.nojekyll` y este README.
3. Settings → Pages → Deploy from a branch → `main` / root.

## Exclusiones de pacientes (Grupos 2 y 3)
Las marcas de «Excluir» se guardan en el navegador de quien las hace. Para aplicarlas de forma permanente, usa «Exportar exclusiones (CSV)» y envíalo a Revenue Management para incorporarlo al Excel y a la siguiente versión del tablero.

## Actualizar
Cada actualización reemplaza el bloque `const D=...` incrustado en `index.html` (datos agregados generados desde el pipeline de Excel).
