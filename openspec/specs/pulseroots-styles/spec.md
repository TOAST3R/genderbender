# pulseroots-styles Specification

## Purpose
TBD - created by archiving change add-pulseroots-styles. Update Purpose after archive.
## Requirements
### Requirement: Treinta y un estilos del árbol de PulseRoots con tempo
`drum_styles_v/` SHALL incluir `GLITCH HOP 110.txt`, `IDM 120.txt`, `SKWEEE 100.txt`, `DECONSTRUCTED CLUB 130.txt`, `MICROHOUSE 124.txt`, `DUB TECHNO 118.txt`, `SCHRANZ 150.txt`, `HARDGROOVE 135.txt`, `FRENCHCORE 200.txt`, `INDUSTRIAL HARDCORE 150.txt`, `HARDSTYLE 150.txt`, `BAKALAO 125.txt`, `BOOGIE 110.txt`, `MOTORIK 120.txt`, `FUTURE GARAGE 130.txt`, `PSYBIENT 100.txt`, `NEUROFUNK 174.txt`, `LIQUID DNB 174.txt`, `RIDDIM 140.txt`, `FUTURE BASS 150.txt`, `MIDTEMPO BASS 105.txt`, `PHONK 130.txt`, `DRIFT PHONK 155.txt`, `BRAZILIAN PHONK 130.txt`, `BROKEN BEAT 120.txt`, `BOSSA NOVA CHILL 100.txt`, `DEMBOW 120.txt`, `FUNK DE RAIZ 130.txt`, `SINGELI 200.txt`, `NORTEC 125.txt`, `ACID JAZZ 105.txt`, generados con `tools/make_style.py build` desde fuentes en `styles_src/` escritas con la escala de 5 niveles. Cada fuente SHALL llevar una receta de groove (swing, amount por voz y slide) en un comentario.

#### Scenario: Selección en el plugin
- **WHEN** se elige cualquiera de ellos en los selectores de estilo
- **THEN** el plugin genera el patrón base de ese estilo

#### Scenario: Fuente y archivo coinciden
- **WHEN** se ejecuta `python3 tools/check_styles.py`
- **THEN** imprime `ok`, y cada `.txt` nuevo es idéntico al que genera su fuente

### Requirement: Reparto común de patrones
Los 31 estilos SHALL repartir sus patrones como las cumbias: p4/p5 BASE (centro del pad, por defecto), p2/p3 ENERGÍA, p6/p7 VARIACIÓN, p0/p1 INTRO y p8 FILL. Los patrones p0–p5 SHALL contener golpes. Los patrones p6, p7 y p8 SHALL contener golpes salvo cuando repetirían exactamente el mismo patrón de otro estilo generado: en ese caso SHALL quedar vacíos y el patrón se conserva solo en un estilo.

#### Scenario: Pad en el centro
- **WHEN** el pad XY está en (0,0)
- **THEN** suena la base del estilo (p4 en el compás 1 y p5 en el compás 2)

#### Scenario: Sin patrones repetidos
- **WHEN** se comparan los p6, p7 y p8 no vacíos de todos los estilos generados
- **THEN** no hay dos iguales

#### Scenario: FILL
- **WHEN** suena un p8 no vacío
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

#### Scenario: Medio tiempo
- **WHEN** suena la base de GLITCH HOP 110, PSYBIENT 100, RIDDIM 140, FUTURE BASS 150, MIDTEMPO BASS 105 o PHONK 130
- **THEN** el snare cae en la negra 3 y no en la 2 ni en la 4

#### Scenario: Hardstyle sin hats
- **WHEN** suena la base de HARDSTYLE 150 con Density por defecto
- **THEN** solo suenan el kick en las negras, el clap en 2 y 4 y el lotom a contratiempo

#### Scenario: Clave de bossa
- **WHEN** suena la base de BOSSA NOVA CHILL 100
- **THEN** el clap toca los pasos 0, 3, 6, 10 y 12 de cada compás (en semicorcheas)

#### Scenario: Dembow
- **WHEN** suena la base de DEMBOW 120
- **THEN** el snare toca los pasos 3, 6, 11 y 14 (en semicorcheas) y el kick las cuatro negras

#### Scenario: Ride de liquid
- **WHEN** suena la base de LIQUID DNB 174
- **THEN** el hho toca las ocho corcheas del compás

#### Scenario: Tabla alfabética
- **WHEN** se lee la tabla "Included styles" del README
- **THEN** las familias están en orden alfabético y "Other" es la última

### Requirement: Familia en el README y en la página de huellas
La tabla "Included styles" del README SHALL listar los estilos nuevos así: cuatro filas nuevas ("Bass music", "Downtempo / chill", "IDM / experimental" y "Phonk") en su sitio alfabético, y el resto de estilos añadidos a la fila de su familia existente (ver `design.md`), con la tabla en orden alfabético y "Other" al final. `docs/fingerprints.html` SHALL estar regenerado con esa tabla.

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
- **THEN** `git status` solo muestra como nuevos los 31 `.txt` y sus fuentes, y ningún `.txt` anterior como modificado

