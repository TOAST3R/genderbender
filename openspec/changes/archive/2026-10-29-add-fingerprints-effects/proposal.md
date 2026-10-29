## Why

Con los kits, el preview ya suena distinto en cada familia, pero sigue sonando seco: sin sala, sin eco y sin saturación. Muchos estilos (dub, techno, downtempo, gabber) no se reconocen sin su espacio o su distorsión. Tres knobs globales de efectos dejan probar eso sin salir de la página y sin cargar recursos externos.

## What Changes

- **Bus maestro** en el preview: todas las voces y las salidas de los kits pasan por él antes de llegar a los altavoces.
- **Tres knobs** de efectos globales: **Distortion** (saturación con compensación de volumen), **Delay** (eco sincronizado al BPM, corchea con puntillo, con realimentación) y **Reverb** (respuesta de impulso generada en la página).
- Los knobs están en la cabecera y en la vista ampliada, sincronizados, y se pueden mover mientras suena.
- Los valores se recuerdan en el navegador y entran en el permalink (`#dist=…&dly=…&rev=…`) cuando no son 0.
- Solo afecta al sonido de la página: ni al plugin ni al MIDI exportado.

## Capabilities

### New Capabilities

### Modified Capabilities
- `style-fingerprints`: efectos globales (distortion, delay y reverb) del preview.

## Impact

- `tools/view_styles.py` (plantilla) y `docs/fingerprints.html` regenerado.
- Sin recursos externos, sin cambios en el plugin, en los estilos ni en el MIDI.
- Los envíos por voz (por ejemplo, reverb solo en la caja) quedan para más adelante, junto con el kit por voz.
