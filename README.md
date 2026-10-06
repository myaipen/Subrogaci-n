# Dashboard Ejecutivo — Pacientes de Subrogación (Fertilidad Integral)

Sitio estático (un solo `index.html`, sin librerías externas). Contiene **solo cifras agregadas**: sin nombres, historias clínicas ni contacto de pacientes.

## Publicar en GitHub Pages
1. Crea el repo `fertilidad-subrogacion-dashboard` (recomendado: **privado**, con Pages restringido a la organización; si es público, cualquiera con el link verá las cifras).
2. Sube `index.html` y `.nojekyll`.
3. Settings → Pages → Deploy from a branch → `main` / root.
4. URL: `https://myaipen.github.io/fertilidad-subrogacion-dashboard/`

## Actualizar
`build_data.py` es el script de referencia que genera el bloque de datos a partir del pipeline de Excel (corte 30-sep-2026). Cada actualización reemplaza el JSON incrustado en `const D=...` dentro de `index.html`.
