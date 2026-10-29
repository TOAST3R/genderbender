## ADDED Requirements

### Requirement: Cuarenta y dos estilos de techno, house, hardcore, psytrance, hard house, EBM, rave y drill and bass con tempo
`drum_styles_v/` SHALL incluir `DETROIT TECHNO 128.txt`, `MINIMAL TECHNO 126.txt`, `HARD TECHNO 145.txt`, `ACID TECHNO 140.txt`, `UK TECHNO 135.txt`, `DEEP HOUSE 122.txt`, `TECH HOUSE 126.txt`, `GHETTOTECH 150.txt`, `ACID HOUSE 124.txt`, `ITALO HOUSE 122.txt`, `GABBER 180.txt`, `GABBER ROLL 180.txt`, `HAPPY HARDCORE 170.txt`, `GOA TRANCE 145.txt`, `FULL-ON 145.txt`, `PROGRESSIVE PSY 138.txt`, `DARK PSY 150.txt`, `FOREST PSY 150.txt`, `PSYCORE 190.txt`, `ZENONESQUE 135.txt`, `MINIMAL PSY 140.txt`, `HI-TECH 180.txt`, `NITZHONOT 150.txt`, `SUOMISAUNDI 150.txt`, `PSYBREAKS 135.txt`, `PSYDUB 100.txt`, `UK HARD HOUSE 150.txt`, `HARD NRG 155.txt`, `SCOUSE HOUSE 150.txt`, `CHICAGO HARD HOUSE 135.txt`, `DUTCH HOUSE 128.txt`, `EBM 120.txt`, `BELGIAN EBM 118.txt`, `NEW BEAT 110.txt`, `AGGROTECH 140.txt`, `DARK ELECTRO 125.txt`, `EBM TECHNO 130.txt`, `RAVE 91 130.txt`, `HARDCORE TECHNO 145.txt`, `BREAKBEAT HARDCORE 145.txt`, `DARKCORE 155.txt`, `DRILL N BASS 175.txt`, generados con `tools/make_style.py build` desde fuentes en `styles_src/` escritas con la escala de 5 niveles. Cada fuente SHALL llevar una receta de groove (swing, amount por voz y slide) en un comentario.

#### Scenario: Selección en el plugin
- **WHEN** se elige cualquiera de ellos en los selectores de estilo
- **THEN** el plugin genera el patrón base de ese estilo

#### Scenario: Fuente y archivo coinciden
- **WHEN** se ejecuta `python3 tools/check_styles.py`
- **THEN** imprime `ok`, y cada `.txt` nuevo es idéntico al que genera su fuente

### Requirement: Reparto común de patrones
Los 42 estilos SHALL repartir sus patrones como las cumbias: p4/p5 BASE (centro del pad, por defecto), p2/p3 ENERGÍA, p6/p7 VARIACIÓN, p0/p1 INTRO y p8 FILL. Todos los patrones SHALL contener golpes.

#### Scenario: Pad en el centro
- **WHEN** el pad XY está en (0,0)
- **THEN** suena la base del estilo (p4 en el compás 1 y p5 en el compás 2)

#### Scenario: FILL
- **WHEN** suena p8 de cualquiera de los 42 estilos
- **THEN** la caja o los toms tocan un redoble

### Requirement: Capas de Density
En cada estilo, el ritmo esencial SHALL ir en el nivel `X`, y los adornos SHALL ir en los niveles inferiores, de más a menos importante.

#### Scenario: Density por defecto
- **WHEN** suena cualquier estilo con Density por defecto
- **THEN** solo suenan los pasos `X` de la fuente

#### Scenario: Subir Density
- **WHEN** Density pasa de 50 a 255
- **THEN** se van añadiendo golpes sin que desaparezca ninguno de los anteriores

### Requirement: Ritmo propio de cada estilo
Con Density por defecto, la base (p4/p5) de cada estilo SHALL tocar el ritmo que define su género, y SHALL NOT coincidir en kick, snare y hats con la base de ningún otro estilo de `drum_styles_v/`.

