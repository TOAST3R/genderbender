## Why

No hay ningún estilo de música tradicional española. El reto es que casi toda va en compás ternario (muiñeira y sardana en 6/8, jota y sevillana en 3/4, bulería, soleá y seguiriya en compás de 12), y el patrón del plugin son 32 pasos de un 4/4 que no se dividen entre 3. Con swing 67 la deformación del plugin lleva los pasos 0, 2 y 5 de cada negra exactamente a 0, 1/3 y 2/3 de la negra: un tresillo exacto. Eso permite escribir los compases ternarios sin tocar el plugin.

## What Changes

- 16 estilos nuevos en `drum_styles_v/`, con el tempo sugerido en el nombre: `MUINEIRA 120`, `PASACORREDOIRA 110`, `MARCHA PROCESIONAL 70`, `ARIN-ARIN 130`, `BIRIBILKETA 110`, `JOTA ARAGONESA 60`, `SARDANA 100`, `BALL DE BASTONS 110`, `TANGOS 100`, `TIENTOS 75`, `BULERIA 80`, `SOLEA 50`, `SEGUIRIYA 45`, `SEVILLANA 65`, `FANDANGO DE HUELVA 60`, `TAJARASTE 110`.
- Fuentes legibles en `styles_src/*.style`, con la escala de 5 niveles (`X x o - ,`) y su receta de groove en un comentario.
- Mismo reparto de patrones en el pad que las cumbias: p4/p5 BASE, p2/p3 ENERGÍA, p6/p7 VARIACIÓN, p0/p1 INTRO y p8 FILL.
- README, tabla "Included styles":
  - fila nueva **Flamenco**: TANGOS 100 (100), TIENTOS 75 (75), BULERIA 80 (80), SOLEA 50 (50), SEGUIRIYA 45 (45), SEVILLANA 65 (65), FANDANGO DE HUELVA 60 (60)
  - fila nueva **Folk ibérico**: MUINEIRA 120 (120), PASACORREDOIRA 110 (110), MARCHA PROCESIONAL 70 (70), ARIN-ARIN 130 (130), BIRIBILKETA 110 (110), JOTA ARAGONESA 60 (60), SARDANA 100 (100), BALL DE BASTONS 110 (110), TAJARASTE 110 (110)
- `docs/fingerprints.html` regenerado con `tools/view_styles.py`, para que la página agrupe los estilos nuevos.
- Sin cambios en el plugin ni en `tools/`. No se toca ningún `.txt` existente.

## Capabilities

### New Capabilities
- `spanish-folk-styles`: los 16 estilos de folclore español y flamenco, la rejilla de tresillos con swing 67 para los compases ternarios y el ritmo que define cada uno.

### Modified Capabilities

## Impact

- Archivos nuevos: `styles_src/<estilo>.style` (16) y `drum_styles_v/<ESTILO>.txt` (16).
- `README.md` (sección "Included styles") y `docs/fingerprints.html`.
- Los nueve estilos ternarios dependen de que el swing global esté en 67; se dice en la cabecera de cada fuente y en el README.
- Fuera de alcance: los estilos de la lista descartados (ver Non-Goals en `design.md`).
