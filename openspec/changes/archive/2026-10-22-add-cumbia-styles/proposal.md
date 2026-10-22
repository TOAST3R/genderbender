## Why

GenderBender no tiene ningún estilo de cumbia, a pesar de cubrir otros géneros bailables latinos y de club (reggaetón, juke, gqom…). Además, los estilos solo se pueden crear con el editor de SuperCollider, cuyo formato `.txt` no es legible ni versionable a mano.

## What Changes

- Cinco estilos nuevos en `drum_styles_v/`, uno por sub-género y con el tempo en el nombre: `CUMBIA COLOMBIANA 95`, `CUMBIA SONIDERA 92`, `CUMBIA VILLERA 98`, `CUMBIA DIGITAL 100` y `CUMBIA REBAJADA 72`.
- Los cinco comparten el mismo reparto de patrones en el pad XY: p4/p5 BASE (centro, por defecto), p2/p3 ENERGÍA, p6/p7 VARIACIÓN, p0/p1 INTRO y p8 FILL.
- Archivos fuente legibles en `styles_src/*.style`, con una cuadrícula por voz y patrón, y una receta de groove (swing y slide) como comentario.
- Nueva herramienta `tools/make_style.py`:
  - `build` genera el `.txt` con el formato exacto del editor.
  - `decode` convierte cualquier `.txt` en una cuadrícula legible.
  - Valida la entrada.
- Sin cambios en el plugin.

## Capabilities

### New Capabilities
- `style-authoring`: formato fuente de estilos y herramienta para generar y decodificar los `.txt` del plugin.
- `cumbia-styles`: los cinco estilos de cumbia y su reparto común de patrones.

### Modified Capabilities

## Impact

- Archivos nuevos: `tools/make_style.py`, `styles_src/*.style` y `drum_styles_v/CUMBIA *.txt`.
- No se toca `genderbender.jsfx` ni el editor de SuperCollider. Los estilos de cumbia no tendrán `.preset` para ese editor.
