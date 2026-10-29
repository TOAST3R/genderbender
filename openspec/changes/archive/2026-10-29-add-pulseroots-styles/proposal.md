## Why

El árbol de géneros de PulseRoots (https://mendiak.github.io/pulse.roots/, datos en `data/pulseroots.genres.json`) tiene 14 familias y 293 subgéneros. Comparados con los 122 estilos actuales: unos 70 ya están cubiertos, unos 60 no tienen batería (ambient, drone, noise, música concreta, clásica…) y unos 130 solo se diferencian de otro por el sonido. Quedan 31 con una rejilla propia que todavía no está: IDM y club experimental, variantes de techno y hardcore, phonk, future bass y midtempo, y ritmos globales como dembow, singeli, nortec o bossa.

## What Changes

- 31 estilos nuevos en `drum_styles_v/`, con el tempo sugerido en el nombre: `GLITCH HOP 110`, `IDM 120`, `SKWEEE 100`, `DECONSTRUCTED CLUB 130`, `MICROHOUSE 124`, `DUB TECHNO 118`, `SCHRANZ 150`, `HARDGROOVE 135`, `FRENCHCORE 200`, `INDUSTRIAL HARDCORE 150`, `HARDSTYLE 150`, `BAKALAO 125`, `BOOGIE 110`, `MOTORIK 120`, `FUTURE GARAGE 130`, `PSYBIENT 100`, `NEUROFUNK 174`, `LIQUID DNB 174`, `RIDDIM 140`, `FUTURE BASS 150`, `MIDTEMPO BASS 105`, `PHONK 130`, `DRIFT PHONK 155`, `BRAZILIAN PHONK 130`, `BROKEN BEAT 120`, `BOSSA NOVA CHILL 100`, `DEMBOW 120`, `FUNK DE RAIZ 130`, `SINGELI 200`, `NORTEC 125`, `ACID JAZZ 105`.
- Fuentes legibles en `styles_src/*.style`, con la escala de 5 niveles (`X x o - ,`) y su receta de groove en un comentario.
- Mismo reparto de patrones en el pad que las cumbias: p4/p5 BASE, p2/p3 ENERGÍA, p6/p7 VARIACIÓN, p0/p1 INTRO y p8 FILL.
- README, tabla "Included styles":
  - fila nueva **Bass music**: FUTURE BASS 150 (150), MIDTEMPO BASS 105 (105)
  - fila nueva **Downtempo / chill**: BOSSA NOVA CHILL 100 (100)
  - fila nueva **IDM / experimental**: GLITCH HOP 110 (110), IDM 120 (120), SKWEEE 100 (100), DECONSTRUCTED CLUB 130 (130)
  - fila nueva **Phonk**: PHONK 130 (130), DRIFT PHONK 155 (155), BRAZILIAN PHONK 130 (130)
  - filas existentes: House (+MICROHOUSE), Techno (+DUB TECHNO, SCHRANZ, HARDGROOVE), Hardcore / hard dance (+FRENCHCORE, INDUSTRIAL HARDCORE, HARDSTYLE, BAKALAO), Synth / disco (+BOOGIE, MOTORIK), UK garage / 2-step (+FUTURE GARAGE), Psytrance (+PSYBIENT), Drum & bass (+NEUROFUNK, LIQUID DNB), Dubstep (+RIDDIM), Breaks (+BROKEN BEAT), Reggaeton / dancehall (+DEMBOW, FUNK DE RAIZ), Afro / Latin club (+SINGELI, NORTEC), Funk / New Orleans (+ACID JAZZ)
- `docs/fingerprints.html` regenerado con `tools/view_styles.py`, para que la página agrupe los estilos nuevos.
- Sin cambios en el plugin ni en `tools/`. No se toca ningún `.txt` existente.

## Capabilities

### New Capabilities
- `pulseroots-styles`: los 31 estilos sacados del árbol de géneros de PulseRoots que tienen una rejilla de batería propia, su reparto de patrones y el ritmo que define cada uno.

### Modified Capabilities

## Impact

- Archivos nuevos: `styles_src/<estilo>.style` (31) y `drum_styles_v/<ESTILO>.txt` (31).
- `README.md` (sección "Included styles") y `docs/fingerprints.html`.
- **Orden de la tabla**: las filas nuevas se insertan en orden alfabético, así que la página de huellas y su selector de género las muestran en su sitio.
- Fuera de alcance: los subgéneros descartados (ver Non-Goals en `design.md`).
