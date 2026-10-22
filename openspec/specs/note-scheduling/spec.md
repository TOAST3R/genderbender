# note-scheduling Specification

## Purpose
TBD - created by archiving change add-swing-slide. Update Purpose after archive.
## Requirements
### Requirement: Emisión sample-accurate
Cada NoteOn y NoteOff SHALL emitirse con un offset de sample dentro del bloque calculado a partir de su tiempo programado en negras, no en el offset 0 del bloque en el que se detecta el paso.

#### Scenario: Nota en mitad de un bloque
- **WHEN** el tiempo programado de una nota cae a 300 samples del inicio de un bloque de 512
- **THEN** el NoteOn se envía con offset 300

#### Scenario: Sin swing ni slide
- **WHEN** el swing global vale 50 % y todos los slides valen 0
- **THEN** cada nota suena en el sample exacto de su paso de rejilla, sin el retraso de hasta un bloque del comportamiento anterior

### Requirement: Patrón inalterado
Para cada paso, la selección de posición (`k % 32`), el morph XY, la lógica de break y la probabilidad SHALL producir el mismo resultado que el comportamiento anterior. La lógica de break SHALL calcularse a partir del tiempo recto del paso.

#### Scenario: Mismo preset, mismo patrón
- **WHEN** se carga un preset existente con swing neutro
- **THEN** los pasos que pueden sonar y sus probabilidades son los mismos que antes del cambio

### Requirement: NoteOff coherentes
El NoteOff de cada nota SHALL programarse a partir del tiempo final de su NoteOn (con swing y slide) más la duración en ticks de `1/(ts_num×16)` negras. Ninguna nota SHALL quedar colgada.

#### Scenario: Duración mínima con swing
- **WHEN** la duración vale 1 tick y la nota se retrasa por swing más de 1 tick
- **THEN** el NoteOff se envía después de su NoteOn

#### Scenario: Re-disparo de la misma nota
- **WHEN** se emite un NoteOn de una nota que todavía tiene un NoteOff pendiente
- **THEN** ese NoteOff pendiente se envía justo antes del nuevo NoteOn y se retira de la cola

### Requirement: Cola de eventos de 128 entradas
Los eventos programados SHALL almacenarse en una cola de 128 entradas, en memoria que no se solape con los arrays de patrones ni con otros buffers. Si la cola está llena, SHALL descartarse el NoteOn nuevo y nunca un NoteOff pendiente.

#### Scenario: Patrones del tom bajo intactos
- **WHEN** el plugin reproduce durante varios compases con todas las voces activas
- **THEN** los 9 patrones del tom bajo conservan los valores cargados del estilo

#### Scenario: Cola llena
- **WHEN** la cola tiene 128 eventos pendientes y llega un nuevo NoteOn
- **THEN** el NoteOn se descarta y los NoteOff pendientes se emiten normalmente

### Requirement: Manejo de transporte
Al detectar un salto de transporte (loop, seek o paso de stop a play), el plugin SHALL emitir de inmediato los NoteOff de las notas que ya sonaron, descartar los NoteOn pendientes y reanudar la evaluación de pasos desde la nueva posición. Al pasar a stop SHALL vaciar la cola enviando sus NoteOff.

#### Scenario: Vuelta de loop
- **WHEN** el transporte vuelve del final al inicio de un loop
- **THEN** no quedan notas colgadas y el primer paso del loop suena

#### Scenario: Stop
- **WHEN** se detiene el transporte con notas sonando
- **THEN** todas reciben su NoteOff

