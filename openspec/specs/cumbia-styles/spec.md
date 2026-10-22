# cumbia-styles Specification

## Purpose
TBD - created by archiving change add-cumbia-styles. Update Purpose after archive.
## Requirements
### Requirement: Cinco estilos de cumbia con tempo
`drum_styles_v/` SHALL incluir `CUMBIA COLOMBIANA 95.txt`, `CUMBIA SONIDERA 92.txt`, `CUMBIA VILLERA 98.txt`, `CUMBIA DIGITAL 100.txt` y `CUMBIA REBAJADA 72.txt`, generados desde `styles_src/`, con el tempo sugerido en el nombre y una receta de groove en la fuente.

#### Scenario: Selección en el plugin
- **WHEN** se elige cualquiera de ellos en los selectores de estilo
- **THEN** el plugin genera el patrón base de ese estilo

### Requirement: Reparto común de patrones
Los cinco estilos SHALL repartir sus patrones así: p4/p5 BASE (centro del pad, por defecto), p2/p3 ENERGÍA, p6/p7 VARIACIÓN, p0/p1 INTRO y p8 FILL. Todos ellos SHALL contener golpes.

#### Scenario: Pad en el centro
- **WHEN** el pad XY está en (0,0)
- **THEN** suena la base del estilo (p4 en el compás 1 y p5 en el compás 2)

#### Scenario: Ritmo esencial con Density por defecto
- **WHEN** suena cualquier estilo de cumbia con Density en su valor por defecto
- **THEN** suenan el bombo, el llamador o timbal y el guache, güiro o shaker de la base, y los adornos (valores menores de 255) solo se añaden al subir Density

#### Scenario: Base de la cumbia colombiana
- **WHEN** suena la base de CUMBIA COLOMBIANA 95 con Div por defecto
- **THEN** el kick cae en las negras 1 y 3 y el llamador (snare) en el "&" de cada negra

