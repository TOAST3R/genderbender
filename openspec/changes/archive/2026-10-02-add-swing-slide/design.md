## Context

`genderbender.jsfx` es un generador MIDI de 7 voces (kick, snare, clap, hh cerrado, hh abierto, tom alto, tom bajo). Cada voz lee un patrón de 32 pasos con probabilidades 0–255, interpolado entre 4 de 9 patrones con el pad XY (`sector`, `Xmap`, `Ymap`).

Estado actual del disparo de notas (`@block`):

- `beats[i] = (beat_position * divs[i]) % 32`, con `divs = {1,1,2,4,8,12,16,24,32,16,12}` pasos por negra. El `Div` de cada voz (sliders 10, 15, 20…) es un índice en `divs`.
- Cuando `beats[i]` cambia respecto al bloque anterior, se evalúa la voz (`xxdrumFunc` + `checkInstrument` / `checkInstrumentBreak`) y `playNote` hace `midisend(0, NoteOn)`. La nota sale en el offset 0 del bloque en el que se detecta el paso, es decir, tarde (entre 0 y 1 bloque).
- NoteOff: `noteOffTimes[n] = curbeatposNew1 + dur`, en ticks de `1/(ts_num*16)` negras. Al final del bloque se recorre la cola de 32 entradas y se envía NoteOff en offset 0.
- Hay código muerto de un swing anterior: `playNoteSwing` y `checkInstrumentSwing` (nunca llamadas, usan la variable `even`, que nunca se define), los defaults `*_Swing.val_pos` y una rama de NoteOn retrasado comentada en el bucle de la cola.
- **Bug de memoria preexistente:** `lotom = 1900` ocupa 1900–2187 y se solapa con `noteTimes = 2100` (2100–2131). Escribir la cola corrompe los patrones 6 y 7 del tom bajo.
- GUI: `@gfx 686 369`, fondo `bg.png` sin archivo fuente y sin hueco libre. Los knobs son `draw_pot_automate` (interacción de ratón) más `drawmeter` (dibujo). El `gfxindex 4` no tiene imagen cargada, así que lo único visible es el meter.

## Goals / Non-Goals

**Goals:**
- Swing global estilo MPC con amount por voz, aplicado sobre una rejilla común de semicorcheas.
- Slide por voz en ms, positivo y negativo.
- Notas sample-accurate (sin jitter de bloque), aunque el swing esté a 50 %.
- Sin notas colgadas en ningún caso (Duration mínima, saltos de loop, stop).
- Compatibilidad con presets y proyectos existentes, que deben sonar igual en patrón (y solo cambiar en precisión de timing).

**Non-Goals:**
- Humanize aleatorio de timing o velocidad.
- Swing con otras rejillas (8ths, 32nds) como base seleccionable.
- Rediseñar la GUI existente o regenerar el arte del personaje.
- Refactorizar las funciones `xxdrumFunc` duplicadas por voz.

## Decisions

### D1. Planificador con lookahead en lugar de detección de cambio de paso

En cada bloque:

```
b0 = beat_position
bpb = tempo / 60 / srate                 // negras por sample
b1 = b0 + samplesblock * bpb             // fin del bloque
la = SLIDE_MAX_MS/1000 * tempo/60        // lookahead en negras (30 ms)

para cada voz v (div = divs[Div_v]):
  mientras (k = last_k[v] + 1) / div <= b1 + la:
      t_straight = k / div
      evaluar paso: pos = k % 32, morph XY, break (calculado con t_straight), probabilidad
      si suena: t = warp(t_straight, S_v) + slide_v_ms/1000 * tempo/60
                encolar NoteOn(t) y NoteOff(t + dur/(ts_num*16))
      last_k[v] = k

para cada evento con t < b1 (ordenados por t):
  offset = clamp(floor((t - b0) / bpb), 0, samplesblock-1)
  midisend(offset, …)
```

