## Why

La página de huellas tiene el mismo aspecto para un gabber que para una cumbia, y el tempo de cada estilo es fijo: no se puede oír un estilo más lento para entenderlo o más rápido para compararlo con otro. Una escena animada por familia, que se mueve al tempo y con los golpes, da carácter a cada género y une lo que se ve con lo que se oye. Un slider de BPM permite cambiar el tempo sin perder el de cada estilo.

## What Changes

- **Slider de BPM** (40–240) en la cabecera y en la vista ampliada, sincronizados, con **↺** para volver al BPM del estilo. Al pulsar Play en otro estilo vuelve a su BPM (como el Swing). Si se ha movido, A/B toca los dos estilos a ese tempo. Cambiarlo a mitad de compás no salta. El MIDI exportado usa ese tempo. Entra en el permalink (`#bpm=…`) cuando no es el del estilo.
- **Nueve escenas animadas** de fondo, una por grupo de kit: 909 (panel TR con la tira de pasos), 808 (túnel de anillos), Acústico (batería vista desde arriba), Lo-fi (vinilo girando), Hardcore (franjas de aviso y sacudida), 80s (rejilla synthwave con sol), Percusión (tejido con ondas), Chiptune (CRT con ecualizador de bloques) y Otros (grano suave).
- Las escenas se mueven **al tempo** y reaccionan a **los golpes** (cola de pasos) y a **la energía** (analizador). Siguen al estilo que suena, también en A/B, con un fundido de 400 ms; sin reproducción, siguen al género del filtro.
- Sin destellos a pantalla completa; con `prefers-reduced-motion`, imagen fija. Las huellas van sobre tarjetas sólidas para que se lean siempre.
- Solo afecta a la página: ni al plugin ni a los estilos.

## Capabilities

### New Capabilities

### Modified Capabilities
- `style-fingerprints`: slider de BPM y escenas animadas por familia.

## Impact

- `tools/view_styles.py` (plantilla) y `docs/fingerprints.html` regenerado (unos 15–25 KB más).
- El MIDI exportado cambia de tempo si se mueve el slider (las notas no cambian).
- Sin recursos externos, sin cambios en el plugin ni en los estilos.
