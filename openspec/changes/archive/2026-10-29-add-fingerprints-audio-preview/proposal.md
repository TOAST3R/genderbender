## Why

La página de huellas enseña la rejilla de cada estilo, pero no cómo suena. Para comprobar si dos estilos se distinguen, o cómo entran las capas de Density, hay que abrir REAPER. Un preview de audio en la propia página deja escuchar el ritmo de cualquier estilo con un clic.

## What Changes

- Botón **▶ Play** en cada estilo de `docs/fingerprints.html`. Al pulsarlo suena en bucle su BASE (p4 en el compás 1 y p5 en el 2, como el plugin) y el botón pasa a **■ Stop**. Solo suena un estilo a la vez: pulsar Play en otro para el anterior. Esc también lo para.
- En la vista ampliada, un ▶ por patrón (p0–p8) para escuchar cada uno en bucle.
- El sonido se sintetiza en el navegador con Web Audio (bombo, caja, palmas, hats, toms), sin muestras: la página sigue siendo un solo archivo sin recursos externos.
- **Tempo:** el BPM que indica el nombre del estilo (`DETROIT TECHNO 128` → 128). Si el nombre no lo lleva, el de su entrada en la tabla del README (`101 JUKE (160)`), y si tampoco, 120. No hay campo para cambiarlo.
- README: se añade `(bpm)` a las 35 entradas cuyo nombre no lleva BPM (sin renombrar ningún archivo).
- El slider de Density existente se aplica también al sonido (`256 − v < Density`), y un slider de swing (50–75 %) aplica la deformación de `groove-swing`. Al pulsar Play, el swing pasa solo al de la receta del estilo (`styles_src/*.style`), con su amount por voz; sin fuente, 50.
- Sin cambios en el plugin ni en los estilos.

## Capabilities

### New Capabilities

### Modified Capabilities
- `style-fingerprints`: preview de audio con Play/Stop y tempo por estilo.

## Impact

- `tools/view_styles.py` (plantilla HTML, script y cálculo del BPM de cada estilo) y `docs/fingerprints.html` regenerado.
- `README.md`: `(bpm)` en 35 entradas de la tabla "Included styles".
- El preview no reproduce el sonido del sampler de REAPER: sirve para oír el ritmo, no el timbre.