- Por qué: el disparo en offset 0 no permite ni retrasar ni adelantar con precisión. Una cola temporal resuelve a la vez el jitter, el swing y el slide.
- Alternativa descartada: mantener la detección actual y solo retrasar los pasos impares. El jitter de bloque se sumaría al swing y el slide negativo sería imposible.
- Alternativa descartada: usar `pdc_delay` para el slide negativo. Añade latencia a toda la pista y complica la monitorización.
- Las voces cuyo `Div` está en modo break usan su índice de break; `compases` se calcula a partir de `t_straight` del paso, no de `beat_position` del bloque.
- `Div = 0` (índice 0 en `divs`, valor 1) sigue el mismo flujo. Un `Div` de valor 0 no existe en `divs`.

### D2. Swing como deformación lineal a trozos de cada corchea

Sea `u` la posición dentro de la corchea, con `u = frac(t*2)/2 ∈ [0, 0.5)`, y `p = S/100 * 0.5` la nueva posición de la segunda semicorchea:

```
warp(u) = u < 0.25 ?  u * (p / 0.25)
                   :  p + (u - 0.25) * ((0.5 - p) / 0.25)
```

- Con Div 4 (semicorcheas) el resultado es idéntico al swing de un MPC. Con Div 1 y 2 las notas caen en los bordes de la corchea y no cambian. Con 32nds y tresillos el tiempo se deforma de forma monótona, así que nunca se reordenan las notas.
- Alternativa descartada: mover solo los pasos que caen en semicorcheas impares. Con 32nds podría hacer colisionar o cruzar notas, y los tresillos ignorarían el swing.

### D3. Combinación global × amount

`S_v = 50 + (S_global − 50) * amount_v / 100`, con `S_global ∈ [50, 75]` y `amount_v ∈ [0, 100]` (100 por defecto). Así un solo knob controla el groove y cada voz decide cuánto lo sigue.

### D4. Slide en ms, rango ±30, sumado tras el swing

- Se convierte a negras con el tempo del bloque.
- El lookahead `la` cubre el peor caso de adelanto (−30 ms).
- Tras un salto de transporte, los pasos cuyo tiempo final quedaría antes de `b0` se emiten en el offset 0, es decir, en su sitio en lugar de adelantados.

### D5. Cola de eventos de 128 entradas en memoria propia

- Arrays paralelos `evTime`, `evType` (on/off), `evNote` y `evVel`, en una zona libre (por ejemplo a partir de 20000), sin solaparse con patrones, `beats` (3000), `divs` (5000) ni cadenas.
- Si la cola se llena, se descarta el NoteOn nuevo (nunca un NoteOff pendiente).
- `last_k[7]` también va en memoria propia.
- Se retiran `noteTimes` y `noteOffTimes`, cuya zona solapada es la causa del bug de `lotom`.

### D6. Coherencia de NoteOff

- El NoteOff se programa en `t_on + dur` (dur en ticks `1/(ts_num*16)` de negra), así que siempre llega después de su NoteOn.
- Al emitir un NoteOn de una nota que ya tiene un NoteOff pendiente, primero se emite ese NoteOff en el mismo offset y se borra de la cola. Así se evita que un NoteOff antiguo corte la nota nueva.

### D7. Transporte

- Se detecta un salto cuando `b0 < last_b1 − ε` o `b0 > last_b1 + la + ε`, y también al pasar de stop a play.
- Al saltar: se emiten de inmediato todos los NoteOff pendientes de notas que ya sonaron, se descartan los NoteOn pendientes y se reanuda la evaluación desde `b0` (en la implementación hay un único horizonte de evaluación `evalHorizon` compartido por todas las voces y rejillas, en lugar de un `last_k` por voz; así un cambio de `Div` en plena reproducción no duplica ni salta pasos).
- **Slide negativo en loops:** antes del salto, una voz puede haber adelantado el paso que cae justo en el final del loop. Si una voz emitió un NoteOn cuyo tiempo recto es mayor o igual que el punto de salto, se omite su paso en la nueva posición `b0`. Así el inicio del loop suena adelantado y una sola vez.
- **Guarda de medio sample:** solo se emiten los eventos con `t < b1 − ½ sample`. Un paso que cae exactamente en el final de un loop (por redondeo, en el último sample del bloque) pasa al bloque siguiente y se descarta con el salto.
- En stop: se vacía la cola enviando sus NoteOff y se mantiene el reset actual de posiciones.

