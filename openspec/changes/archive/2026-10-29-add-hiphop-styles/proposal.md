## Why

Ninguno de los 60 estilos toca un backbeat de hip-hop: kick sincopado, caja en 2 y 4 y corcheas con swing. La familia R&B / trap solo tiene `RB`, `WCOAST R&B 110` y `VAPORTRAP`, y no hay un trap con redobles de hat en fusas ni un drill.

## What Changes

- 6 estilos nuevos en `drum_styles_v/`, con el tempo sugerido en el nombre: `BOOM BAP 90`, `LOFI HIPHOP 82`, `TRIP HOP 88`, `NEW JACK SWING 104`, `TRAP 140`, `UK DRILL 142`.
- Fuentes legibles en `styles_src/*.style`, con la escala de 5 niveles (`X x o - ,`) y su receta de groove en un comentario.
- Mismo reparto de patrones en el pad que las cumbias: p4/p5 BASE, p2/p3 ENERGÍA, p6/p7 VARIACIÓN, p0/p1 INTRO y p8 FILL.
- README, tabla "Included styles":
  - fila nueva **Hip-hop**: BOOM BAP 90 (90), LOFI HIPHOP 82 (82), TRIP HOP 88 (88), NEW JACK SWING 104 (104)
  - fila **R&B / trap**: se añaden TRAP 140 (140) y UK DRILL 142 (142)
- `docs/fingerprints.html` regenerado con `tools/view_styles.py`, para que la página agrupe los estilos nuevos.
- Sin cambios en el plugin ni en `tools/`. No se toca ningún `.txt` existente.

## Capabilities

### New Capabilities
- `hiphop-styles`: los seis estilos de hip-hop y trap, su reparto de patrones y el ritmo que define cada uno.

### Modified Capabilities

## Impact

- Archivos nuevos: `styles_src/<estilo>.style` (6) y `drum_styles_v/<ESTILO>.txt` (6).
- `README.md` (sección "Included styles") y `docs/fingerprints.html`.
- **Conflicto con los otros cambios de estilos** (`add-hiphop-styles`, `add-synth-disco-styles`, `add-afro-latin-club-styles`, `add-breaks-styles`, `add-hard-dance-styles`, `add-sambass-schaffel-styles`): todos editan la tabla del README y `docs/fingerprints.html`. Se aplican de uno en uno, regenerando la página en cada uno.
- Fuera de alcance: los géneros cuyo ritmo depende de tresillos o de la dinámica (Memphis phonk con cencerro, cloud rap), snap y crunk, y guardar el swing en el estilo.
