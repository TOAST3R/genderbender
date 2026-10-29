## ADDED Requirements

### Requirement: Samples propios por voz
En la vista ampliada, cada voz SHALL poder usar un archivo de audio elegido por el usuario en su equipo (con un botón o soltándolo sobre el nombre de la voz) en lugar del sonido del kit, con una ganancia propia, y SHALL poder volver al kit. Las voces sin sample SHALL seguir sonando con el kit. El volumen de cada golpe SHALL seguir el valor del paso. Los samples SHALL guardarse solo en el navegador (IndexedDB) y seguir cargados al volver a la página; no SHALL enviarse a ningún sitio. Cuando hay samples propios, la página SHALL indicarlo.

#### Scenario: Cambiar el bombo
- **WHEN** se carga un WAV en la voz kick y se pulsa Play
- **THEN** el bombo suena con ese WAV y el resto de voces con el kit

#### Scenario: Recordado al recargar
- **WHEN** se carga un sample, se recarga la página y se pulsa Play
- **THEN** la voz sigue sonando con ese sample

#### Scenario: Archivo no válido
- **WHEN** se elige un archivo que no es audio
- **THEN** la página avisa y la voz sigue como estaba

### Requirement: Exportar WAV
La vista ampliada SHALL exportar a WAV (16 bits, 44,1 kHz, estéreo) lo que se oye con los ajustes actuales (Density, Swing, BPM, kit o samples, mute/solo y efectos): cada parte repetida 1, 2, 4 u 8 compases, la secuencia completa, y todas las partes no vacías en un ZIP. Cada parte SHALL poder arrastrarse como WAV al escritorio o al DAW. Con "colas envueltas" (activado por defecto), la cola de los efectos SHALL sumarse al principio para que el loop empalme. La duración SHALL ser exactamente la de los compases al BPM efectivo.

#### Scenario: Parte en loop
- **WHEN** se exporta p4 de DETROIT TECHNO 128 a 2 compases
- **THEN** el WAV dura 2 × 240 / 128 = 3,75 s (165 375 muestras) y empieza y acaba sin salto

#### Scenario: Todas las partes
- **WHEN** se pulsa "todas las partes" en un estilo con FILL vacío
- **THEN** se descarga un ZIP con un WAV por cada parte no vacía y ninguno para el FILL

#### Scenario: Arrastrar
- **WHEN** se arrastra el asa WAV de p5 a una pista de REAPER
- **THEN** REAPER recibe el WAV de p5 con los ajustes actuales
