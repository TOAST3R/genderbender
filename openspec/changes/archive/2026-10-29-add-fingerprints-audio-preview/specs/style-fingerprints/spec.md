## ADDED Requirements

### Requirement: Preview de audio por estilo
Cada estilo de la página SHALL tener un botón Play. Al pulsarlo, la página SHALL tocar en bucle su p4 y su p5, alternando a cada compás, con sonidos sintetizados en el navegador y sin cargar recursos externos, y el botón SHALL pasar a Stop. Solo SHALL sonar un estilo o patrón a la vez. Cada paso SHALL sonar solo si `256 − v < Density`, con el valor actual del slider de Density.

#### Scenario: Play y Stop
- **WHEN** se pulsa Play en un estilo y después Stop
- **THEN** suena su base en bucle hasta pulsar Stop, y el botón vuelve a mostrar Play

#### Scenario: Uno a la vez
- **WHEN** suena un estilo y se pulsa Play en otro
- **THEN** el primero se para, su botón vuelve a Play y suena solo el segundo

#### Scenario: Esc
- **WHEN** suena un estilo, la vista ampliada está cerrada y se pulsa Esc
- **THEN** la reproducción se para

#### Scenario: Density
- **WHEN** suena un estilo y se sube Density de 50 a 255
- **THEN** a partir del paso siguiente suenan también los pasos con valores menores de 255

#### Scenario: Patrón vacío
- **WHEN** se pulsa el ▶ de un patrón vacío en la vista ampliada
- **THEN** no suena ninguna nota

### Requirement: Preview por patrón
La vista ampliada SHALL tener un ▶ por cada patrón p0–p8 que toque ese patrón en bucle, con las mismas reglas de reproducción única, Density y tempo.

#### Scenario: Escuchar el FILL
- **WHEN** se pulsa el ▶ de p8 en la vista ampliada de un estilo
- **THEN** suena en bucle solo p8 de ese estilo

### Requirement: Tempo de cada estilo
La reproducción SHALL usar el BPM del nombre del estilo (su número final de 2 o 3 cifras entre 60 y 220). Si el nombre no lo lleva, SHALL usar el `(bpm)` de su entrada en la tabla "Included styles" del README, y si tampoco, 120. El paso SHALL durar `60 / BPM / 8` segundos, y la página SHALL mostrar el BPM junto al botón Play.

#### Scenario: BPM en el nombre
- **WHEN** se pulsa Play en `DETROIT TECHNO 128`
- **THEN** suena a 128 BPM

#### Scenario: BPM en el README
- **WHEN** el nombre es `101 JUKE` y su entrada en el README es `101 JUKE (160)`
- **THEN** suena a 160 BPM

#### Scenario: Sin BPM
- **WHEN** un estilo no tiene BPM ni en el nombre ni en el README
- **THEN** suena a 120 BPM

### Requirement: Swing del preview
La cabecera SHALL tener un slider de swing de 50 a 75 % que SHALL mover el tiempo de cada paso con la misma deformación por corchea que el plugin (`groove-swing`). Al pulsar Play, el slider SHALL pasar al swing de la receta del estilo (cabecera de su `styles_src/*.style`), y cada voz SHALL usar `S_voz = 50 + (S − 50) × amount / 100` con el amount de la receta (100 % si no lo indica). Los estilos sin fuente SHALL sonar con swing 50.

#### Scenario: Swing del estilo
- **WHEN** se pulsa Play en DEEP HOUSE 122, cuya receta es `swing 56 · amount: hhc 100, resto 0`
- **THEN** el slider pasa a 56, el hhc suena con swing 56 y el resto de voces recto

#### Scenario: Estilo sin fuente
- **WHEN** se pulsa Play en un estilo sin `.style` en `styles_src/`
- **THEN** el slider pasa a 50 y todo suena recto

#### Scenario: Ajuste a mano
- **WHEN** suena un estilo y se mueve el slider de swing
- **THEN** los pasos siguientes usan el valor nuevo, con el mismo amount por voz

#### Scenario: Swing por defecto
- **WHEN** el swing está en 50
- **THEN** todos los pasos caen en la rejilla recta

#### Scenario: Swing a 66
- **WHEN** el swing está en 66
- **THEN** la segunda semicorchea de cada corchea suena a 0,33 negras del inicio de la corchea
