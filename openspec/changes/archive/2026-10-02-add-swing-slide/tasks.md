## 1. Preparación

- [x] 1.1 Copiar `GenderBender/genderbender.jsfx` y `GenderBender/bg.png` a copias de respaldo (`backup/`, fuera de la carpeta del plugin)
- [x] 1.2 Inventariar la memoria usada en `@init` (patrones 100–2187, `beats` 3000, `oldbeats` 3100, `divs` 5000…) y fijar la nueva zona libre para la cola y `last_k` (por ejemplo, desde 20000)

## 2. Sliders y parámetros

- [x] 2.1 Declarar el slider 52 (`-swing` 50–75, por defecto 50), los sliders 53–59 (`-<voz>_swingamt` 0–100, por defecto 100) y los sliders 60–66 (`-<voz>_slide` −30–30, por defecto 0)
- [x] 2.2 Añadir en `@init` los defaults de los `val_pos` nuevos (swing, amounts, slides)
- [x] 2.3 Añadir los `file_var` de los `val_pos` nuevos al final del bloque `file_var` de `@serialize`
- [x] 2.4 Eliminar el código muerto: `playNoteSwing`, `checkInstrumentSwing`, los defaults `*_Swing.val_pos` y la rama de NoteOn comentada

## 3. Planificador de eventos

- [x] 3.1 Crear la cola de 128 eventos (`evTime`, `evType`, `evNote`, `evVel`) con funciones para encolar (descartando el NoteOn si la cola está llena) y retirar
- [x] 3.2 Implementar la emisión por bloque: para cada evento con `t < b1`, calcular `offset = clamp(floor((t-b0)/bpb), 0, samplesblock-1)` y llamar a `midisend` en orden temporal
- [x] 3.3 Implementar el re-disparo: antes de un NoteOn, emitir y retirar el NoteOff pendiente de esa nota
- [x] 3.4 Sustituir la detección `beats[i] != oldbeats[i]` por la evaluación de pasos `k` con `k/div` en `(last_k, b1 + lookahead]` para cada voz, respetando la selección Div normal o Div break
- [x] 3.5 Refactorizar `checkInstrument` y `checkInstrumentBreak` para que devuelvan si el paso suena en vez de llamar a `playNote`, y calcular `compases` y `secondBar` desde el tiempo recto del paso
- [x] 3.6 Programar el NoteOff en `t_on + dur/(ts_num*16)` y eliminar `noteTimes`, `noteOffTimes` y la cola antigua de 32 entradas (corrige el solape con `lotom`)
- [x] 3.7 Detectar saltos de transporte y el paso de stop a play: emitir los NoteOff pendientes, descartar los NoteOn y reinicializar `last_k[v] = ceil(b0*div)-1`
- [x] 3.8 En stop, vaciar la cola enviando sus NoteOff (mantener el reset de posiciones actual)

## 4. Swing y slide

- [x] 4.1 Implementar `warp(t, S)`: deformación lineal a trozos de cada corchea con `p = S/100*0.5`
- [x] 4.2 Calcular `S_v = 50 + (S_global-50)*amount_v/100` por voz y aplicarlo a las notas normales y de break
- [x] 4.3 Aplicar el slide: `t = warp(t_recto, S_v) + slide_ms/1000*tempo/60`, con un lookahead de 30 ms en negras

## 5. GUI

- [x] 5.1 Escribir un script (Python + Pillow) que genere un `bg.png` de 686×470: el original arriba y, abajo, una franja de madera tomada del propio PNG con un panel oscuro del mismo estilo
- [x] 5.2 Cambiar `@gfx 686 369` a `@gfx 686 470`
- [x] 5.3 Dibujar la tira GROOVE: el knob SWING global y 7 columnas con AMT y SLIDE (`draw_pot_automate` + `drawmeter`/`drawmeterMap`), sincronizando slider ↔ `val_pos` como los knobs existentes
- [x] 5.4 Dibujar las etiquetas (GROOVE, SWING, nombres de voz, AMT, SLIDE) con `gfx_drawstr` en el gris de las etiquetas existentes
- [x] 5.5 Fijar el `reset_val` de cada knob nuevo a su valor por defecto (50, 100 o 0)

## 6. Verificación en REAPER

- [x] 6.1 Cargar el plugin sin errores de compilación y comprobar que los 66 sliders aparecen en la lista de automatización
- [x] 6.2 Con swing 50, slides 0 y un preset existente, grabar el MIDI de salida y verificar que las notas caen exactamente en la rejilla y que el patrón coincide con el original
- [x] 6.3 Con swing 75 y Div de semicorcheas, verificar sobre el MIDI grabado que los pasos impares se desplazan 0.125 negras; con amount 0, que no se desplazan
- [x] 6.4 Verificar los Div de 32nds y tresillos con swing (sin reordenar notas) y los Div 1 y 2 (sin cambios)
- [x] 6.5 Verificar slide +20 ms y −15 ms medido en el MIDI grabado, incluido el primer paso tras una vuelta de loop
- [x] 6.6 Verificar que no quedan notas colgadas con Duration 1 y swing máximo, con loops, seek y stop
- [x] 6.7 Verificar que los patrones del tom bajo (6 y 7) ya no se corrompen durante la reproducción
- [x] 6.8 Guardar y recargar un proyecto con valores GROOVE no neutros, y cargar un `.preset` antiguo para comprobar los defaults
