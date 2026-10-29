## MODIFIED Requirements

### Requirement: Familia en el README y en la página de huellas
La tabla "Included styles" del README SHALL listar los estilos de este cambio así: los cinco de techno en la fila "Techno"; DEEP HOUSE 122, TECH HOUSE 126, ACID HOUSE 124 e ITALO HOUSE 122 en la fila "House"; GHETTOTECH 150 en la fila "Electro"; GABBER 180, GABBER ROLL 180 y HAPPY HARDCORE 170 en la fila "Hardcore / hard dance"; DRILL N BASS 175 en la fila "Breaks"; los 13 de psytrance en la fila "Psytrance"; los 5 de hard house en la fila "Hard house"; EBM 120, BELGIAN EBM 118, NEW BEAT 110, AGGROTECH 140 y EBM TECHNO 130 en la fila "EBM / industrial"; DARK ELECTRO 125 en la fila "Electro"; y RAVE 91 130, HARDCORE TECHNO 145, BREAKBEAT HARDCORE 145 y DARKCORE 155 en la fila "Rave / oldskool". `docs/fingerprints.html` SHALL estar regenerado con esa tabla.

#### Scenario: Página al día
- **WHEN** se ejecuta `python3 tools/check_styles.py`
- **THEN** no informa de que `docs/fingerprints.html` esté desfasado

#### Scenario: Agrupación
- **WHEN** se abre `docs/fingerprints.html`
- **THEN** cada estilo aparece bajo la familia que le asigna la tabla, con GHETTOTECH 150 y DARK ELECTRO 125 bajo "Electro", y ninguno en "Other"
