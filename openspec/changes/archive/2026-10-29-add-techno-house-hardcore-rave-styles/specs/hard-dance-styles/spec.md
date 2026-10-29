## MODIFIED Requirements

### Requirement: Familia en el README y en la página de huellas
La tabla "Included styles" del README SHALL listar TRANCE 138 y MAKINA 170 en la fila "Hardcore / hard dance" (antes "Hard dance"), junto a los estilos de hardcore. `docs/fingerprints.html` SHALL estar regenerado con esa tabla.

#### Scenario: Página al día
- **WHEN** se ejecuta `python3 tools/check_styles.py`
- **THEN** no informa de que `docs/fingerprints.html` esté desfasado

#### Scenario: Agrupación
- **WHEN** se abre `docs/fingerprints.html`
- **THEN** TRANCE 138 y MAKINA 170 aparecen bajo la familia "Hardcore / hard dance", y no en "Other"
