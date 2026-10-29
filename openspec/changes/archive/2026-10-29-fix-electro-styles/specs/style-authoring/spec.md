## ADDED Requirements

### Requirement: Base no vacía
`python3 tools/check_styles.py` SHALL fallar, nombrando el estilo, si algún `drum_styles_v/*.txt` tiene el patrón p4 o el p5 sin ninguna nota.

#### Scenario: Base vacía
- **WHEN** un estilo tiene p4 o p5 a 0 en todas las voces
- **THEN** `check_styles.py` sale con error y nombra ese estilo

#### Scenario: Todos con base
- **WHEN** todos los estilos tienen notas en p4 y p5
- **THEN** `check_styles.py` imprime `ok`
