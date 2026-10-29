## Why

Los tres estilos de la familia "Electro / Miami bass" están rotos: ELECTRO CYBOTRON y ELECTRO UR 138 solo tienen notas en p0/p1 y BASS 101 en p0–p3, así que su BASE (p4/p5) está vacía y no suenan ni en el centro del pad ni en el preview de la página. AFRO BEAT tiene los 9 patrones vacíos. Son estilos antiguos (commit `7db9261`) sin fuente en `styles_src/`, y `check_styles.py` no lo detecta porque solo comprueba el formato. Además, a la familia le faltan casi todos sus subgéneros: electro clásico de Detroit, electro-funk, electro-bass, electro house, outrun, electroclash, darkwave y electro industrial actual.

## What Changes

- 9 estilos nuevos en `drum_styles_v/`, con el tempo sugerido en el nombre: `CYBOTRON ELECTRO 125`, `ELECTRO FUNK 127`, `DARKWAVE 120`, `ELECTRO BASS 130`, `DETROIT ELECTRO 130`, `ELECTROCLASH 125`, `ELECTRO HOUSE 128`, `OUTRUN 118`, `INDUSTRIAL ELECTRO 130`.
- Fuentes legibles en `styles_src/*.style`, con la escala de 5 niveles (`X x o - ,`) y su receta de groove en un comentario.
- Mismo reparto de patrones en el pad que las cumbias: p4/p5 BASE, p2/p3 ENERGÍA, p6/p7 VARIACIÓN, p0/p1 INTRO y p8 FILL.
- README, tabla "Included styles":
  - fila **Electro** (antes "Electro / Miami bass"): los nueve nuevos más SYNTHWAVE 100, DARK ELECTRO 125 y GHETTOTECH 150, en el orden de `design.md`; salen ELECTRO CYBOTRON, ELECTRO UR 138 y BASS 101
  - filas **Synth / disco**, **EBM / industrial** y **House**: pierden SYNTHWAVE 100, DARK ELECTRO 125 y GHETTOTECH 150
  - fila **Afro / Caribbean**: sale AFRO BEAT
- `docs/fingerprints.html` regenerado con `tools/view_styles.py`, para que la página agrupe los estilos nuevos.
- Se borran 4 `.txt` rotos (ELECTRO CYBOTRON, ELECTRO UR 138, BASS 101 y AFRO BEAT).
- `tools/check_styles.py` falla si un estilo tiene la BASE (p4 o p5) vacía.
- Sin cambios en el plugin.

## Capabilities

### New Capabilities
- `electro-styles`: la familia Electro rehecha: nueve estilos nuevos, tres movidos de otras familias, el orden cronológico de la fila y el ritmo que define cada uno.

### Modified Capabilities
- `style-authoring`: `check_styles.py` exige que p4 y p5 tengan notas.
- `synth-disco-styles`: SYNTHWAVE 100 pasa a la familia Electro.
- `techno-house-hardcore-rave-styles`: GHETTOTECH 150 y DARK ELECTRO 125 pasan a la familia Electro.

## Impact

- Archivos nuevos: `styles_src/<estilo>.style` (9) y `drum_styles_v/<ESTILO>.txt` (9).
- `README.md` (sección "Included styles") y `docs/fingerprints.html`.
- `tools/check_styles.py`; se borran `drum_styles_v/ELECTRO CYBOTRON.txt`, `ELECTRO UR 138.txt`, `BASS 101.txt` y `AFRO BEAT.txt`.
- Fuera de alcance: los subgéneros de Non-Goals en `design.md`.
