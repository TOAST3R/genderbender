## Why

El preview de la página de huellas suena siempre con el mismo kit sintetizado, así que un techno, un boom bap, una salsa y un gabber suenan con el mismo bombo y los mismos hats. Cuesta imaginar cómo quedaría cada estilo con su sonido. Cambiar a samples obligaría a cargar recursos externos (licencias, CORS, claves de API); en cambio, varios kits **sintetizados** dan timbres muy distintos y la página sigue siendo un solo archivo.

## What Changes

- **Nueve kits sintetizados** para el preview: Actual, 808, 909, Acústico, Lo-fi, Hardcore, 80s / Linn, Percusión y Chiptune, cada uno con sus 7 voces.
- **Selector de kit** en la cabecera y en la vista ampliada, sincronizados, con la opción **Auto** (por defecto): el kit sigue a la familia del estilo que suena y cambia con ella (también en A/B y al cambiar de estilo).
- **El kit se puede cambiar en cualquier momento**, también mientras suena: el golpe siguiente ya usa el kit nuevo.
- El kit elegido se recuerda en el navegador y entra en el permalink (`#kit=808`).
- Solo afecta al sonido de la página: ni al plugin ni al MIDI exportado.

## Capabilities

### New Capabilities

### Modified Capabilities
- `style-fingerprints`: kits sintetizados del preview, con Auto por familia.

## Impact

- `tools/view_styles.py` (plantilla y script) y `docs/fingerprints.html` regenerado.
- Sin recursos externos, sin cambios en el plugin, en los estilos ni en el MIDI.
- El kit por voz (mezclar voces de kits distintos) queda para más adelante.
