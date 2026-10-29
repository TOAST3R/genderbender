## Why

GenderBender solo tiene dos estilos de drum & bass genéricos (`drumbass`, `DurumBass160`), hechos con el editor de SuperCollider y sin fuente legible. Faltan los sub-géneros que tienen una gramática de batería propia: el breakbeat troceado del jungle, el two-step seco del techstep o el snare en el 3 del halftime.

## What Changes

- Siete estilos nuevos en `drum_styles_v/`, con el tempo sugerido en el nombre: `JUNGLE 165`, `RAGGA JUNGLE 165`, `HARDSTEP 172`, `JUMP-UP 174`, `DANCEFLOOR DNB 174`, `TECHSTEP 172` y `HALFTIME 174`.
- Fuentes legibles en `styles_src/*.style`, escritas con la escala de 5 niveles (`X x o - ,`) de `five-level-density-scale`, cada una con su receta de groove (swing y slide) en un comentario.
- Mismo reparto de patrones en el pad que las cumbias: p4/p5 BASE, p2/p3 ENERGÍA, p6/p7 VARIACIÓN, p0/p1 INTRO y p8 FILL.
- README: tabla de estilos incluidos y recuento actualizados.
- Sin cambios en el plugin ni en `tools/`. `drumbass` y `DurumBass160` no se tocan.

## Capabilities

### New Capabilities
- `dnb-styles`: los siete estilos de drum & bass, su reparto de patrones y el ritmo que define cada sub-género.

### Modified Capabilities

## Impact

- Archivos nuevos: `styles_src/<estilo>.style` (7) y `drum_styles_v/<ESTILO>.txt` (7).
- `README.md`: sección "Included styles".
- **Depende de `five-level-density-scale`**: debe aplicarse antes, porque las fuentes usan los valores nuevos de `x o -` y el símbolo `,`. Con la escala antigua, `make_style.py build` rechazaría `,` y los adornos entrarían con otros umbrales de Density.
- Fuera de alcance: el resto de sub-géneros comentados (Liquid, Jazzstep, Footwork Jungle, Crossbreed, Neurofunk, Darkstep, Synthwave DnB), las notas fantasma con velocidad propia (el plugin usa una velocidad fija por voz) y exportar los presets `DURUMBASS_160` y `DURUMBREAK_160`.