#### Scenario: Bombo a negras
- **WHEN** suena la base de cualquier estilo nuevo salvo DARKCORE 155, DRILL N BASS 175, EBM 120, BELGIAN EBM 118, DARK ELECTRO 125, PSYBREAKS 135 y PSYDUB 100
- **THEN** el kick toca las cuatro negras del compás 1

#### Scenario: Ghettotech
- **WHEN** suena la base de GHETTOTECH 150
- **THEN** el clap toca las cuatro negras y el kick además cada "a"

#### Scenario: Gabber desnudo
- **WHEN** suena la base de GABBER 180 con Density por defecto
- **THEN** solo suenan el kick en las negras y el hho en cada "&"

#### Scenario: Redoble de gabber con Density
- **WHEN** suena p5 de GABBER 180 y Density pasa de 50 a 180
- **THEN** el kick añade semicorcheas y luego fusas en la negra 4

#### Scenario: Gabber roll
- **WHEN** suena p5 de GABBER ROLL 180 con Density por defecto
- **THEN** el kick toca la "e", el "&" y la "a" de la negra 4 además de las negras

#### Scenario: Breakbeat hardcore frente a jungle
- **WHEN** se comparan las bases de BREAKBEAT HARDCORE 145 y JUNGLE 165
- **THEN** BREAKBEAT HARDCORE toca el kick en las cuatro negras del compás 1, y JUNGLE no

#### Scenario: Drill and bass
- **WHEN** suena la base de DRILL N BASS 175 con Density por defecto
- **THEN** el snare toca fusas seguidas en las negras 2 y 4 de los dos compases

#### Scenario: Bombo en corcheas
- **WHEN** suena la base de EBM 120
- **THEN** el kick toca las ocho corcheas del compás

#### Scenario: Psydub en medio tiempo
- **WHEN** suena la base de PSYDUB 100
- **THEN** el kick toca solo la negra 1 y el snare solo la 3

#### Scenario: Dutch house
- **WHEN** suena la base de DUTCH HOUSE 128
- **THEN** el clap toca cada contratiempo

#### Scenario: Subgéneros de psytrance distintos
- **WHEN** se comparan las bases de los trece estilos de Psytrance
- **THEN** no hay dos que coincidan en kick, snare, clap, hhc y hho

#### Scenario: Fila de hardcore
- **WHEN** se abre `docs/fingerprints.html`
- **THEN** TRANCE 138, MAKINA 170, GABBER 180, GABBER ROLL 180 y HAPPY HARDCORE 170 aparecen bajo "Hardcore / hard dance", y los de psytrance, hard house y EBM bajo sus filas nuevas

### Requirement: Familia en el README y en la página de huellas
La tabla "Included styles" del README SHALL listar los estilos nuevos así: los cinco de techno añadidos a la fila "Techno", los cinco de house a la fila "House", GABBER 180, GABBER ROLL 180 y HAPPY HARDCORE 170 a la fila "Hardcore / hard dance" (antes "Hard dance"), DRILL N BASS 175 a la fila "Breaks", filas nuevas "Psytrance" (13 estilos), "Hard house" (5) y "EBM / industrial" (6), y RAVE 91 130, HARDCORE TECHNO 145, BREAKBEAT HARDCORE 145 y DARKCORE 155 en una fila nueva "Rave / oldskool". `docs/fingerprints.html` SHALL estar regenerado con esa tabla.

#### Scenario: Página al día
- **WHEN** se ejecuta `python3 tools/check_styles.py`
- **THEN** no informa de que `docs/fingerprints.html` esté desfasado

#### Scenario: Agrupación
- **WHEN** se abre `docs/fingerprints.html`
- **THEN** cada estilo nuevo aparece bajo la familia que le asigna la tabla, y no en "Other"

### Requirement: Estilos existentes intactos
El cambio SHALL NOT modificar ningún `.txt` existente de `drum_styles_v/`.

#### Scenario: Comprobación con git
- **WHEN** se aplica el cambio
- **THEN** `git status` solo muestra como nuevos los 42 `.txt` y sus fuentes, y ningún `.txt` anterior como modificado
