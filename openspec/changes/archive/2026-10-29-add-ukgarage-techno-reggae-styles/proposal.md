## Why

La familia UK garage está repartida en tres filas (UK garage / 2-step, Grime y Dubstep) y le faltan speed garage, bassline, breakstep y wonky. La fila Techno mezcla los clásicos con los estilos originales del editor sin orden y le faltan subgéneros (bleep, ambient, tribal, deep, hypnotic, peak time, industrial). Y no hay ningún estilo de reggae: ni ska, ni rocksteady, ni el one drop del roots, ni steppers, rockers, dub o dancehall digital.

## What Changes

- 20 estilos nuevos en `drum_styles_v/`, con el tempo sugerido en el nombre: `SPEED GARAGE 135`, `BASSLINE 138`, `BREAKSTEP 140`, `WONKY 140`, `BLEEP TECHNO 122`, `AMBIENT TECHNO 120`, `TRIBAL TECHNO 130`, `DEEP TECHNO 124`, `HYPNOTIC TECHNO 130`, `PEAK TIME TECHNO 132`, `INDUSTRIAL TECHNO 140`, `SKA 120`, `ROCKSTEADY 80`, `ROOTS REGGAE 75`, `DUB 70`, `ROCKERS 80`, `STEPPERS 75`, `TWO TONE 160`, `DIGITAL DANCEHALL 95`, `MODERN DANCEHALL 100`.
- Fuentes legibles en `styles_src/*.style`, con la escala de 5 niveles (`X x o - ,`) y su receta de groove en un comentario.
- Mismo reparto de patrones en el pad que las cumbias: p4/p5 BASE, p2/p3 ENERGÍA, p6/p7 VARIACIÓN, p0/p1 INTRO y p8 FILL.
- README, tabla "Included styles":
  - fila **UK garage** (antes "UK garage / 2-step"): se le unen Grime y Dubstep y se añaden SPEED GARAGE 135 (135), BASSLINE 138 (138), BREAKSTEP 140 (140) y WONKY 140 (140), en el orden de `design.md`
  - fila **Techno**: en orden cronológico, con BLEEP TECHNO 122 (122), AMBIENT TECHNO 120 (120), TRIBAL TECHNO 130 (130), DEEP TECHNO 124 (124), HYPNOTIC TECHNO 130 (130), PEAK TIME TECHNO 132 (132) e INDUSTRIAL TECHNO 140 (140) en su sitio
  - fila nueva **Reggae / dancehall**: SKA 120 (120), ROCKSTEADY 80 (80), ROOTS REGGAE 75 (75), DUB 70 (70), ROCKERS 80 (80), STEPPERS 75 (75), TWO TONE 160 (160), DIGITAL DANCEHALL 95 (95), 101 DANCEHALL (95), MODERN DANCEHALL 100 (100)
  - fila "Reggaeton / dancehall" renombrada a **Reggaeton / funk carioca**
- `docs/fingerprints.html` regenerado con `tools/view_styles.py`, para que la página agrupe los estilos nuevos.
- Sin cambios en el plugin ni en `tools/`. No se toca ningún `.txt` existente.

## Capabilities

### New Capabilities
- `ukgarage-techno-reggae-styles`: los 20 estilos nuevos de UK garage, techno y reggae/dancehall, la reorganización de esas familias en el README y el ritmo que define cada estilo.

### Modified Capabilities

## Impact

- Archivos nuevos: `styles_src/<estilo>.style` (20) y `drum_styles_v/<ESTILO>.txt` (20).
- `README.md` (sección "Included styles") y `docs/fingerprints.html`.
- **Reorganiza familias**: desaparecen "Grime" y "Dubstep" (sus estilos pasan a "UK garage"), "UK garage / 2-step" pasa a "UK garage" y "Reggaeton / dancehall" a "Reggaeton / funk carioca". El selector de género de la página cambia en consecuencia. Se aplica encima de `add-fingerprints-audio-preview`, que también toca el README.
- Fuera de alcance: los subgéneros de Non-Goals en `design.md`.
