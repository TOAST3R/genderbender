## Why

Al probar un estilo en la página de huellas se oye, pero no se ve qué paso está sonando ni qué hace el sonido. Solo se marca el patrón del compás actual. Con un cursor de paso y un visualizador de la onda es más fácil relacionar la huella con lo que se oye, y ver el efecto de Density, Swing, del kit y de los efectos.

## What Changes

- **Cursor de paso** en la vista ampliada: una columna resaltada recorre el patrón que suena, al compás del audio y con el swing aplicado.
- **Golpe por voz**: el nombre de la voz (kick, snare…) se ilumina un instante cada vez que suena.
- **Visualizador** del sonido de salida, con dos modos que se alternan con un clic: **Onda** (osciloscopio) y **Espectro** (barras de frecuencia). Está en la vista ampliada y en una barra fija al pie de la página mientras suena algo desde la lista.
- Con `prefers-reduced-motion` no hay animación: el visualizador no se dibuja y no hay destellos. El cursor de paso sí se mueve, porque informa de qué suena.
- Solo afecta a la página: ni al plugin, ni al MIDI, ni al sonido.

## Capabilities

### New Capabilities

### Modified Capabilities
- `style-fingerprints`: cursor de paso y visualizador del preview.

## Impact

- `tools/view_styles.py` (plantilla) y `docs/fingerprints.html` regenerado.
- Sin recursos externos y sin cambios en el plugin, en los estilos ni en el MIDI.
