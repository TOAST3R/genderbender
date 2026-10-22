## Why

GenderBender genera patrones de batería perfectamente rectos y, además, dispara cada nota en el offset 0 del bloque en el que detecta el cambio de paso, lo que añade un jitter de hasta un bloque (~11 ms). No hay forma de dar groove (swing) ni de adelantar/atrasar una voz respecto al beat, algo básico en estilos como garage, grime, juke o house que son el foco de los estilos incluidos. Existió un intento previo de swing (`playNoteSwing`, `checkInstrumentSwing`) que quedó como código muerto.

## What Changes

- Nuevo **swing global** estilo MPC (50–75 %) aplicado sobre una rejilla fija de semicorcheas común a todas las voces.
- Nuevo **swing amount por voz** (0–100 %) que escala cuánto sigue cada voz al swing global: `S_voz = 50 + (S_global − 50) · amount / 100`.
- Voces cuyo `Div` no es de semicorcheas (32nds, tresillos…) reciben el swing mediante una deformación temporal lineal a trozos dentro de cada corchea, sin reordenar notas.
- Nuevo **slide por voz** en milisegundos (±30 ms) que desplaza todas las notas de la voz, sumado después del swing; los valores negativos adelantan notas mediante lookahead.
- Nuevo **planificador de eventos** con lookahead y precisión de sample que sustituye al disparo en offset 0: corrige el jitter de bloque y sirve de base para swing y slide.
- Los NoteOff se calculan a partir del tiempo final (swing + slide) para no dejar notas colgadas.
- Cola de eventos ampliada de 32 a 128 entradas, ubicada en memoria que no solape con los arrays de patrones.
- 15 sliders nuevos (52–66); los presets/proyectos existentes cargan con valores neutros (swing 50 %, amount 100 %, slide 0 ms).
- GUI ampliada de 686×369 a ~686×470 con una tira **GROOVE** inferior (knob SWING global + amount y slide por voz); `bg.png` se extiende por script.
- Se elimina el código muerto de swing anterior (`playNoteSwing`, `checkInstrumentSwing`, defaults `*_Swing.val_pos`).
- Cambio de comportamiento perceptible: incluso con swing neutro, las notas pasan a sonar exactamente en la rejilla en vez de con retraso de bloque.

## Capabilities

### New Capabilities
- `groove-swing`: swing global estilo MPC, amount por voz y deformación temporal para rejillas que no son de semicorcheas.
- `voice-slide`: desplazamiento micro-temporal por voz en ms, incluido el adelanto mediante lookahead.
- `note-scheduling`: planificador de eventos MIDI sample-accurate con lookahead, cola de 128 eventos, NoteOff coherentes y manejo de saltos de transporte.
- `groove-gui`: tira GROOVE en la interfaz ampliada, sliders automatizables y persistencia en presets.

### Modified Capabilities
<!-- No existen specs previas en openspec/specs/. -->

## Impact

- `GenderBender/genderbender.jsfx`: declaración de sliders, `@init` (memoria, defaults), `@block` (reescritura del disparo de notas), `@serialize`, `@gfx` (tamaño y nuevos knobs).
- `GenderBender/bg.png`: se regenera más alto (se conserva una copia del original).
- Presets `.preset` existentes: siguen funcionando; los sliders nuevos toman sus valores por defecto.
- Requiere una versión de REAPER que admita más de 64 sliders (se usarán 66).
