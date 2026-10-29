# ukgarage-techno-reggae-styles Specification

## Purpose
TBD - created by archiving change add-ukgarage-techno-reggae-styles. Update Purpose after archive.
## Requirements
### Requirement: Veinte estilos de UK garage, techno y reggae con tempo
`drum_styles_v/` SHALL incluir `SPEED GARAGE 135.txt`, `BASSLINE 138.txt`, `BREAKSTEP 140.txt`, `WONKY 140.txt`, `BLEEP TECHNO 122.txt`, `AMBIENT TECHNO 120.txt`, `TRIBAL TECHNO 130.txt`, `DEEP TECHNO 124.txt`, `HYPNOTIC TECHNO 130.txt`, `PEAK TIME TECHNO 132.txt`, `INDUSTRIAL TECHNO 140.txt`, `SKA 120.txt`, `ROCKSTEADY 80.txt`, `ROOTS REGGAE 75.txt`, `DUB 70.txt`, `ROCKERS 80.txt`, `STEPPERS 75.txt`, `TWO TONE 160.txt`, `DIGITAL DANCEHALL 95.txt`, `MODERN DANCEHALL 100.txt`, generados con `tools/make_style.py build` desde fuentes en `styles_src/` escritas con la escala de 5 niveles. Cada fuente SHALL llevar una receta de groove (swing, amount por voz y slide) en un comentario.

#### Scenario: Selección en el plugin
- **WHEN** se elige cualquiera de ellos en los selectores de estilo
- **THEN** el plugin genera el patrón base de ese estilo

#### Scenario: Fuente y archivo coinciden
- **WHEN** se ejecuta `python3 tools/check_styles.py`
- **THEN** imprime `ok`, y cada `.txt` nuevo es idéntico al que genera su fuente

### Requirement: Reparto común de patrones
Los 20 estilos SHALL repartir sus patrones como las cumbias: p4/p5 BASE (centro del pad, por defecto), p2/p3 ENERGÍA, p6/p7 VARIACIÓN, p0/p1 INTRO y p8 FILL. Todos los patrones SHALL contener golpes.

#### Scenario: Pad en el centro
- **WHEN** el pad XY está en (0,0)
- **THEN** suena la base del estilo (p4 en el compás 1 y p5 en el compás 2)

#### Scenario: FILL
- **WHEN** suena p8 de cualquiera de los 20 estilos
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

#### Scenario: One drop
- **WHEN** suena la base de ROOTS REGGAE 75
- **THEN** el kick y el rim tocan solo la negra 3

#### Scenario: Steppers
- **WHEN** suena la base de STEPPERS 75
- **THEN** el kick toca las cuatro negras y el rim la 3

#### Scenario: Skank del ska
- **WHEN** suena la base de SKA 120
- **THEN** el hho toca cada contratiempo y el kick la 1 y la 3

#### Scenario: UK garage reunido
- **WHEN** se abre la familia "UK garage" en la página de huellas
- **THEN** aparecen los estilos de 2-step, grime, dubstep, UK funky y 4x4 junto a los cuatro nuevos, y no existen las familias "Grime" ni "Dubstep"

#### Scenario: Techno cronológico
- **WHEN** se abre la familia "Techno" en la página de huellas
- **THEN** DETROIT TECHNO 128 es el primero y los originales techAXX, TekkBooooring, TekkChungo y TekkThump van al final

#### Scenario: Sin fills repetidos
- **WHEN** se comparan los p6, p7 y p8 no vacíos de los 20 estilos nuevos con los de todos los estilos generados
- **THEN** no hay dos iguales

### Requirement: Familia en el README y en la página de huellas
La tabla "Included styles" del README SHALL listar los estilos nuevos así: una fila "UK garage" que reúne las antiguas "UK garage / 2-step", "Grime" y "Dubstep" más los cuatro estilos nuevos, la fila "Techno" en orden cronológico con los siete nuevos, una fila nueva "Reggae / dancehall" con los nueve nuevos y 101 DANCEHALL, y la fila de reggaeton renombrada a "Reggaeton / funk carioca", todo en orden alfabético de familias con "Other" al final. `docs/fingerprints.html` SHALL estar regenerado con esa tabla.

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
- **THEN** `git status` solo muestra como nuevos los 20 `.txt` y sus fuentes, y ningún `.txt` anterior como modificado

