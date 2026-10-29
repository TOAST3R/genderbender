## Why

No hay trance ni hard dance. Casi todos sus sub-géneros se distinguen por el sonido y no por la batería, pero dos aportan algo nuevo: el trance usa el redoble de caja como subida, que con la escala de 5 niveles se puede tocar con Density, y la mákina es un género de baile propio con caja en vez de palmas.

## What Changes

- 2 estilos nuevos en `drum_styles_v/`, con el tempo sugerido en el nombre: `TRANCE 138`, `MAKINA 170`.
- Fuentes legibles en `styles_src/*.style`, con la escala de 5 niveles (`X x o - ,`) y su receta de groove en un comentario.
- Mismo reparto de patrones en el pad que las cumbias: p4/p5 BASE, p2/p3 ENERGÍA, p6/p7 VARIACIÓN, p0/p1 INTRO y p8 FILL.
- README, tabla "Included styles":
  - fila nueva **Hard dance**: TRANCE 138 (138), MAKINA 170 (170)
- `docs/fingerprints.html` regenerado con `tools/view_styles.py`, para que la página agrupe los estilos nuevos.
- Sin cambios en el plugin ni en `tools/`. No se toca ningún `.txt` existente.

## Capabilities

### New Capabilities
- `hard-dance-styles`: los dos estilos de trance y mákina, su reparto de patrones y su uso de Density como subida.

### Modified Capabilities

## Impact

- Archivos nuevos: `styles_src/<estilo>.style` (2) y `drum_styles_v/<ESTILO>.txt` (2).
- `README.md` (sección "Included styles") y `docs/fingerprints.html`.
- **Conflicto con los otros cambios de estilos** (`add-hiphop-styles`, `add-synth-disco-styles`, `add-afro-latin-club-styles`, `add-breaks-styles`, `add-hard-dance-styles`, `add-sambass-schaffel-styles`): todos editan la tabla del README y `docs/fingerprints.html`. Se aplican de uno en uno, regenerando la página en cada uno.
- Fuera de alcance: el resto de trance y hard dance (ver Non-Goals en `design.md`).
