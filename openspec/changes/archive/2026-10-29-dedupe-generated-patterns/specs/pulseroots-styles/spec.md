## MODIFIED Requirements

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
