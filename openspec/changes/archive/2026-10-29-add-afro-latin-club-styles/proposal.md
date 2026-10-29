## Why

La mayoría de los estilos dejan casi vacíos los toms. Los géneros de club afro y latino recientes (amapiano, afro house, kuduro, guaracha) viven de la percusión, y solo `GQOM` y `AFRO BEAT` cubren algo de ese terreno.

## What Changes

- 4 estilos nuevos en `drum_styles_v/`, con el tempo sugerido en el nombre: `AMAPIANO 112`, `AFRO HOUSE 122`, `KUDURO 135`, `GUARACHA 130`.
- Fuentes legibles en `styles_src/*.style`, con la escala de 5 niveles (`X x o - ,`) y su receta de groove en un comentario.
- Mismo reparto de patrones en el pad que las cumbias: p4/p5 BASE, p2/p3 ENERGÍA, p6/p7 VARIACIÓN, p0/p1 INTRO y p8 FILL.
- README, tabla "Included styles":
  - fila nueva **Afro / Latin club**: AMAPIANO 112 (112), AFRO HOUSE 122 (122), KUDURO 135 (135), GUARACHA 130 (130)
- `docs/fingerprints.html` regenerado con `tools/view_styles.py`, para que la página agrupe los estilos nuevos.
- Sin cambios en el plugin ni en `tools/`. No se toca ningún `.txt` existente.

## Capabilities

### New Capabilities
- `afro-latin-club-styles`: los cuatro estilos de club afro y latino, su reparto de patrones y el ritmo que define cada uno.

### Modified Capabilities

## Impact

- Archivos nuevos: `styles_src/<estilo>.style` (4) y `drum_styles_v/<ESTILO>.txt` (4).
- `README.md` (sección "Included styles") y `docs/fingerprints.html`.
- **Conflicto con los otros cambios de estilos** (`add-hiphop-styles`, `add-synth-disco-styles`, `add-afro-latin-club-styles`, `add-breaks-styles`, `add-hard-dance-styles`, `add-sambass-schaffel-styles`): todos editan la tabla del README y `docs/fingerprints.html`. Se aplican de uno en uno, regenerando la página en cada uno.
- Fuera de alcance: afrobeats (falta saber si `AFRO BEAT` ya lo cubre), azonto, coupé-décalé, rabòday, changa tuki, budots, kwaito, tribal guarachero de Monterrey (pide tresillos) y tecnocumbia (≈ `CUMBIA DIGITAL 100`).
