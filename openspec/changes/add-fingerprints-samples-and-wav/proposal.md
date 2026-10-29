## Why

El preview de la página de huellas solo suena con kits sintetizados, y lo que se oye no se puede sacar como audio: solo como MIDI. Quien quiere probar un estilo con sus propios samples, o llevarse el loop a un DAW o a un sampler, tiene que reconstruirlo a mano. Cargar samples del portátil y exportar WAV cierra ese círculo sin subir nada a ningún servidor.

## What Changes

- **Samples propios por voz**: en la vista ampliada, cada voz puede cargar un archivo de audio del portátil (botón o arrastrándolo sobre el nombre de la voz) y volver al kit con ✕. Las voces sin sample siguen con el kit. Ganancia por sample y el valor del paso (0–255) como velocity. El hhc sigue cortando al hho.
- Los samples se **guardan en IndexedDB** (solo en el navegador) y siguen ahí al recargar. La página avisa "samples propios" cuando hay alguno, porque el permalink no los lleva.
- **Exportar WAV** (16 bits, 44,1 kHz, estéreo) de lo que se oye: Density, Swing, BPM, kit o samples, velocity, mute/solo y efectos.
  - Por parte: en cada patrón (p0–p8), **⠿ WAV** para arrastrar al escritorio o al DAW y **⬇** para descargar.
  - **⬇ secuencia .wav** (INTRO → BASE → ENERGÍA → VARIACIÓN → FILL, como ▶ secuencia).
  - **⬇ todas las partes .zip** (las vacías no se incluyen).
  - Compases: 1, 2, 4 u 8 (por parte); **colas envueltas** activadas por defecto para que el loop empalme.
- El audio pasa a construirse sobre el contexto que se le dé, para que el directo y el render offline compartan el mismo código.

## Capabilities

### New Capabilities

### Modified Capabilities
- `style-fingerprints`: samples propios por voz y exportación WAV.

## Impact

- `tools/view_styles.py` (plantilla) y `docs/fingerprints.html` regenerado.
- La página sigue sin cargar recursos externos: los samples son archivos locales que el usuario elige y no salen del navegador.
- Sin cambios en el plugin, en los estilos ni en el MIDI exportado.
- Para más adelante: stems (un WAV por voz, reutilizando el ZIP), captura en directo con el pad, y afinación y recorte por sample.
