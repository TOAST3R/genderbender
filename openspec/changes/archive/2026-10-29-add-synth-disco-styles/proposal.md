## Why

No hay ningún backbeat de pop/rock ochentero ni ningún disco. Las casas que hay (`Chicago.Jouse 125`, `JetoHouse 135`) son house, y ningún estilo usa los toms como protagonistas de los fills, que es lo que define el sonido LinnDrum y Simmons.

## What Changes

- 3 estilos nuevos en `drum_styles_v/`, con el tempo sugerido en el nombre: `SYNTHWAVE 100`, `DISCO 118`, `ITALO DISCO 120`.
- Fuentes legibles en `styles_src/*.style`, con la escala de 5 niveles (`X x o - ,`) y su receta de groove en un comentario.
- Mismo reparto de patrones en el pad que las cumbias: p4/p5 BASE, p2/p3 ENERGÍA, p6/p7 VARIACIÓN, p0/p1 INTRO y p8 FILL.
- README, tabla "Included styles":
  - fila nueva **Synth / disco**: SYNTHWAVE 100 (100), DISCO 118 (118), ITALO DISCO 120 (120)
- `docs/fingerprints.html` regenerado con `tools/view_styles.py`, para que la página agrupe los estilos nuevos.
- Sin cambios en el plugin ni en `tools/`. No se toca ningún `.txt` existente.

## Capabilities

### New Capabilities
- `synth-disco-styles`: los tres estilos de synthwave y disco, su reparto de patrones y el ritmo que define cada uno.

### Modified Capabilities

## Impact

- Archivos nuevos: `styles_src/<estilo>.style` (3) y `drum_styles_v/<ESTILO>.txt` (3).
- `README.md` (sección "Included styles") y `docs/fingerprints.html`.
- **Conflicto con los otros cambios de estilos** (`add-hiphop-styles`, `add-synth-disco-styles`, `add-afro-latin-club-styles`, `add-breaks-styles`, `add-hard-dance-styles`, `add-sambass-schaffel-styles`): todos editan la tabla del README y `docs/fingerprints.html`. Se aplican de uno en uno, regenerando la página en cada uno.
- Fuera de alcance: Hi-NRG, Eurobeat, Eurodance, nu-disco y synth-pop, que en este plugin sonarían como DISCO o ITALO DISCO.
