## ADDED Requirements

### Requirement: Efectos globales del preview
La página SHALL ofrecer tres knobs de efectos globales para el preview (Distortion, Delay y Reverb, de 0 a 100), en la cabecera y en la vista ampliada, sincronizados, sin cargar recursos externos. Con los tres a 0 el sonido SHALL ser el mismo que sin efectos. El tiempo del delay SHALL seguir al BPM del estilo que suena, también en A/B. Los knobs SHALL poder moverse mientras suena sin parar la reproducción. Los efectos SHALL afectar solo al sonido de la página, no al MIDI exportado.

#### Scenario: Mover un knob mientras suena
- **WHEN** suena un estilo y se sube Reverb de 0 a 60
- **THEN** la reproducción sigue sin pararse y los golpes siguientes suenan con reverb

#### Scenario: Delay sincronizado
- **WHEN** con Delay por encima de 0 se toca A/B entre SALSA 180 y MAMBO 190
- **THEN** el eco dura una corchea con puntillo a 180 BPM en los compases de SALSA 180 y a 190 BPM en los de MAMBO 190

#### Scenario: El MIDI no cambia
- **WHEN** se exporta el MIDI de un estilo con los efectos a 0 y con los efectos a 100
- **THEN** los dos archivos son idénticos

### Requirement: Efectos recordados y en el permalink
Los valores de los knobs SHALL guardarse en el navegador y en los parámetros `dist`, `dly` y `rev` del permalink, que solo se escriben cuando no son 0; al cargar la página, el permalink SHALL tener prioridad sobre lo guardado.

#### Scenario: Permalink con efectos
- **WHEN** se carga `fingerprints.html#rev=40&dly=25`
- **THEN** Reverb está en 40, Delay en 25 y Distortion en 0, aunque en el navegador hubiera otros valores guardados
