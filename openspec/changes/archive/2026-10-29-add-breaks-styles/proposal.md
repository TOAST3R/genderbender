## Why

Los breaks solo aparecen dentro del drum & bass. Faltan el breakbeat a tempo medio del big beat, el break troceado del Baltimore club (el origen del Jersey club, que sí está) y el amen destrozado en fusas del breakcore.

## What Changes

- 3 estilos nuevos en `drum_styles_v/`, con el tempo sugerido en el nombre: `BIG BEAT 125`, `BALTIMORE CLUB 130`, `BREAKCORE 190`.
- Fuentes legibles en `styles_src/*.style`, con la escala de 5 niveles (`X x o - ,`) y su receta de groove en un comentario.
- Mismo reparto de patrones en el pad que las cumbias: p4/p5 BASE, p2/p3 ENERGÍA, p6/p7 VARIACIÓN, p0/p1 INTRO y p8 FILL.
- README, tabla "Included styles":
  - fila nueva **Breaks**: BIG BEAT 125 (125), BALTIMORE CLUB 130 (130), BREAKCORE 190 (190)
- `docs/fingerprints.html` regenerado con `tools/view_styles.py`, para que la página agrupe los estilos nuevos.
- Sin cambios en el plugin ni en `tools/`. No se toca ningún `.txt` existente.

## Capabilities

### New Capabilities
- `breaks-styles`: los tres estilos de breakbeat, su reparto de patrones y el ritmo que define cada uno.

### Modified Capabilities

## Impact

- Archivos nuevos: `styles_src/<estilo>.style` (3) y `drum_styles_v/<ESTILO>.txt` (3).
- `README.md` (sección "Included styles") y `docs/fingerprints.html`.
- **Conflicto con los otros cambios de estilos** (`add-hiphop-styles`, `add-synth-disco-styles`, `add-afro-latin-club-styles`, `add-breaks-styles`, `add-hard-dance-styles`, `add-sambass-schaffel-styles`): todos editan la tabla del README y `docs/fingerprints.html`. Se aplican de uno en uno, regenerando la página en cada uno.
- Fuera de alcance: nu skool breaks, Florida breaks, acid breaks y progressive breaks (≈ BIG BEAT en este plugin), broken beat (depende de la dinámica) y drill 'n' bass (≈ BREAKCORE).
