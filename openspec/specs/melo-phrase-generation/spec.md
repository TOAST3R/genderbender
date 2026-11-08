# melo-phrase-generation Specification

## Purpose
Hace que la generación suene a frases musicales: cada voz genera motivos, los recuerda, los varía según una forma de frase y evoluciona con el tiempo, con opción de congelar el resultado y repetirlo de forma exacta.

## Requirements

### Requirement: Motivo generado y recordado
Al empezar una frase, cada voz SHALL generar un motivo de dos compases (el par de patrones, como en gb_18): qué pasos suenan y qué alturas tocan, a partir de su estilo, el pad y la densidad. El motivo SHALL guardarse y reutilizarse dentro de la frase en lugar de volver a sortearse. Una frase SHALL tener 4 motivos (8 compases).

#### Scenario: Repetición dentro de la frase
- **WHEN** la forma de frase es AAAA y la evolución vale 0
- **THEN** los cuatro motivos de la frase (compases 1–2, 3–4, 5–6 y 7–8) tocan el mismo ritmo y el mismo contorno

### Requirement: Forma de frase
Cada estilo SHALL declarar una forma de frase por voz (por ejemplo AA'AB, ABAB, AAAA). `A` SHALL ser el motivo, `A'` una variación leve y `B` una respuesta generada que termina en nota del acorde.

#### Scenario: Respuesta
- **WHEN** la forma es AA'AB
- **THEN** el cuarto motivo (compases 7–8) es distinto de A y su última nota es nota del acorde

### Requirement: Variación sobre el contorno
Las variaciones SHALL conservar el ritmo y la forma del motivo y cambiar como mucho un tercio de sus notas: añadir o quitar notas de paso, invertir el último salto o desplazar el contorno un grado.

#### Scenario: Variación leve
- **WHEN** se genera A' a partir de un motivo de 6 notas
- **THEN** A' cambia 2 notas como mucho y conserva los pasos de los tiempos fuertes

### Requirement: Re-armonización del motivo
Si el acorde cambia mientras se repite un motivo, sus alturas SHALL recalcularse sobre el acorde y la escala nuevos, conservando el contorno.

#### Scenario: Motivo sobre otro acorde
- **WHEN** el motivo A se generó sobre i y se repite sobre iv
- **THEN** el bajo y la melodía siguen el mismo contorno, transportado a las notas de iv

### Requirement: Evolución
Un control de evolución (0–100) SHALL fijar qué proporción del motivo se regenera al empezar cada frase. Con 0 el motivo SHALL repetirse sin cambios y con 100 SHALL generarse uno nuevo en cada frase.

#### Scenario: Evolución 0
- **WHEN** la evolución vale 0
- **THEN** todas las frases usan el mismo motivo A

### Requirement: Lock por voz
Cada voz SHALL tener un lock. Con el lock activo, la voz SHALL dejar de generar y repetir la frase actual, re-armonizada sobre los acordes. Mover el pad o cambiar la densidad SHALL dejar de afectar a esa voz mientras el lock esté activo.

#### Scenario: Lock activo y pad en movimiento
- **WHEN** la melodía tiene el lock activo y se mueve el pad
- **THEN** la melodía repite la frase bloqueada

#### Scenario: Lock guardado
- **WHEN** se guarda y se vuelve a abrir un proyecto con una voz bloqueada
- **THEN** la voz toca la misma frase bloqueada

### Requirement: Semilla reproducible
El plugin SHALL tener una semilla que se guarda en el proyecto y el preset. Con la misma semilla, el mismo estado de los controles y el transporte reproduciendo desde el mismo punto, SHALL generar exactamente las mismas notas.

#### Scenario: Reapertura del proyecto
- **WHEN** se reproduce un proyecto desde el inicio, se cierra, se vuelve a abrir y se reproduce otra vez desde el inicio
- **THEN** las dos grabaciones de MIDI son idénticas
