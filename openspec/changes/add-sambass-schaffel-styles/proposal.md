## Why

Dos huecos en familias que ya existen. El drum & bass no tiene ningún estilo con percusión latina, y el sambass pone surdo y tamborim sobre el two-step. El techno solo tiene rejillas rectas, y el schaffel es techno con pulso de 12/8, que el swing del plugin a ~66 % puede tocar.

## What Changes

- 2 estilos nuevos en `drum_styles_v/`, con el tempo sugerido en el nombre: `SAMBASS 172`, `SCHAFFEL 125`.
- Fuentes legibles en `styles_src/*.style`, con la escala de 5 niveles (`X x o - ,`) y su receta de groove en un comentario.
- Mismo reparto de patrones en el pad que las cumbias: p4/p5 BASE, p2/p3 ENERGÍA, p6/p7 VARIACIÓN, p0/p1 INTRO y p8 FILL.
- README, tabla "Included styles":
  - fila **Drum & bass**: se añade SAMBASS 172 (172)
  - fila **Techno**: se añade SCHAFFEL 125 (125)
- `docs/fingerprints.html` regenerado con `tools/view_styles.py`, para que la página agrupe los estilos nuevos.
- Sin cambios en el plugin ni en `tools/`. No se toca ningún `.txt` existente.

## Capabilities

### New Capabilities
- `sambass-schaffel-styles`: SAMBASS 172 en la familia Drum & bass y SCHAFFEL 125 en Techno, con el ritmo que define cada uno.

### Modified Capabilities

## Impact

- Archivos nuevos: `styles_src/<estilo>.style` (2) y `drum_styles_v/<ESTILO>.txt` (2).
- `README.md` (sección "Included styles") y `docs/fingerprints.html`.
- **Conflicto con los otros cambios de estilos** (`add-hiphop-styles`, `add-synth-disco-styles`, `add-afro-latin-club-styles`, `add-breaks-styles`, `add-hard-dance-styles`, `add-sambass-schaffel-styles`): todos editan la tabla del README y `docs/fingerprints.html`. Se aplican de uno en uno, regenerando la página en cada uno.
- Fuera de alcance: el resto de sub-géneros de techno (≈ los `Tekk…` existentes) y de drum & bass (ver `add-dnb-styles`).
