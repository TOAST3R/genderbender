## Context

Un estilo `.txt` contiene 7 voces separadas por `/` (`bdrum, sdrum, clap, hhclosed, hhopen, hitom, lotom`). Cada voz tiene 9 patrones separados por `\t` con el formato `<voz><i>|v0,…,v31`. El archivo termina con un `\t` y sin salto de línea, igual que la salida de `drummermenu.scd`.

Cada patrón son 32 pasos, que con el Div por defecto (índice 4, 8 pasos por negra) equivalen a un compás de 4/4. El plugin alterna p(2n) y p(2n+1) a cada compás, y p8 vale para los dos.

Los valores 0–255 funcionan como prioridad, no como probabilidad: un paso suena si `256 − v < Density`.

Con el pad XY en (0,0) suena p4/p5.

## Goals / Non-Goals

**Goals:**
- Fuentes legibles y diffeables a partir de las que se generan los `.txt` exactos.
- Cinco cumbias con el mismo mapa de pad.

**Non-Goals:**
- Generar `.preset` de SuperCollider.
- Cambiar el mapa XY del plugin.
- Guardar el tempo o el groove dentro del `.txt`, que el formato no admite.

## Decisions

- **Formato fuente (`.style`):**
  - Líneas `#` de comentario. La cabecera lleva `name:` y la receta de groove en comentarios.
  - Bloques `[pN pM …]` que aplican sus líneas a varios patrones. Un bloque posterior sobrescribe las voces que nombra.
  - Líneas `<voz> <cuadrícula>`, con los espacios de la cuadrícula ignorados. 16 caracteres equivalen a semicorcheas (el carácter i va al paso 2i) y 32 a fusas.
  - Escala: `X`=255, `x`=170, `o`=120, `-`=60, `.`=0. También se admite `[n]` para un valor numérico directo, para preservar los valores al decodificar.
  - Las voces admiten alias: `kick`=`bdrum`, `snare`=`sdrum`, `hhc`=`hhclosed`, `hho`=`hhopen`.
- **Validación:** cualquier voz, patrón, carácter o longitud desconocidos provoca un error con número de línea y no se escribe nada.
- **`decode`:** emite un `.style` con una línea de 32 pasos por voz y por patrón no vacío, usando símbolos de la escala cuando el valor coincide y `[n]` en el resto. Así, `build(decode(x)) == x` para cualquier `.txt` bien formado. Tres estilos existentes (`DUBSTEP140`, `TekkChungo` y `RB`) traen patrones corruptos del editor (`bdrum1|i`, `-10.0`); `decode` los rechaza con un error en lugar de inventar un formato para representar basura. Arreglarlos queda fuera de este cambio.
- **Valores = prioridad frente a Density:** con Density por defecto (slider 50) solo suenan los pasos a 255. Por eso lo esencial de cada ritmo (bombo, llamador, guache/güiro/shaker) va en `X`, y los adornos en `x`, `o` o `-`, que entran con Density ≥87, ≥137 y ≥197. Lo descubrió la verificación en REAPER: la primera versión tenía el "chk-chk" del guache en `x` y con los valores por defecto no sonaba.
- **Reparto de patrones:** p4/p5 BASE, p2/p3 ENERGÍA, p6/p7 VARIACIÓN, p0/p1 INTRO y p8 FILL, iguales en los cinco estilos.
- **Python 3 sin dependencias.**

## Risks / Trade-offs

- [Hallazgo, fuera de alcance] `@serialize` del plugin sincroniza `snare_Dens.val_pos=slider14`, pero no `kick_Dens.val_pos=slider9`, y `@block` lee `*_Dens.val_pos`. Con la GUI cerrada, la densidad del kick ignora el slider (y su automatización) y usa el valor por defecto interno, 200. Se deja para un cambio aparte.

- [Riesgo] La interpretación musical puede no convencer. → Mitigación: las fuentes son texto plano y se retocan y regeneran en segundos.
- [Riesgo] Un `.txt` mal formado deja silencio en el plugin sin dar ningún error. → Mitigación: el round-trip con `decode` y la verificación en una instancia aislada de REAPER.
