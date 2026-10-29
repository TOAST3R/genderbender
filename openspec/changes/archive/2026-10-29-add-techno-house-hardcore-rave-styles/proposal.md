## Why

Los estilos "Techno" que hay (`techAXX`, `Tekk…`) no tocan bombo a negras: con Density por defecto solo suena el bombo en la negra 1. No hay techno de Detroit, minimal, acid ni UK techno; el house solo tiene `Chicago.Jouse 125`, `JetoHouse 135` y `MIAMI BEIGE 135`; no hay gabber ni happy hardcore, y falta todo el rave de 1991–93 (breakbeat hardcore, hoover belga, darkcore), el psytrance y sus subgéneros, el hard house y sus variantes, el EBM y sus variantes, y el drill and bass. Como estos géneros comparten casi todos el bombo a negras y se distinguen sobre todo por el sonido, cada estilo tiene que ganarse su sitio con la rejilla: dónde va el clap, cómo se mueven los hats, redobles, toms o bombos rotos.

## What Changes

- 42 estilos nuevos en `drum_styles_v/`, con el tempo sugerido en el nombre: `DETROIT TECHNO 128`, `MINIMAL TECHNO 126`, `HARD TECHNO 145`, `ACID TECHNO 140`, `UK TECHNO 135`, `DEEP HOUSE 122`, `TECH HOUSE 126`, `GHETTOTECH 150`, `ACID HOUSE 124`, `ITALO HOUSE 122`, `GABBER 180`, `GABBER ROLL 180`, `HAPPY HARDCORE 170`, `GOA TRANCE 145`, `FULL-ON 145`, `PROGRESSIVE PSY 138`, `DARK PSY 150`, `FOREST PSY 150`, `PSYCORE 190`, `ZENONESQUE 135`, `MINIMAL PSY 140`, `HI-TECH 180`, `NITZHONOT 150`, `SUOMISAUNDI 150`, `PSYBREAKS 135`, `PSYDUB 100`, `UK HARD HOUSE 150`, `HARD NRG 155`, `SCOUSE HOUSE 150`, `CHICAGO HARD HOUSE 135`, `DUTCH HOUSE 128`, `EBM 120`, `BELGIAN EBM 118`, `NEW BEAT 110`, `AGGROTECH 140`, `DARK ELECTRO 125`, `EBM TECHNO 130`, `RAVE 91 130`, `HARDCORE TECHNO 145`, `BREAKBEAT HARDCORE 145`, `DARKCORE 155`, `DRILL N BASS 175`.
- Fuentes legibles en `styles_src/*.style`, con la escala de 5 niveles (`X x o - ,`) y su receta de groove en un comentario.
- Mismo reparto de patrones en el pad que las cumbias: p4/p5 BASE, p2/p3 ENERGÍA, p6/p7 VARIACIÓN, p0/p1 INTRO y p8 FILL.
- README, tabla "Included styles":
  - fila **Techno**: se añaden DETROIT TECHNO 128 (128), MINIMAL TECHNO 126 (126), HARD TECHNO 145 (145), ACID TECHNO 140 (140), UK TECHNO 135 (135)
  - fila **House**: se añaden DEEP HOUSE 122 (122), TECH HOUSE 126 (126), GHETTOTECH 150 (150), ACID HOUSE 124 (124), ITALO HOUSE 122 (122)
  - fila **Hard dance** renombrada a **Hardcore / hard dance**: se añaden GABBER 180 (180), GABBER ROLL 180 (180), HAPPY HARDCORE 170 (170)
  - fila nueva **Psytrance**: GOA TRANCE 145 (145), FULL-ON 145 (145), PROGRESSIVE PSY 138 (138), DARK PSY 150 (150), MINIMAL PSY 140 (140), HI-TECH 180 (180), SUOMISAUNDI 150 (150), PSYBREAKS 135 (135), PSYDUB 100 (100), FOREST PSY 150 (150), PSYCORE 190 (190), ZENONESQUE 135 (135), NITZHONOT 150 (150)
  - fila nueva **Hard house**: UK HARD HOUSE 150 (150), HARD NRG 155 (155), SCOUSE HOUSE 150 (150), CHICAGO HARD HOUSE 135 (135), DUTCH HOUSE 128 (128)
  - fila nueva **EBM / industrial**: EBM 120 (120), BELGIAN EBM 118 (118), NEW BEAT 110 (110), AGGROTECH 140 (140), DARK ELECTRO 125 (125), EBM TECHNO 130 (130)
  - fila **Breaks**: se añade DRILL N BASS 175 (175)
  - fila nueva **Rave / oldskool**: RAVE 91 130 (130), HARDCORE TECHNO 145 (145), BREAKBEAT HARDCORE 145 (145), DARKCORE 155 (155)
- `docs/fingerprints.html` regenerado con `tools/view_styles.py`, para que la página agrupe los estilos nuevos.
- Sin cambios en el plugin ni en `tools/`. No se toca ningún `.txt` existente.

## Capabilities

### New Capabilities
- `techno-house-hardcore-rave-styles`: los 42 estilos de techno, house, hardcore, psytrance, hard house, EBM, rave oldskool y drill and bass, su reparto de patrones y el ritmo que define cada uno.

### Modified Capabilities
- `hard-dance-styles`: la fila "Hard dance" del README pasa a llamarse "Hardcore / hard dance".

## Impact

- Archivos nuevos: `styles_src/<estilo>.style` (42) y `drum_styles_v/<ESTILO>.txt` (42).
- `README.md` (sección "Included styles") y `docs/fingerprints.html`.
- **Renombra una familia**: "Hard dance" pasa a "Hardcore / hard dance", así que el selector de género de la página de huellas cambia de nombre para TRANCE 138 y MAKINA 170.
- Fuera de alcance: los géneros de Non-Goals en `design.md`, y la línea 303 de los acid (el plugin solo toca batería).