### D8. Sliders y persistencia

| Slider | Nombre | Rango | Defecto |
|---|---|---|---|
| 52 | `-swing` | 50–75, paso 1 | 50 |
| 53–59 | `-kick_swingamt` … `-lotom_swingamt` | 0–100 | 100 |
| 60–66 | `-kick_slide` … `-lotom_slide` (ms) | −30–30 | 0 |

- Los nombres empiezan por `-` (ocultos en la UI genérica), igual que los demás.
- `@serialize` añade los `val_pos` nuevos **al final** del bloque `file_var` existente.

### D9. GUI: tira GROOVE inferior

- `@gfx 686 486` (la tira necesita ~110 px para el meter, el valor y las etiquetas).
- `bg.png` se regenera con un script (Python + Pillow): se copia el original arriba y se rellenan los ~101 px inferiores con una franja de madera tomada del propio PNG (por ejemplo, espejando una banda sin personaje), más un panel oscuro semitransparente del mismo estilo que los existentes.
- El original se conserva como `bg_original.png`. El script vive en `tools/extend_bg.py` y regenera el fondo a partir de ese original.
- Contenido de la tira: el knob `SWING` global a la izquierda y, a la derecha, 7 columnas (KICK, SNR, CLAP, HHC, HHO, HIT, LOT), cada una con `AMT` y `SLIDE`. Mismo patrón `draw_pot_automate` + `drawmeter` / `drawmeterMap`.
- Las etiquetas se dibujan en tiempo de ejecución con `gfx_drawstr` horizontal, en el mismo color gris, porque no se puede rotar texto como en el PNG.

### D10. Limpieza

Se eliminan `playNoteSwing`, `checkInstrumentSwing`, los defaults `*_Swing.val_pos` y la rama de NoteOn comentada. `playNote` desaparece: lo sustituye el encolado.

## Risks / Trade-offs

- [Riesgo] Cambios de tempo dentro de la ventana de lookahead hacen que eventos ya encolados en negras se emitan con un error mínimo. → Mitigación: la conversión a offset se hace en el bloque de emisión con el tempo actual, así que el error se limita a ~30 ms × Δtempo, que es despreciable.
- [Riesgo] La probabilidad y el morph XY se evalúan hasta 30 ms antes. Mover el pad justo en el borde puede no reflejarse en ese paso. → Mitigación: aceptable, es imperceptible.
- [Riesgo] Hay un cambio audible en proyectos existentes por la corrección del jitter. → Mitigación: el patrón no cambia, solo la precisión. Se documenta en el changelog o versión.
- [Riesgo] Rangos de `Div` muy altos (32 pasos por negra) con las 7 voces pueden saturar la cola de 128. → Mitigación: el peor caso es 7 × 32 × ~(bloque + 30 ms) pasos, muy por debajo de 128 a tempos normales. El descarte de NoteOn evita corrupción.
- [Riesgo] El planificador asume que REAPER corta el bloque de audio en el punto de loop, de modo que ningún bloque cruza el final del loop. Si un bloque lo cruzara, el paso del final del loop sonaría dentro de ese bloque y el del inicio sonaría después del salto, lo que daría un golpe doble por vuelta. Así lo muestra la simulación. → Mitigación: se verifica en REAPER (tarea 6.5). Si aparece el doble, habría que limitar la emisión al principio del bloque siguiente.
- [Riesgo] Un REAPER antiguo (64 sliders o menos) no cargaría los sliders 65 y 66. → Mitigación: se requiere el REAPER actual, que es la decisión del usuario.
- [Trade-off] Las etiquetas de la tira GROOVE son texto horizontal, no rotado como en el resto. Es aceptable y no requiere el archivo fuente del fondo.

## Migration Plan

- Copia de seguridad de `genderbender.jsfx` y `bg.png` antes de modificarlos.
- Los presets existentes cargan con swing 50, amount 100 y slide 0. Suenan como antes salvo por el timing, que ahora es más preciso.
- Rollback: restaurar los dos archivos.

## Open Questions

- Ninguna bloqueante. Se podrá ajustar a oído si `SLIDE_MAX_MS = 30` resulta corto.
