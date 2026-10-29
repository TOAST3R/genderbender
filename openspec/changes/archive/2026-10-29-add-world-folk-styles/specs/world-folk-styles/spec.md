## ADDED Requirements

### Requirement: Treinta y seis estilos de folk y músicas del mundo con tempo
`drum_styles_v/` SHALL incluir `BLUES SHUFFLE 100.txt`, `WESTERN SWING 170.txt`, `BLUEGRASS 120.txt`, `COUNTRY SHUFFLE 120.txt`, `TRAIN BEAT 110.txt`, `ROCKABILLY 180.txt`, `ZYDECO 120.txt`, `TWO-STEP 140.txt`, `REEL 110.txt`, `JIG 115.txt`, `STRATHSPEY 120.txt`, `IRISH POLKA 140.txt`, `SON 95.txt`, `RUMBA GUAGUANCO 100.txt`, `BOLERO 80.txt`, `MERENGUE 130.txt`, `MAMBO 190.txt`, `CHA-CHA-CHA 120.txt`, `KOMPA 120.txt`, `SALSA 180.txt`, `BACHATA 130.txt`, `MARACATU 90.txt`, `FREVO 140.txt`, `SAMBA 100.txt`, `BAIAO 100.txt`, `AXE 130.txt`, `CANDOMBE 110.txt`, `TANGO 64.txt`, `MILONGA 90.txt`, `CHACARERA 70.txt`, `HUAYNO 90.txt`, `HUAPANGO 110.txt`, `SON JAROCHO 120.txt`, `FREYLEKHS 130.txt`, `BHANGRA 95.txt`, `KEHERWA 100.txt`, generados con `tools/make_style.py build` desde fuentes en `styles_src/` escritas con la escala de 5 niveles. Cada fuente SHALL llevar una receta de groove (swing, amount por voz y slide) en un comentario.

#### Scenario: Selección en el plugin
- **WHEN** se elige cualquiera de ellos en los selectores de estilo
- **THEN** el plugin genera el patrón base de ese estilo

#### Scenario: Fuente y archivo coinciden
- **WHEN** se ejecuta `python3 tools/check_styles.py`
- **THEN** imprime `ok`, y cada `.txt` nuevo es idéntico al que genera su fuente

### Requirement: Reparto común de patrones
Los 36 estilos SHALL repartir sus patrones como las cumbias: p4/p5 BASE (centro del pad, por defecto), p2/p3 ENERGÍA, p6/p7 VARIACIÓN, p0/p1 INTRO y p8 FILL. Todos los patrones SHALL contener golpes.

#### Scenario: Pad en el centro
- **WHEN** el pad XY está en (0,0)
- **THEN** suena la base del estilo (p4 en el compás 1 y p5 en el compás 2)

#### Scenario: FILL
- **WHEN** suena p8 de cualquiera de los 36 estilos
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

#### Scenario: Clave 3-2
- **WHEN** suena la base de SON 95 o SALSA 180
- **THEN** el clap toca los pasos 0, 3, 6, 10 y 12 de cada compás (en semicorcheas)

#### Scenario: Train beat
- **WHEN** suena la base de TRAIN BEAT 110
- **THEN** el snare toca las 16 semicorcheas y el kick la 1 y la 3

#### Scenario: Shuffle
- **WHEN** suena la base de COUNTRY SHUFFLE 120 con swing global 67
- **THEN** los hats caen en el primer y el tercer tresillo de cada negra

#### Scenario: Surdo de samba
- **WHEN** suena la base de SAMBA 100
- **THEN** el kick toca las negras 2 y 4 y no la 1 ni la 3

#### Scenario: Sin notas fuera de la rejilla
- **WHEN** se revisan los ocho estilos ternarios
- **THEN** ninguna nota cae fuera de los pasos 0, 2 y 5 de cada negra

### Requirement: Familia en el README y en la página de huellas
La tabla "Included styles" del README SHALL listar los estilos nuevos así: seis filas nuevas ("Brazil", "Celtic", "Country / Americana", "Latin / Caribbean", "South America" y "World folk") en su sitio alfabético, con los estilos en el orden de `design.md`. `docs/fingerprints.html` SHALL estar regenerado con esa tabla.

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
- **THEN** `git status` solo muestra como nuevos los 36 `.txt` y sus fuentes, y ningún `.txt` anterior como modificado
