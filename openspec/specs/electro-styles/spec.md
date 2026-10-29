# electro-styles Specification

## Purpose
TBD - created by archiving change fix-electro-styles. Update Purpose after archive.
## Requirements
### Requirement: Nueve estilos de electro con tempo
`drum_styles_v/` SHALL incluir `CYBOTRON ELECTRO 125.txt`, `ELECTRO FUNK 127.txt`, `DARKWAVE 120.txt`, `ELECTRO BASS 130.txt`, `DETROIT ELECTRO 130.txt`, `ELECTROCLASH 125.txt`, `ELECTRO HOUSE 128.txt`, `OUTRUN 118.txt`, `INDUSTRIAL ELECTRO 130.txt`, generados con `tools/make_style.py build` desde fuentes en `styles_src/` escritas con la escala de 5 niveles. Cada fuente SHALL llevar una receta de groove (swing, amount por voz y slide) en un comentario.

#### Scenario: Selección en el plugin
- **WHEN** se elige cualquiera de ellos en los selectores de estilo
- **THEN** el plugin genera el patrón base de ese estilo

#### Scenario: Fuente y archivo coinciden
- **WHEN** se ejecuta `python3 tools/check_styles.py`
- **THEN** imprime `ok`, y cada `.txt` nuevo es idéntico al que genera su fuente

### Requirement: Reparto común de patrones
Los 9 estilos SHALL repartir sus patrones como las cumbias: p4/p5 BASE (centro del pad, por defecto), p2/p3 ENERGÍA, p6/p7 VARIACIÓN, p0/p1 INTRO y p8 FILL. Todos los patrones SHALL contener golpes.

#### Scenario: Pad en el centro
- **WHEN** el pad XY está en (0,0)
- **THEN** suena la base del estilo (p4 en el compás 1 y p5 en el compás 2)

#### Scenario: FILL
- **WHEN** suena p8 de cualquiera de los 9 estilos
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

#### Scenario: Electro de Detroit
- **WHEN** suena la base de DETROIT ELECTRO 130
- **THEN** el kick no toca las cuatro negras y el hhc toca las 16 semicorcheas

#### Scenario: Electro-bass
- **WHEN** suena p5 de ELECTRO BASS 130 con Density a 255
- **THEN** el hhc toca fusas en la negra 4

#### Scenario: Outrun
- **WHEN** suena la base de OUTRUN 118
- **THEN** el kick toca las cuatro negras y snare y clap la 2 y la 4

#### Scenario: Familia Electro
- **WHEN** se abre la familia "Electro" en la página de huellas
- **THEN** CYBOTRON ELECTRO 125 es el primero, y aparecen SYNTHWAVE 100, DARK ELECTRO 125 y GHETTOTECH 150

#### Scenario: Estilos borrados
- **WHEN** se buscan ELECTRO CYBOTRON, ELECTRO UR 138, BASS 101 y AFRO BEAT
- **THEN** no existen ni en `drum_styles_v/` ni en la tabla del README

### Requirement: Familia en el README y en la página de huellas
La tabla "Included styles" del README SHALL listar los estilos nuevos así: una fila "Electro" (antes "Electro / Miami bass") con los nueve estilos nuevos más SYNTHWAVE 100, DARK ELECTRO 125 y GHETTOTECH 150 en orden cronológico, y sin ELECTRO CYBOTRON, ELECTRO UR 138, BASS 101 ni AFRO BEAT en ninguna fila. `docs/fingerprints.html` SHALL estar regenerado con esa tabla.

#### Scenario: Página al día
- **WHEN** se ejecuta `python3 tools/check_styles.py`
- **THEN** no informa de que `docs/fingerprints.html` esté desfasado

#### Scenario: Agrupación
- **WHEN** se abre `docs/fingerprints.html`
- **THEN** cada estilo nuevo aparece bajo la familia que le asigna la tabla, y no en "Other"

### Requirement: Estilos rotos borrados
El cambio SHALL borrar `ELECTRO CYBOTRON.txt`, `ELECTRO UR 138.txt`, `BASS 101.txt` y `AFRO BEAT.txt`, y SHALL NOT modificar ningún otro `.txt` existente.

#### Scenario: Comprobación con git
- **WHEN** se aplica el cambio
- **THEN** `git status` muestra esos cuatro `.txt` como borrados, los nueve nuevos y sus fuentes como nuevos, y ningún otro `.txt` como modificado

