## ADDED Requirements

### Requirement: Pad XY del plugin
La vista ampliada SHALL tener un pad de −100 a 100 en cada eje que mezcle los patrones con la misma fórmula que el plugin: el sector se elige con las condiciones `x<0 y<0` → 1, `x<0 y>0` → 2, `x≥0 y≥0` → 3, `x≥0 y≤0` → 4, en ese orden y ganando la última que se cumple; cada voz interpola los valores de cuatro patrones con `X = |x|/100` e `Y = |y|/100` según la fórmula de su sector; y el valor resultante suena si `256 − v < Density`. El pad SHALL poder moverse mientras suena.

#### Scenario: Centro
- **WHEN** el pad está en (0, 0)
- **THEN** suenan las mismas notas que p4 en el compás 1 y p5 en el 2

#### Scenario: Bordes
- **WHEN** el pad está en (100, 0), en (0, −100) o en (100, −100)
- **THEN** suenan p2/p3, p0/p1 o p8, respectivamente

#### Scenario: Discontinuidad del centro
- **WHEN** el pad está en (0, 1)
- **THEN** la mezcla es la del sector 3, igual que en el plugin

### Requirement: Secuencia del estilo
La vista ampliada SHALL tener un botón que toque en bucle INTRO (p0/p1), BASE (p4/p5), ENERGÍA (p2/p3), VARIACIÓN (p6/p7) y FILL (p8, dos veces), saltando las partes vacías y marcando el patrón que suena.

#### Scenario: Estilo con FILL vacío
- **WHEN** se toca la secuencia de un estilo con p8 vacío
- **THEN** después de la VARIACIÓN vuelve a la INTRO sin compases en silencio

### Requirement: Mute y solo por voz
La vista ampliada SHALL tener un control de mute y otro de solo por cada una de las 7 voces. Con algún solo activo SHALL sonar solo las voces en solo. Mute y solo SHALL aplicarse al preview y al MIDI exportado.

#### Scenario: Solo de kick
- **WHEN** se activa el solo del kick y se exporta el MIDI
- **THEN** el archivo solo tiene notas de kick

### Requirement: Comparar dos estilos
La vista ampliada SHALL permitir elegir un segundo estilo y alternar la BASE de los dos cada dos compases, cada uno con su BPM y su swing.

#### Scenario: A/B
- **WHEN** en la vista ampliada de SALSA 180 se elige MAMBO 190 y se activa A/B
- **THEN** suenan dos compases de SALSA 180 a 180 BPM y dos de MAMBO 190 a 190 BPM, en bucle
