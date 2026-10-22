## Why

Los estilos solo se pueden ver como texto (`make_style.py decode`) o escuchándolos en REAPER, de uno en uno. No hay forma de ver de un vistazo los 31 estilos ni sus 9 patrones, y por eso pasan desapercibidos patrones vacíos (el p8 de cuatro estilos), patrones casi idénticos dentro de un estilo o estilos que se copian entre sí. Una página de "huellas" visual, publicada en GitHub Pages, permite revisarlos sin REAPER y enseñarlos a quien llegue al repo.

## What Changes

- Nueva herramienta `tools/view_styles.py` que lee `drum_styles_v/*.txt` y genera `docs/fingerprints.html`: una página autocontenida (sin dependencias ni CDN, datos incrustados) con todos los estilos.
- Cada estilo se muestra como una tira de 9 mapas de calor (p0–p8, 7 voces × 32 pasos, color según el valor 0–255). Un p8 vacío se marca.
- Los estilos se agrupan por familia según la tabla "Included styles" del README; los que no aparecen van a "Other".
- Un slider global de Density atenúa los pasos que no sonarían con ese valor (`256 − v < Density`, la misma regla del plugin).
- Al hacer clic en una tira se amplía ese estilo.
- `docs/fingerprints.html` se versiona porque GitHub Pages lo sirve desde `main /docs`. `tools/check_styles.py` comprueba además que está al día con los estilos.
- README: cómo regenerar la página y enlace a la página publicada.
- Sin cambios en el plugin ni en los estilos. Sin audio ni pad XY.

## Capabilities

### New Capabilities
- `style-fingerprints`: la página de huellas, su generación y la comprobación de que está al día.

### Modified Capabilities

## Impact

- Archivos nuevos: `tools/view_styles.py`, `docs/fingerprints.html`.
- `tools/check_styles.py`: una comprobación más (la página coincide con lo que generaría `view_styles.py`).
- `README.md`: tabla de layout y sección de uso.
- Ajuste manual en GitHub (lo hace el usuario): Settings → Pages → rama `main`, carpeta `/docs`. Hace falta hacer push para que se publique.
- Cualquier cambio futuro de estilos (p. ej. `add-dnb-styles`) tendrá que regenerar la página o `check_styles.py` fallará.
