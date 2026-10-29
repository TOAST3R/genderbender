## ADDED Requirements

### Requirement: Slider de BPM
La página SHALL ofrecer un slider de BPM de 40 a 240, en la cabecera y en la vista ampliada, sincronizados, con un botón para volver al BPM del estilo. Al pulsar Play en un estilo, el slider SHALL ponerse en el BPM de ese estilo. Si se mueve, el preview SHALL tocar a ese tempo, también los dos estilos de A/B; si no se mueve, cada estilo SHALL sonar a su BPM. Cambiar el BPM mientras suena SHALL mantener la posición en el compás. El MIDI exportado SHALL usar el BPM del slider, con las mismas notas. El permalink SHALL llevar `bpm` cuando difiere del BPM del estilo.

#### Scenario: Volver al BPM del estilo
- **WHEN** suena DETROIT TECHNO 128, se sube el BPM a 140 y se pulsa Play en SALSA 180
- **THEN** el slider pasa a 180 y SALSA 180 suena a 180 BPM

#### Scenario: A/B al mismo tempo
- **WHEN** con A/B entre SALSA 180 y MAMBO 190 se pone el BPM en 150
- **THEN** los compases de los dos estilos suenan a 150 BPM

#### Scenario: MIDI al tempo elegido
- **WHEN** con el BPM en 100 se exporta el MIDI de DETROIT TECHNO 128
- **THEN** el archivo tiene tempo 100 y las mismas notas que el exportado a 128

### Requirement: Escenas animadas por familia
La página SHALL mostrar de fondo una escena animada para cada grupo de kit (909, 808, Acústico, Lo-fi, Hardcore, 80s, Percusión, Chiptune y Otros), dibujada en la propia página sin recursos externos, en claro y en oscuro. La escena SHALL ser la del estilo que suena, también en A/B, con un fundido al cambiar; sin reproducción, la del género del filtro. Mientras suena, la escena SHALL moverse al tempo efectivo y reaccionar a los golpes y a la energía del sonido. Las huellas SHALL dibujarse sobre fondos sólidos. Ninguna escena SHALL producir destellos a pantalla completa ligados al ritmo. Con `prefers-reduced-motion: reduce`, la escena SHALL ser una imagen fija.

#### Scenario: La escena sigue al estilo que suena
- **WHEN** se pulsa Play en DETROIT TECHNO 128 y después en SALSA 180
- **THEN** de fondo se ve primero la escena 909 y después la de Percusión

#### Scenario: Al tempo
- **WHEN** suena un estilo de la escena 80s y se sube el BPM de 110 a 220
- **THEN** la rejilla avanza el doble de rápido

#### Scenario: Movimiento reducido
- **WHEN** con `prefers-reduced-motion: reduce` suena un estilo
- **THEN** la escena se dibuja una vez como imagen fija y no se anima
