# melo-voices Specification

## Purpose
Describe cómo cada una de las tres voces (bajo, acordes y melodía) decide cuándo suena y qué notas toca a partir de su estilo, del pad XY y de la armonía común.

## Requirements

### Requirement: Género por voz
Cada voz SHALL tener su propio selector de estilo entre los estilos de `melo_styles/`. El estilo de una voz SHALL aportar sus patrones de ritmo, altura y articulación.

#### Scenario: Estilo distinto por voz
- **WHEN** el bajo usa ACID HOUSE y la melodía usa CUMBIA COLOMBIANA
- **THEN** el bajo toca los patrones de ACID HOUSE y la melodía los de CUMBIA COLOMBIANA

### Requirement: Ritmo por densidad
Cada paso SHALL sonar según su valor de ritmo (0–255) comparado con la densidad de la voz, con la misma regla que gb_18. Con la densidad por defecto solo SHALL sonar el nivel `X`.

#### Scenario: Densidad por defecto
- **WHEN** la densidad está en su valor por defecto
- **THEN** solo suenan los pasos con valor 255

### Requirement: Pad XY global con peso por voz
Un único pad XY SHALL mezclar los 9 patrones de cada voz con la misma geometría de esquinas y cuadrantes que gb_18. Cada voz SHALL tener un peso de pad (0–100). Con peso 0 la voz SHALL tocar siempre su BASE (p4 en el compás 1 y p5 en el compás 2, como el centro del pad de gb_18), y con peso 100 la posición completa del pad.

#### Scenario: Bajo fijo
- **WHEN** el peso de pad del bajo vale 0 y se mueve el pad
- **THEN** el bajo sigue tocando su BASE (p4/p5) y los acordes y la melodía cambian

### Requirement: Altura mezclada por sorteo ponderado
Al mezclar patrones, el ritmo SHALL interpolarse de forma bilineal. La altura y la articulación de cada paso SHALL sortearse entre las de las esquinas activas, con probabilidad igual a su peso bilineal.

#### Scenario: Pad en una esquina
- **WHEN** el pad está exactamente en una esquina
- **THEN** la altura de cada paso es siempre la de ese patrón

### Requirement: Bajo relativo al acorde
El bajo SHALL tocar una nota monofónica calculada a partir del grado del paso sobre el acorde actual, en la octava elegida por el usuario. La aproximación `a` SHALL tocar la nota a un semitono de la fundamental del acorde siguiente.

#### Scenario: Quinta sobre el IV
- **WHEN** la tónica es A menor, el acorde actual es iv (Dm) y el paso pide `5`
- **THEN** el bajo toca A

### Requirement: Acordes con voicing
La voz de acordes SHALL construir el acorde actual con el tipo de voicing del paso, sobre la escala vigente, con voice leading: SHALL elegir la inversión que mueva menos las notas respecto al acorde anterior, dentro del registro de la voz.

#### Scenario: Voice leading
- **WHEN** el acorde pasa de Am a Dm en triada
- **THEN** se toca la inversión de Dm con menos movimiento total de semitonos desde Am

### Requirement: Strum
La voz de acordes SHALL tener un control de strum (0–50 ms) que reparte los NoteOn de un acorde de grave a agudo.

#### Scenario: Strum a 20 ms
- **WHEN** el strum vale 20 ms y suena una triada
- **THEN** las tres notas empiezan con 10 ms de separación entre sí

### Requirement: Melodía por contorno
La melodía SHALL moverse por la escala vigente según el contorno de cada paso. En los tiempos fuertes SHALL ajustar la nota a la nota del acorde más cercana. Un control de salto máximo SHALL limitar el intervalo entre notas consecutivas.

#### Scenario: Tiempo fuerte
- **WHEN** el contorno lleva la melodía a una nota que no es del acorde en el primer tiempo de un compás
- **THEN** la melodía toca la nota del acorde más cercana

#### Scenario: Registro
- **WHEN** el contorno sube varias veces seguidas hasta pasar el límite superior del registro
- **THEN** la melodía salta una octava abajo en lugar de salirse del registro

### Requirement: Controles por voz
Cada voz SHALL tener controles de densidad, octava (−2 a +2), duración, velocidad, swing y slide, como en gb_18. La duración SHALL ignorarse en los pasos ligados.

#### Scenario: Octava
- **WHEN** la octava del bajo vale −1
- **THEN** todas las notas del bajo suenan 12 semitonos más graves

### Requirement: Swing global
El plugin SHALL tener un swing global (50–75) con cantidad por voz, aplicado con la misma regla que gb_18.

#### Scenario: Swing neutro
- **WHEN** el swing global vale 50
- **THEN** ninguna nota se desplaza
