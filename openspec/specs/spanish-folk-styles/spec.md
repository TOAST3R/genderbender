# spanish-folk-styles Specification

## Purpose
TBD - created by archiving change add-spanish-folk-styles. Update Purpose after archive.
## Requirements
### Requirement: Dieciséis estilos de folclore español y flamenco con tempo
`drum_styles_v/` SHALL incluir `MUINEIRA 120.txt`, `PASACORREDOIRA 110.txt`, `MARCHA PROCESIONAL 70.txt`, `ARIN-ARIN 130.txt`, `BIRIBILKETA 110.txt`, `JOTA ARAGONESA 60.txt`, `SARDANA 100.txt`, `BALL DE BASTONS 110.txt`, `TANGOS 100.txt`, `TIENTOS 75.txt`, `BULERIA 80.txt`, `SOLEA 50.txt`, `SEGUIRIYA 45.txt`, `SEVILLANA 65.txt`, `FANDANGO DE HUELVA 60.txt`, `TAJARASTE 110.txt`, generados con `tools/make_style.py build` desde fuentes en `styles_src/` escritas con la escala de 5 niveles. Cada fuente SHALL llevar una receta de groove (swing, amount por voz y slide) en un comentario.

#### Scenario: Selección en el plugin
- **WHEN** se elige cualquiera de ellos en los selectores de estilo
- **THEN** el plugin genera el patrón base de ese estilo

#### Scenario: Fuente y archivo coinciden
- **WHEN** se ejecuta `python3 tools/check_styles.py`
- **THEN** imprime `ok`, y cada `.txt` nuevo es idéntico al que genera su fuente

### Requirement: Reparto común de patrones
Los 16 estilos SHALL repartir sus patrones como las cumbias: p4/p5 BASE (centro del pad, por defecto), p2/p3 ENERGÍA, p6/p7 VARIACIÓN, p0/p1 INTRO y p8 FILL. Todos los patrones SHALL contener golpes.

#### Scenario: Pad en el centro
- **WHEN** el pad XY está en (0,0)
- **THEN** suena la base del estilo (p4 en el compás 1 y p5 en el compás 2)

#### Scenario: FILL
- **WHEN** suena p8 de cualquiera de los 16 estilos
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

#### Scenario: Tresillo exacto
- **WHEN** suena la base de MUINEIRA 120 con swing global 67
- **THEN** todas las notas caen a 0, 1/3 o 2/3 de cada negra del plugin, con menos de 3 ms de error

#### Scenario: Compás de bulería
- **WHEN** suena la base de BULERIA 80 con swing 67
- **THEN** las palmas fuertes caen en los tiempos 3, 6, 8, 10 y 12 del compás de 12

#### Scenario: Palmas de tangos
- **WHEN** suena la base de TANGOS 100
- **THEN** las palmas tocan las negras 2, 3 y 4 y no la 1

#### Scenario: Receta de swing
- **WHEN** se lee la cabecera de cualquier estilo ternario
- **THEN** pide swing global 67 y el preview de la página lo pone al pulsar Play

### Requirement: Familia en el README y en la página de huellas
La tabla "Included styles" del README SHALL listar los estilos nuevos así: dos filas nuevas, "Flamenco" y "Folk ibérico", en su sitio alfabético, con los estilos en el orden de `design.md`. `docs/fingerprints.html` SHALL estar regenerado con esa tabla.

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
- **THEN** `git status` solo muestra como nuevos los 16 `.txt` y sus fuentes, y ningún `.txt` anterior como modificado

