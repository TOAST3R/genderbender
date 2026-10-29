# hard-dance-styles Specification

## Purpose
TBD - created by archiving change add-hard-dance-styles. Update Purpose after archive.
## Requirements
### Requirement: Dos estilos de trance y mákina con tempo
`drum_styles_v/` SHALL incluir `TRANCE 138.txt`, `MAKINA 170.txt`, generados con `tools/make_style.py build` desde fuentes en `styles_src/` escritas con la escala de 5 niveles. Cada fuente SHALL llevar una receta de groove (swing, amount por voz y slide) en un comentario.

#### Scenario: Selección en el plugin
- **WHEN** se elige cualquiera de ellos en los selectores de estilo
- **THEN** el plugin genera el patrón base de ese estilo

#### Scenario: Fuente y archivo coinciden
- **WHEN** se ejecuta `python3 tools/check_styles.py`
- **THEN** imprime `ok`, y cada `.txt` nuevo es idéntico al que genera su fuente

### Requirement: Reparto común de patrones
Los 2 estilos SHALL repartir sus patrones como las cumbias: p4/p5 BASE (centro del pad, por defecto), p2/p3 ENERGÍA, p6/p7 VARIACIÓN, p0/p1 INTRO y p8 FILL. Todos los patrones SHALL contener golpes.

#### Scenario: Pad en el centro
- **WHEN** el pad XY está en (0,0)
- **THEN** suena la base del estilo (p4 en el compás 1 y p5 en el compás 2)

#### Scenario: FILL
- **WHEN** suena p8 de cualquiera de los 2 estilos
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

#### Scenario: Subida con Density
- **WHEN** suena p8 de TRANCE 138 y Density pasa de 50 a 180
- **THEN** el snare pasa de corcheas a semicorcheas y luego a fusas

#### Scenario: Trance
- **WHEN** suena la base de TRANCE 138
- **THEN** el kick toca las cuatro negras, el hho cada contratiempo y el clap la 2 y la 4

#### Scenario: Mákina frente a trance
- **WHEN** se comparan las bases de MAKINA 170 y TRANCE 138
- **THEN** MAKINA marca 2 y 4 con el snare y TRANCE con el clap

### Requirement: Familia en el README y en la página de huellas
La tabla "Included styles" del README SHALL listar TRANCE 138 y MAKINA 170 en la fila "Hardcore / hard dance" (antes "Hard dance"), junto a los estilos de hardcore. `docs/fingerprints.html` SHALL estar regenerado con esa tabla.

#### Scenario: Página al día
- **WHEN** se ejecuta `python3 tools/check_styles.py`
- **THEN** no informa de que `docs/fingerprints.html` esté desfasado

#### Scenario: Agrupación
- **WHEN** se abre `docs/fingerprints.html`
- **THEN** TRANCE 138 y MAKINA 170 aparecen bajo la familia "Hardcore / hard dance", y no en "Other"

### Requirement: Estilos existentes intactos
El cambio SHALL NOT modificar ningún `.txt` existente de `drum_styles_v/`.

#### Scenario: Comprobación con git
- **WHEN** se aplica el cambio
- **THEN** `git status` solo muestra como nuevos los 2 `.txt` y sus fuentes, y ningún `.txt` anterior como modificado

