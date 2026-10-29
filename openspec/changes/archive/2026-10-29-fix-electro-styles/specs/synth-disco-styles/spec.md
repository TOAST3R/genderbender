## MODIFIED Requirements

### Requirement: Familia en el README y en la página de huellas
La tabla "Included styles" del README SHALL listar DISCO 118 e ITALO DISCO 120 en la fila "Synth / disco", y SYNTHWAVE 100 en la fila "Electro". `docs/fingerprints.html` SHALL estar regenerado con esa tabla.

#### Scenario: Página al día
- **WHEN** se ejecuta `python3 tools/check_styles.py`
- **THEN** no informa de que `docs/fingerprints.html` esté desfasado

#### Scenario: Agrupación
- **WHEN** se abre `docs/fingerprints.html`
- **THEN** DISCO 118 e ITALO DISCO 120 aparecen bajo "Synth / disco" y SYNTHWAVE 100 bajo "Electro"
