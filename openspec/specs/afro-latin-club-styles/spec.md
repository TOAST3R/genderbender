# afro-latin-club-styles Specification

## Purpose
TBD - created by archiving change add-afro-latin-club-styles. Update Purpose after archive.
## Requirements
### Requirement: Cuatro estilos de club afro y latino con tempo
`drum_styles_v/` SHALL incluir `AMAPIANO 112.txt`, `AFRO HOUSE 122.txt`, `KUDURO 135.txt`, `GUARACHA 130.txt`, generados con `tools/make_style.py build` desde fuentes en `styles_src/` escritas con la escala de 5 niveles. Cada fuente SHALL llevar una receta de groove (swing, amount por voz y slide) en un comentario.

#### Scenario: Selección en el plugin
- **WHEN** se elige cualquiera de ellos en los selectores de estilo
- **THEN** el plugin genera el patrón base de ese estilo

#### Scenario: Fuente y archivo coinciden
- **WHEN** se ejecuta `python3 tools/check_styles.py`
- **THEN** imprime `ok`, y cada `.txt` nuevo es idéntico al que genera su fuente

### Requirement: Reparto común de patrones
Los 4 estilos SHALL repartir sus patrones como las cumbias: p4/p5 BASE (centro del pad, por defecto), p2/p3 ENERGÍA, p6/p7 VARIACIÓN, p0/p1 INTRO y p8 FILL. Todos los patrones SHALL contener golpes.

#### Scenario: Pad en el centro
- **WHEN** el pad XY está en (0,0)
- **THEN** suena la base del estilo (p4 en el compás 1 y p5 en el compás 2)

#### Scenario: FILL
- **WHEN** suena p8 de cualquiera de los 4 estilos
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

#### Scenario: Log drum
- **WHEN** suena la base de AMAPIANO 112
- **THEN** lotom toca los pasos 0, 3, 6, 10 y 12 de cada compás (en semicorcheas)

#### Scenario: Toms en todos
- **WHEN** suena la base de cualquiera de los cuatro estilos
- **THEN** hitom o lotom tocan al menos dos golpes por compás en `X`

#### Scenario: Tresillo de kuduro
- **WHEN** suena la base de KUDURO 135
- **THEN** el kick toca las cuatro negras y el snare los pasos 0, 3, 8 y 11 de cada compás (en semicorcheas)

#### Scenario: Afro house frente a guaracha
- **WHEN** se comparan las bases de AFRO HOUSE 122 y GUARACHA 130
- **THEN** AFRO HOUSE marca 2 y 4 con el clap y GUARACHA con el snare

### Requirement: Familia en el README y en la página de huellas
La tabla "Included styles" del README SHALL listar los estilos nuevos así: una fila nueva "Afro / Latin club" con AMAPIANO 112, AFRO HOUSE 122, KUDURO 135 y GUARACHA 130. `docs/fingerprints.html` SHALL estar regenerado con esa tabla.

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
- **THEN** `git status` solo muestra como nuevos los 4 `.txt` y sus fuentes, y ningún `.txt` anterior como modificado

