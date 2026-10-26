## Why

Density decide qué pasos suenan (`256 − v < Density`), así que el número de niveles de valor marca cuántos escalones de densidad tiene un estilo. Los estilos antiguos usan solo 3 niveles (255/170/85), y la escala del formato `.style` (`X=255 x=170 o=120 -=60`) está espaciada de forma irregular. Una escala de 5 niveles equiespaciados da escalones regulares de Density para los estilos nuevos.

## What Changes

- **BREAKING (formato `.style`)**: la escala de `tools/make_style.py` pasa a 5 niveles equiespaciados: `X=255 x=204 o=153 -=102 ,=51 .=0`. Cada nivel entra con Density >1, >52, >103, >154 y >205. `,` es un símbolo nuevo.
- `[n]` se sigue admitiendo para valores exactos.
- **BREAKING (decode)**: `decode` ajusta cada valor al nivel más cercano de la escala en vez de emitir `[n]`, así que deja de garantizar el round-trip byte a byte.
- Los `.txt` existentes de `drum_styles_v/`, tanto los antiguos como las cumbias, no se reescriben. Sus fuentes `styles_src/*.style` se pasan a valores exactos `[n]` para que al reconstruirlas sigan dando el mismo `.txt`.
- Sin cambios en el plugin: `genderbender.jsfx` ya acepta cualquier valor de 0 a 255.

## Capabilities

### New Capabilities

### Modified Capabilities
- `style-authoring`: nueva escala de 5 niveles con el símbolo `,`, y `decode` ajusta al nivel más cercano en lugar de garantizar el round-trip exacto.

## Impact

- `tools/make_style.py`: escala, docstring y `to_style`.
- `styles_src/*.style`: las cinco cumbias, de `x/o/-` a `[170]/[120]/[60]`, con la cabecera de escala actualizada.
- `drum_styles_v/*.txt`: sin cambios.
- Requisito previo: archivar `add-cumbia-styles` para que `style-authoring` exista en `openspec/specs/`.
