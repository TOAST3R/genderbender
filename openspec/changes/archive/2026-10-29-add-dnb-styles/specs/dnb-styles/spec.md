## ADDED Requirements

### Requirement: Siete estilos de drum & bass con tempo
`drum_styles_v/` SHALL incluir `JUNGLE 165.txt`, `RAGGA JUNGLE 165.txt`, `HARDSTEP 172.txt`, `JUMP-UP 174.txt`, `DANCEFLOOR DNB 174.txt`, `TECHSTEP 172.txt` y `HALFTIME 174.txt`, generados con `tools/make_style.py build` desde fuentes en `styles_src/` escritas con la escala de 5 niveles. Cada fuente SHALL llevar una receta de groove (swing y slide) en un comentario.

#### Scenario: Selección en el plugin
- **WHEN** se elige cualquiera de ellos en los selectores de estilo
- **THEN** el plugin genera el patrón base de ese estilo

#### Scenario: Fuente y archivo coinciden
- **WHEN** se ejecuta `python3 tools/check_styles.py`
- **THEN** imprime `ok`, y cada `.txt` nuevo es idéntico al que genera su fuente

### Requirement: Reparto común de patrones
Los siete estilos SHALL repartir sus patrones como las cumbias: p4/p5 BASE (centro del pad, por defecto), p2/p3 ENERGÍA, p6/p7 VARIACIÓN, p0/p1 INTRO y p8 FILL. Todos los patrones SHALL contener golpes.

#### Scenario: Pad en el centro
- **WHEN** el pad XY está en (0,0)
- **THEN** suena la base del estilo (p4 en el compás 1 y p5 en el compás 2)

#### Scenario: FILL
- **WHEN** suena p8 de cualquiera de los siete estilos
- **THEN** la caja o los toms tocan un redoble

### Requirement: Capas de Density
En cada estilo, el ritmo esencial SHALL ir en el nivel `X`, y los adornos (fantasmas de caja, kicks extra, aperturas de hat, trozos de break) SHALL ir en los niveles inferiores, de más a menos importante.

#### Scenario: Density por defecto
- **WHEN** suena cualquier estilo con Density por defecto
- **THEN** solo suenan los pasos `X` de la fuente

#### Scenario: Subir Density
- **WHEN** Density pasa de 50 a 255
- **THEN** se van añadiendo golpes sin que desaparezca ninguno de los anteriores

### Requirement: Ritmo propio de cada sub-género
Con Density por defecto, la base (p4/p5) de cada estilo SHALL tocar el ritmo que define su sub-género, de forma que no haya dos estilos con el mismo kick, snare y hats.

#### Scenario: Two-step
- **WHEN** suena la base de JUMP-UP 174, DANCEFLOOR DNB 174 o TECHSTEP 172
- **THEN** el kick cae en la negra 1 y en el "&" del 3, y el snare en las negras 2 y 4

#### Scenario: Halftime
- **WHEN** suena la base de HALFTIME 174
- **THEN** el snare cae solo en la negra 3 de cada compás

#### Scenario: Jungle
- **WHEN** suena la base de JUNGLE 165 o de RAGGA JUNGLE 165
- **THEN** además de las negras 2 y 4, el snare toca al menos un golpe sincopado fuera de las negras

#### Scenario: Ragga frente a jungle
- **WHEN** se comparan las bases de RAGGA JUNGLE 165 y JUNGLE 165
- **THEN** RAGGA JUNGLE añade el clap en 3-3-2, y JUNGLE no lo tiene

#### Scenario: Dancefloor frente a techstep
- **WHEN** se comparan las bases de DANCEFLOOR DNB 174 y TECHSTEP 172
- **THEN** DANCEFLOOR toca el hat abierto en cada contratiempo, y TECHSTEP solo el hat cerrado en las negras

### Requirement: Estilos existentes intactos
El cambio SHALL NOT modificar ningún `.txt` existente de `drum_styles_v/`, incluidos `drumbass.txt` y `DurumBass160.txt`.

#### Scenario: Comprobación con git
- **WHEN** se aplica el cambio
- **THEN** `git status` solo muestra como nuevos los siete `.txt` y sus fuentes, y ningún `.txt` anterior como modificado
