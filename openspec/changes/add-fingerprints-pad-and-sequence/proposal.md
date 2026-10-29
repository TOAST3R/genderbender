## Why

En la página de huellas solo se oye un patrón (o el par de la BASE) a la vez, pero el plugin no funciona así: el pad XY mezcla cuatro pares de patrones y lo que suena cambia de forma continua al moverlo. Tampoco se puede oír cómo encadena un estilo sus partes, aislar una voz, ni comparar dos estilos seguidos para decidir si se parecen.

## What Changes

- **Pad XY** en la vista ampliada: un cuadrado de −100 a 100 en cada eje que reproduce exactamente la mezcla del plugin (sector según el signo de X e Y, con el mismo orden de condiciones, e interpolación bilineal de los valores de cuatro patrones), y luego la regla de Density. Se arrastra mientras suena. En el centro suena la BASE.
- **Secuencia**: un botón que toca INTRO (p0/p1) → BASE (p4/p5) → ENERGÍA (p2/p3) → VARIACIÓN (p6/p7) → FILL (p8) en bucle, saltando los patrones vacíos.
- **Mute / solo por voz** en la vista ampliada, para el preview y para el MIDI.
- **A/B**: elegir un segundo estilo y alternar los dos cada dos compases.
- El MIDI de `add-fingerprints-export-and-lazy` exporta también la mezcla del pad y respeta mute/solo.

## Capabilities

### New Capabilities

### Modified Capabilities
- `style-fingerprints`: pad XY con la fórmula del plugin, secuencia, mute/solo y A/B.

## Impact

- `tools/view_styles.py` (plantilla y script) y `docs/fingerprints.html` regenerado.
- **Depende de `add-fingerprints-export-and-lazy`** (render perezoso y exportación MIDI): se aplica después.
- Sin cambios en el plugin ni en los estilos.
