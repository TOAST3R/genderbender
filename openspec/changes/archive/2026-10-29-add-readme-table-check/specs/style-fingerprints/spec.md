## ADDED Requirements

### Requirement: Tabla del README al día con los estilos
`python3 tools/check_styles.py` SHALL fallar si algún `drum_styles_v/*.txt` no corresponde a ninguna entrada de la tabla "Included styles" del README, y SHALL fallar si alguna entrada de la tabla no corresponde a ningún `.txt`. La correspondencia SHALL usar la misma regla que la página de huellas: una entrada `NOMBRE (bpm)` corresponde a `NOMBRE.txt` y a `NOMBRE bpm.txt`, y una entrada sin `(bpm)` al nombre tal cual. Cada error SHALL nombrar el estilo o la entrada.

#### Scenario: Tabla y carpeta coinciden
- **WHEN** cada `.txt` tiene su entrada en la tabla y cada entrada su `.txt`
- **THEN** `check_styles.py` no informa de ningún error de la tabla

#### Scenario: Estilo sin entrada
- **WHEN** existe `drum_styles_v/NUEVO 120.txt` y la tabla no lo lista
- **THEN** `check_styles.py` sale con error y nombra `NUEVO 120.txt`

#### Scenario: Entrada sin estilo
- **WHEN** la tabla lista `TEST2` y no existe ningún `.txt` que le corresponda
- **THEN** `check_styles.py` sale con error y nombra la entrada `TEST2` y su familia
