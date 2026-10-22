# groove-swing Specification

## Purpose
TBD - created by archiving change add-swing-slide. Update Purpose after archive.
## Requirements
### Requirement: Swing global estilo MPC
El plugin SHALL ofrecer un parámetro de swing global con rango 50–75 % y valor por defecto 50 %, que define la posición de la segunda semicorchea dentro de cada corchea como `S/100 × 0.5` negras desde el inicio de la corchea.

#### Scenario: Swing neutro
- **WHEN** el swing global vale 50 %
- **THEN** todas las notas suenan en su posición recta de rejilla

#### Scenario: Swing máximo sobre semicorcheas
- **WHEN** el swing global vale 75 %, el amount de una voz vale 100 % y la voz tiene Div de semicorcheas (índice 3, 4 pasos por negra)
- **THEN** los pasos impares de la voz suenan 0.125 negras después de su posición recta y los pasos pares no se mueven

### Requirement: Swing amount por voz
Cada una de las 7 voces SHALL tener un parámetro amount de 0–100 % (por defecto 100 %), y el swing efectivo de la voz SHALL ser `S_voz = 50 + (S_global − 50) × amount / 100`.

#### Scenario: Voz excluida del swing
- **WHEN** el swing global vale 62 % y el amount del kick vale 0 %
- **THEN** el kick suena recto y las voces con amount 100 % usan swing 62 %

#### Scenario: Amount parcial
- **WHEN** el swing global vale 62 % y el amount del snare vale 50 %
- **THEN** el snare usa un swing efectivo del 56 %

### Requirement: Rejilla común de semicorcheas con deformación temporal
El swing SHALL aplicarse como una deformación temporal monótona y lineal a trozos de cada corchea: el tramo [0, 0.25) de la corchea se mapea a [0, p) y el tramo [0.25, 0.5) se mapea a [p, 0.5), con `p = S_voz/100 × 0.5`. Esto vale para cualquier Div de la voz.

#### Scenario: Voces en negras o corcheas
- **WHEN** una voz tiene Div de 1 o 2 pasos por negra y hay swing activo
- **THEN** sus notas no cambian de posición

#### Scenario: Voces en 32nds o tresillos
- **WHEN** una voz tiene Div de 8, 12 o 24 pasos por negra y hay swing activo
- **THEN** sus notas se desplazan según la deformación y nunca cambian de orden entre sí

### Requirement: Swing en modo break
El swing SHALL aplicarse igual a las notas generadas en la ventana de break que a las del modo normal.

#### Scenario: Break con swing
- **WHEN** una voz está en su ventana de break y hay swing activo
- **THEN** sus notas de break se desplazan con el mismo swing efectivo de la voz

