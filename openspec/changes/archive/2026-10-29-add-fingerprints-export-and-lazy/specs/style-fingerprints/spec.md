## ADDED Requirements

### Requirement: Render perezoso
La página SHALL crear y pintar los canvas de cada tira solo cuando la tira está en pantalla o a menos de 400 px de ella. El cambio de Density y de tema SHALL repintar solo los canvas ya creados. La vista ampliada SHALL pintarse entera al abrirse.

#### Scenario: Carga
- **WHEN** se abre la página con la ventana arriba del todo
- **THEN** solo existen los canvas de las tiras visibles o cercanas, muchos menos que 9 por estilo

#### Scenario: Scroll
- **WHEN** se baja hasta una familia que no se veía
- **THEN** sus tiras aparecen pintadas con la Density actual

### Requirement: Exportar MIDI
La vista ampliada SHALL tener un botón que descargue `<NOMBRE>.mid`: un MIDI tipo 0 con el tempo del estilo y dos compases de lo que se está oyendo (p4/p5 si es la BASE, o el patrón elegido repetido), con Density y swing aplicados y una nota de 1/32 por paso que suena. Las notas SHALL ser por defecto las del plugin (36 + voz) y, con el interruptor "GM", las de General MIDI (36, 38, 39, 42, 46, 50 y 45). En los navegadores con `DownloadURL`, un asa SHALL permitir arrastrar el mismo archivo fuera de la página.

#### Scenario: Descargar la base
- **WHEN** en la vista ampliada de TRAIN BEAT 110, con Density por defecto, se pulsa ⬇ .mid
- **THEN** se descarga `TRAIN BEAT 110.mid`, a 110 BPM, con 32 notas 37 (snare) y 4 notas 36 (kick) en dos compases

#### Scenario: General MIDI
- **WHEN** se activa "GM" y se descarga el mismo estilo
- **THEN** el snare sale en la nota 38 en lugar de la 37

#### Scenario: Arrastrar
- **WHEN** en Chrome se arrastra el asa ⠿ fuera del navegador
- **THEN** el arrastre lleva `DownloadURL` con tipo `audio/midi` y el nombre `<NOMBRE>.mid`

### Requirement: Enlaces a las fuentes
La vista ampliada SHALL enlazar al `.txt` del estilo en el repositorio de GitHub y, si el estilo tiene fuente en `styles_src/`, a su `.style`.

#### Scenario: Estilo con fuente
- **WHEN** se abre la vista ampliada de SALSA 180
- **THEN** hay enlaces a `drum_styles_v/SALSA 180.txt` y a `styles_src/salsa_180.style`

#### Scenario: Estilo sin fuente
- **WHEN** se abre la vista ampliada de GQOM
- **THEN** solo hay enlace al `.txt`

### Requirement: Permalink
El hash de la URL SHALL guardar el estilo abierto, la Density y el género elegido. Al cargar la página con un hash, la página SHALL aplicar el género, la Density y abrir la vista ampliada del estilo; los valores que no existan SHALL ignorarse.

#### Scenario: Abrir un enlace
- **WHEN** se carga `fingerprints.html#style=SALSA 180&density=120&fam=Latin / Caribbean`
- **THEN** se ve solo la familia Latin / Caribbean, Density está en 120 y la vista ampliada de SALSA 180 está abierta

#### Scenario: Estilo inexistente
- **WHEN** el hash nombra un estilo que no existe
- **THEN** la página carga normal, sin vista ampliada

### Requirement: Density y swing en la vista ampliada
La vista ampliada SHALL tener sus propios controles de Density (0–260) y de swing (50–75), sincronizados con los de la cabecera: moverlos SHALL cambiar lo que suena, lo que se pinta y el MIDI exportado igual que los de la cabecera, y al pulsar Play el control de swing SHALL mostrar el swing de la receta del estilo. El contenido de la página SHALL ir centrado.

#### Scenario: Density desde la vista ampliada
- **WHEN** con la vista ampliada abierta se sube su Density a 200
- **THEN** la Density de la cabecera también vale 200 y las tiras y los patrones ampliados se repintan con ella

#### Scenario: Swing al pulsar Play
- **WHEN** en la vista ampliada de DEEP HOUSE 122 se pulsa el ▶ de un patrón
- **THEN** el swing de la vista ampliada muestra 56
