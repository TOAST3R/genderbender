# Spec Delta

## Purpose

Fija los estilos melódicos incluidos en la v1 y el carácter musical que cada uno debe tener, con nombres tomados de los estilos de batería de gb_18.

## ADDED Requirements

### Requirement: Estilos de la v1
`melo_styles/` SHALL incluir 6 estilos: CUMBIA COLOMBIANA, ROOTS REGGAE, ACID HOUSE, BULERIA, LIQUID DNB y SON. Cada nombre SHALL coincidir con un estilo de batería de gb_18 sin su BPM, y su BPM declarado SHALL ser el del estilo de batería.

#### Scenario: Lista completa
- **WHEN** se ejecuta el validador
- **THEN** encuentra los 6 estilos y todos son válidos

### Requirement: Cada estilo cubre los modos de progresión
Cada estilo SHALL declarar al menos 3 progresiones en su banco, una tabla de Markov que cubra cada acorde del banco y al menos una sustitución para un acorde del banco.

#### Scenario: Modo Markov con cualquier estilo
- **WHEN** cualquiera de los 6 estilos es el maestro y el modo es Markov
- **THEN** cada acorde tiene al menos un sucesor posible

### Requirement: CUMBIA COLOMBIANA
SHALL usar menor natural o armónica con progresiones del tipo i–iv–V7–i. El bajo SHALL tocar fundamental y quinta en los tiempos 1 y 3, con anticipación. Los acordes SHALL marcar el contratiempo. La melodía SHALL moverse por grados en corcheas.

#### Scenario: Patrón central del bajo
- **WHEN** CUMBIA COLOMBIANA suena en su BASE (p4/p5) con densidad por defecto
- **THEN** el bajo toca R en el tiempo 1 y 5 en el tiempo 3

### Requirement: ROOTS REGGAE
SHALL usar menor o dórica con progresiones de 2 acordes (i–iv, i–VII). El bajo SHALL evitar el primer tiempo del compás (one drop) y dejar silencios. Los acordes SHALL sonar cortos en los tiempos 2 y 4 (skank).

#### Scenario: Skank
- **WHEN** ROOTS REGGAE suena en su BASE (p4/p5)
- **THEN** los acordes suenan solo en los tiempos 2 y 4 y con duración corta

### Requirement: ACID HOUSE
SHALL usar menor o frigia sobre 1 o 2 acordes. El bajo SHALL tocar semicorcheas con acentos y slides. Los acordes SHALL ser stabs escasos de 7ª menor. La melodía SHALL ser escasa.

#### Scenario: Línea 303
- **WHEN** ACID HOUSE suena en su BASE (p4/p5) con densidad por defecto
- **THEN** el bajo tiene al menos 2 pasos con slide en el compás

### Requirement: BULERIA
SHALL ser ternario, en frigia dominante sobre la tónica (E por defecto), con la cadencia andaluza iv–bIII–bII–I (Am–G–F–E con tónica E) como primera progresión del banco. Los acordes SHALL rasguear con strum y acentos en el compás de 12 tiempos agrupados. La melodía SHALL incluir el semitono b2–1.

#### Scenario: Cadencia andaluza
- **WHEN** BULERIA es el maestro en modo fija con su primera progresión
- **THEN** los acordes son iv–bIII–bII–I sobre la tónica elegida (Am–G–F–E con tónica E)

### Requirement: LIQUID DNB
SHALL usar acordes de 7ª mayor y 9ª menor con progresiones ii–V–I y similares. El bajo SHALL sostener notas largas ligadas. Los acordes SHALL sonar largos. La melodía SHALL arpegiar.

#### Scenario: Bajo ligado
- **WHEN** LIQUID DNB suena en su BASE (p4/p5)
- **THEN** la mayoría de las notas del bajo son ligadas y duran al menos una negra

### Requirement: SON
SHALL usar mayor o menor con ii–V–I e I–IV–V. El bajo SHALL tocar el tumbao: anticipación en el "y" del 2 y en el 4, sin atacar el primer tiempo. Los acordes SHALL tocar un montuno sincopado.

#### Scenario: Tumbao
- **WHEN** SON suena en su BASE (p4/p5) con densidad por defecto
- **THEN** el bajo no ataca el tiempo 1 y suena en el "y" del 2 y en el 4
