# hiphop-styles Specification

## Purpose
TBD - created by archiving change add-hiphop-styles. Update Purpose after archive.
## Requirements
### Requirement: Seis estilos de hip-hop y trap con tempo
`drum_styles_v/` SHALL incluir `BOOM BAP 90.txt`, `LOFI HIPHOP 82.txt`, `TRIP HOP 88.txt`, `NEW JACK SWING 104.txt`, `TRAP 140.txt`, `UK DRILL 142.txt`, generados con `tools/make_style.py build` desde fuentes en `styles_src/` escritas con la escala de 5 niveles. Cada fuente SHALL llevar una receta de groove (swing, amount por voz y slide) en un comentario.

#### Scenario: Selección en el plugin
- **WHEN** se elige cualquiera de ellos en los selectores de estilo
- **THEN** el plugin genera el patrón base de ese estilo

#### Scenario: Fuente y archivo coinciden
- **WHEN** se ejecuta `python3 tools/check_styles.py`
- **THEN** imprime `ok`, y cada `.txt` nuevo es idéntico al que genera su fuente

### Requirement: Reparto común de patrones
Los 6 estilos SHALL repartir sus patrones como las cumbias: p4/p5 BASE (centro del pad, por defecto), p2/p3 ENERGÍA, p6/p7 VARIACIÓN, p0/p1 INTRO y p8 FILL. Todos los patrones SHALL contener golpes.

#### Scenario: Pad en el centro
- **WHEN** el pad XY está en (0,0)
- **THEN** suena la base del estilo (p4 en el compás 1 y p5 en el compás 2)

#### Scenario: FILL
- **WHEN** suena p8 de cualquiera de los 6 estilos
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

#### Scenario: Backbeat
- **WHEN** suena la base de BOOM BAP 90, TRIP HOP 88 o NEW JACK SWING 104
- **THEN** el snare cae en las negras 2 y 4

#### Scenario: Medio tiempo
- **WHEN** suena la base de TRAP 140 o UK DRILL 142
- **THEN** el snare cae en la negra 3 y no en la 2 ni en la 4

#### Scenario: Redoble en fusas
- **WHEN** suena p5 de TRAP 140 con Density a 255
- **THEN** el hhc toca fusas seguidas en la negra 4

#### Scenario: Drill frente a trap
- **WHEN** se comparan las bases de UK DRILL 142 y TRAP 140
- **THEN** solo UK DRILL toca un snare en la "a" del 4 del compás 2

#### Scenario: Lofi frente a boom bap
- **WHEN** se comparan las bases de LOFI HIPHOP 82 y BOOM BAP 90
- **THEN** LOFI marca 2 y 4 con el clap y BOOM BAP con el snare

### Requirement: Familia en el README y en la página de huellas
La tabla "Included styles" del README SHALL listar los estilos nuevos así: una fila nueva "Hip-hop" con BOOM BAP 90, LOFI HIPHOP 82, TRIP HOP 88 y NEW JACK SWING 104, y TRAP 140 y UK DRILL 142 añadidos a la fila "R&B / trap". `docs/fingerprints.html` SHALL estar regenerado con esa tabla.

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
- **THEN** `git status` solo muestra como nuevos los 6 `.txt` y sus fuentes, y ningún `.txt` anterior como modificado

