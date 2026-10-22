## ADDED Requirements

### Requirement: Slide por voz en milisegundos
Cada una de las 7 voces SHALL tener un parámetro slide de −30 a +30 ms (por defecto 0) que desplaza en el tiempo todas sus notas. Se suma después del swing: `t = warp(t_recto) + slide`.

#### Scenario: Slide positivo
- **WHEN** el slide del snare vale +20 ms
- **THEN** cada nota del snare suena 20 ms después de su tiempo con swing

#### Scenario: Slide independiente del tempo
- **WHEN** el tempo cambia de 120 a 140 BPM con un slide de +20 ms
- **THEN** el desplazamiento sigue siendo de 20 ms

### Requirement: Slide negativo mediante lookahead
Un slide negativo SHALL adelantar las notas respecto a su tiempo con swing. Para ello los pasos se evalúan con antelación suficiente para cubrir −30 ms.

#### Scenario: Hats adelantados durante la reproducción continua
- **WHEN** el slide del hh cerrado vale −15 ms y el transporte reproduce sin saltos
- **THEN** cada nota del hh cerrado suena 15 ms antes de su tiempo con swing

#### Scenario: Primer paso tras un salto
- **WHEN** el transporte salta (loop o seek) y el tiempo adelantado del primer paso queda antes del inicio del bloque actual
- **THEN** esa nota suena al inicio del bloque (offset 0) y las siguientes vuelven a salir adelantadas

#### Scenario: Inicio de loop con slide negativo
- **WHEN** una voz con slide negativo ya adelantó el paso del final del loop antes de que el transporte vuelva al inicio
- **THEN** ese golpe adelantado cuenta como el inicio del loop y el paso del inicio no se repite (un solo golpe)
