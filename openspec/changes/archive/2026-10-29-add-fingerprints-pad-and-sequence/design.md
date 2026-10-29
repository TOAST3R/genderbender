## Context

- El plugin calcula el sector del pad en este orden (`genderbender.jsfx`, líneas 766–769), y **la última condición que se cumple gana**:
  1. `x < 0 && y < 0` → sector 1
  2. `x < 0 && y > 0` → sector 2
  3. `x >= 0 && y >= 0` → sector 3
  4. `x >= 0 && y <= 0` → sector 4

  En (0, 0) se cumplen la 3 y la 4, así que el centro es el sector 4. Con `x < 0` e `y = 0` no se cumple ninguna y el sector se queda como estaba.
- Con `X = |x| / 100` e `Y = |y| / 100`, cada voz mezcla los valores de cuatro patrones (`sb` = 0 en el compás 1 y 1 en el 2), según las líneas 501–504:
  - sector 1: `(p[0+sb]·X + p[2+sb]·(1−X))·Y + (p[4+sb]·X + p[6+sb]·(1−X))·(1−Y)`
  - sector 2: `(p[0+sb]·X + p[4+sb]·(1−X))·Y + (p[6+sb]·X + p[8]·(1−X))·(1−Y)`
  - sector 3: `(p[0+sb]·(1−X) + p[2+sb]·X)·(1−Y) + (p[8]·(1−X) + p[6+sb]·X)·Y`
  - sector 4: `(p[0+sb]·(1−X) + p[8]·X)·Y + (p[4+sb]·(1−X) + p[2+sb]·X)·(1−Y)`

  El valor mezclado suena si `256 − v < Density`.
- Esto deja el mapa del pad: centro = p4/p5 (BASE), derecha = p2/p3 (ENERGÍA), abajo = p0/p1 (INTRO), abajo-derecha = p8 (FILL), arriba-derecha = p6/p7 (VARIACIÓN). **El pad no es continuo en el centro**: justo encima (y > 0) se pasa al sector 3, que en (0, 0⁺) da sobre todo p0/p1. La página lo reproduce tal cual.
- El preview de la página ya tiene planificador con look-ahead, Density, swing por estilo y una sola reproducción a la vez.

## Goals / Non-Goals

**Goals:**
- Oír en la página lo mismo que el plugin con el pad en cualquier punto.
- Oír el estilo entero, una voz suelta, o dos estilos seguidos.

**Non-Goals:**
- Corregir la discontinuidad del pad en el plugin (sería un cambio del plugin).
- Los breaks y el random del plugin.

## Decisions

- **Fórmula copiada, no reinterpretada**: una función `padMix(st, voz, paso, compás, x, y)` con el mismo orden de condiciones y las mismas cuatro fórmulas, y una prueba que la compara con la lectura directa de p4/p5 en el centro y de p2/p3, p0/p1 y p8 en los bordes.
- **El pad se lee en cada paso** del planificador, así que arrastrarlo cambia lo que suena al momento, como Density.
- **Secuencia** de 2 compases por parte (p8 se repite dos veces), saltando las partes vacías; el borde de acento marca el patrón que suena.
- **Mute/solo**: siete botones, uno por voz; con algún solo activo suenan solo los solos. Afecta al preview y al MIDI.
- **A/B**: un selector con todos los estilos en la vista ampliada; al activarlo se alternan A y B cada dos compases, cada uno con su BPM y su swing.

## Risks / Trade-offs

- [Discontinuidad visible] Un usuario puede pensar que el pad de la página está mal al oír el salto encima del centro. → Una nota bajo el pad lo explica: "como en el plugin".
- [Tiempo entre estilos en A/B] Si A y B tienen BPM distintos, el cambio se hace al final del par de compases, sin solapar.

## Verificación

No toca el plugin. En un navegador (Playwright): con el pad en (0, 0) las notas programadas son las de p4/p5; en (100, 0) las de p2/p3; en (0, −100) las de p0/p1; en (100, −100) las de p8; en (0, 1) suena sobre todo p0/p1 (la discontinuidad); la secuencia recorre las partes no vacías en orden; un solo deja sonar solo esa voz; A/B alterna dos estilos con sus BPM. A mano: comparar con REAPER moviendo el pad al mismo punto.
