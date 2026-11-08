# melo-midi-output Specification

## Purpose
Define cómo GenderBender Melo envía bajo, acordes y melodía a destinos MIDI independientes, con timing exacto, legato correcto y sin notas colgadas.

## Requirements

### Requirement: Modo de salida
Un selector SHALL elegir entre salida por canal MIDI y salida por bus MIDI de REAPER. En modo canal, todo SHALL salir por el bus 1. En modo bus, cada voz SHALL salir por su propio bus, en el canal 1.

#### Scenario: Modo canal por defecto
- **WHEN** se inserta el plugin sin tocar nada
- **THEN** el bajo sale por el canal 1, los acordes por el 2 y la melodía por el 3, todo en el bus 1

#### Scenario: Modo bus
- **WHEN** el modo es bus
- **THEN** el bajo sale por el bus 1, los acordes por el 2 y la melodía por el 3

### Requirement: Destino configurable por voz
Cada voz SHALL tener un control de destino (canal 1–16 o bus 1–16, según el modo).

#### Scenario: Bajo y melodía al mismo canal
- **WHEN** el bajo y la melodía tienen el canal 5
- **THEN** las notas de ambas voces salen por el canal 5

### Requirement: Acordes partidos
La voz de acordes SHALL poder salir polifónica por un único destino o partida. En modo partido, la nota n del acorde (de grave a agudo) SHALL salir por el destino base + n.

#### Scenario: Triada partida
- **WHEN** los acordes están partidos con destino base 4 y suena una triada
- **THEN** la nota grave sale por el destino 4, la media por el 5 y la aguda por el 6

#### Scenario: Destino fuera de rango
- **WHEN** el destino base + n pasa de 16
- **THEN** esa nota sale por el destino 16

### Requirement: Emisión sample-accurate
Cada NoteOn y NoteOff SHALL emitirse con el offset de sample de su tiempo programado (incluidos swing, slide y strum), como en la spec note-scheduling de gb_18.

#### Scenario: Nota en mitad de bloque
- **WHEN** el tiempo programado de una nota cae a 300 samples del inicio de un bloque
- **THEN** el NoteOn se envía con offset 300

### Requirement: Legato y slide
En un paso ligado o con slide de una voz monofónica, el NoteOn de la nota nueva SHALL enviarse antes del NoteOff de la anterior. En un paso con slide SHALL activarse además el portamento (CC 65) para esa nota.

#### Scenario: Slide en el bajo
- **WHEN** el bajo pasa de A a C con slide
- **THEN** el MIDI grabado muestra el NoteOn de C antes del NoteOff de A, con CC 65 activo durante el paso

### Requirement: Sin notas colgadas
Al parar, hacer seek o volver al inicio de un loop, el plugin SHALL enviar el NoteOff de todas las notas que estén sonando en todos los destinos y descartar los NoteOn pendientes. Si una voz cambia de destino, SHALL cerrar sus notas en el destino anterior.

#### Scenario: Stop con acordes sonando
- **WHEN** se detiene el transporte con un acorde partido sonando en tres canales
- **THEN** cada canal recibe el NoteOff de su nota

#### Scenario: Re-disparo de la misma nota
- **WHEN** suena un NoteOn de una nota que todavía tiene un NoteOff pendiente en el mismo destino
- **THEN** ese NoteOff se envía justo antes del nuevo NoteOn

### Requirement: Cola con prioridad de NoteOff
Si la cola de eventos se llena, SHALL descartarse el NoteOn nuevo y nunca un NoteOff pendiente.

#### Scenario: Cola llena
- **WHEN** la cola está llena y llega un NoteOn
- **THEN** el NoteOn se descarta y los NoteOff pendientes se emiten normalmente
