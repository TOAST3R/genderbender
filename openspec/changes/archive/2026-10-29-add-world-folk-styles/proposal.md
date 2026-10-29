## Why

Faltan casi todas las músicas tradicionales y populares fuera de España: no hay country ni americana (train beat, shuffle, bluegrass, western swing, rockabilly, zydeco), ni música celta (reel, jig, strathspey), ni ritmos cubanos y caribeños (son, salsa, mambo, cha-cha-chá, merengue, bachata, kompa) —el mayor hueco de la colección—, ni samba, baião, frevo o maracatu, ni tango, milonga, candombe o chacarera, ni huapango, son jarocho, klezmer o bhangra. Con la rejilla de tresillos con swing 67 de `add-spanish-folk-styles` caben también los shuffles y los 6/8.

## What Changes

- 36 estilos nuevos en `drum_styles_v/`, con el tempo sugerido en el nombre: `BLUES SHUFFLE 100`, `WESTERN SWING 170`, `BLUEGRASS 120`, `COUNTRY SHUFFLE 120`, `TRAIN BEAT 110`, `ROCKABILLY 180`, `ZYDECO 120`, `TWO-STEP 140`, `REEL 110`, `JIG 115`, `STRATHSPEY 120`, `IRISH POLKA 140`, `SON 95`, `RUMBA GUAGUANCO 100`, `BOLERO 80`, `MERENGUE 130`, `MAMBO 190`, `CHA-CHA-CHA 120`, `KOMPA 120`, `SALSA 180`, `BACHATA 130`, `MARACATU 90`, `FREVO 140`, `SAMBA 100`, `BAIAO 100`, `AXE 130`, `CANDOMBE 110`, `TANGO 64`, `MILONGA 90`, `CHACARERA 70`, `HUAYNO 90`, `HUAPANGO 110`, `SON JAROCHO 120`, `FREYLEKHS 130`, `BHANGRA 95`, `KEHERWA 100`.
- Fuentes legibles en `styles_src/*.style`, con la escala de 5 niveles (`X x o - ,`) y su receta de groove en un comentario.
- Mismo reparto de patrones en el pad que las cumbias: p4/p5 BASE, p2/p3 ENERGÍA, p6/p7 VARIACIÓN, p0/p1 INTRO y p8 FILL.
- README, tabla "Included styles":
  - filas nuevas **Country / Americana**, **Celtic**, **Latin / Caribbean**, **Brazil**, **South America** y **World folk**, en su sitio alfabético, con los estilos en el orden de `design.md`
- `docs/fingerprints.html` regenerado con `tools/view_styles.py`, para que la página agrupe los estilos nuevos.
- Sin cambios en el plugin ni en `tools/`. No se toca ningún `.txt` existente.

## Capabilities

### New Capabilities
- `world-folk-styles`: los 36 estilos de country, celta, latino y caribeño, Brasil, Río de la Plata y Andes, México, klezmer e India, su reparto en seis familias y el ritmo que define cada uno.

### Modified Capabilities

## Impact

- Archivos nuevos: `styles_src/<estilo>.style` (36) y `drum_styles_v/<ESTILO>.txt` (36).
- `README.md` (sección "Included styles") y `docs/fingerprints.html`.
- Los ocho estilos ternarios dependen de que el swing global esté en 67; se dice en su cabecera y en la nota del README.
- Fuera de alcance: los estilos descartados (ver Decisions en `design.md`).
