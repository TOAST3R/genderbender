## Context

- Cada patrón son 32 pasos, que con el Div por defecto equivalen a un compás de 4/4 en fusas. Una línea de 16 caracteres escribe semicorcheas.
- El plugin alterna p(2n) y p(2n+1) a cada compás, así que cada pareja (p4/p5, p2/p3…) forma una frase de 2 compases. p8 vale para los dos.
- Un paso suena si `256 − v < Density`. Con la escala de 5 niveles (`X=255 x=204 o=153 -=102 ,=51`), con Density por defecto (50) solo suena `X`, y cada nivel inferior entra al subir Density (>52, >103, >154, >205).
- La velocidad es fija por voz. El valor del paso solo decide si suena, no su volumen.
- El plugin no fija el tempo: el BPM va solo en el nombre. Por eso dos estilos con la misma rejilla suenan igual aunque su BPM sea distinto, y la diferencia tiene que estar en los golpes.
- El swing es global (50–75 %) con un amount por voz, y no se guarda en el estilo. Con swing 50 todo suena recto.

## Goals / Non-Goals

**Goals:**
- 20 estilos que se distingan entre sí y de los existentes con los valores por defecto (Density 50, pad en el centro).
- Que Density construya cada estilo por capas: ritmo esencial, luego adornos y fantasmas, luego redobles.

**Non-Goals:**
- Cambiar el plugin (velocidad por paso, tresillos, swing guardado en el estilo, frases de más de 2 compases).
- Reproducir una grabación concreta nota a nota.
- MELODIC TECHNO, lovers rock (≈ ROOTS REGGAE), raggamuffin (≈ DIGITAL DANCEHALL), ska-punk y reggae fusion: en este plugin sonarían como otro estilo.

## Decisions

- **Escala de 5 niveles** (`X x o - ,`) y receta de groove (swing, amount por voz y slide) en un comentario de cabecera, como las cumbias y el drum & bass.
- **Reparto del pad** igual que las cumbias: p4/p5 BASE, p2/p3 ENERGÍA, p6/p7 VARIACIÓN, p0/p1 INTRO (hats y percusión, sin bombo ni caja completos) y p8 FILL (redoble de caja y toms).
- **Capas de Density:** el ritmo esencial en `X`; adornos, fantasmas y golpes extra en `x o - ,`, de más a menos importante.
- **Nombres en mayúsculas con el BPM** (`NOMBRE 120`), sin tildes ni eñes en el nombre de archivo, para no depender de cómo REAPER lee nombres no ASCII.
- **Distancia antes de escribir:** con un script de un solo uso (no se añade a `tools/`), comparar la rejilla `X` de cada BASE nueva con la de p4/p5 de todos los estilos existentes y de los otros estilos del cambio. Si dos coinciden en kick, snare y hats, se retoca la fuente nueva.
- **Uso de las voces:** kick = bombo; snare = caja o rim; clap = palmas o cross-stick (rim en el reggae); hhc = hat cerrado o shaker; hho = hat abierto o el skank (ska); hitom/lotom = toms, percusión tribal y eco de dub en los fills.
- **Ritmo esencial (`X`) de cada BASE**, que es lo que distingue los estilos con Density por defecto:

  | Estilo | Kick | Snare / clap | Hats / toms |
  |---|---|---|---|
  | SPEED GARAGE 135 | las cuatro negras y el "&" del 4 | snare en 2, el "&" del 3 y 4 | hhc en las "e" y las "a"; hho en cada "&" |
  | BASSLINE 138 | las cuatro negras | clap en 2 y 4; snare en el "&" del 2 y del 4 | hhc en semicorcheas; hho en el "&" del 1 y del 3 |
  | BREAKSTEP 140 | 1, el "&" y la "a" del 3 | snare en el 3 y el "&" del 4 | hhc en 3-3-2 (1, "a" del 1, "&" del 2, 3, "a" del 3, "&" del 4) |
  | WONKY 140 | 1, la "e" del 2 y la "a" del 3 | snare y clap en el 3 | hhc torcido ("&" del 1, "a" del 2, "e" del 3, "&" del 4) |
  | BLEEP TECHNO 122 | las cuatro negras | clap en el 4; snare en el "&" del 2 | hhc en las negras |
  | AMBIENT TECHNO 120 | las cuatro negras | nada en `X` | hhc en la "a" del 1 y del 3; hho en el "&" del 2 |
  | TRIBAL TECHNO 130 | las cuatro negras | clap solo en el 4 | hhc en semicorcheas; hho en la "a" del 1 y del 3; toms tribales |
  | DEEP TECHNO 124 | las cuatro negras | rim (snare) en la "a" del 2 y la "e" del 4 | hhc en el "&" del 1, la "e" del 2, el "&" del 3 y la "e" del 4; hho en el "&" del 4 |
  | HYPNOTIC TECHNO 130 | las cuatro negras | rim (snare) en la "a" del 1 y del 3 | hhc en el "&" del 1, la "e" del 2, el "&" del 3 y la "e" del 4 |
  | PEAK TIME TECHNO 132 | las cuatro negras | clap en 2 y 4 | hhc en el "&" y la "a" de cada negra; hho en cada "&" |
  | INDUSTRIAL TECHNO 140 | las cuatro negras | snare (golpe metálico) en el "&" del 1 y del 3 | hho en el "&" del 2 y del 4; hhc en cada "e" |
  | SKA 120 | 1 y 3 | snare (rim) en 2 y 4 | hho en cada "&" (el skank); hhc en las negras |
  | ROCKSTEADY 80 | solo en el 3 | rim (clap) en 2 y 4 | hhc en corcheas; hho en el "&" del 2 y del 4 |
  | ROOTS REGGAE 75 | solo en el 3 (one drop) | rim (clap) en el 3 | hhc en semicorcheas; hho en el "&" del 2 y del 4 |
  | DUB 70 | solo en el 3 | snare en el 3 | hho en el "&" del 1 y del 3; toms y eco en los fills |
  | ROCKERS 80 | 1 y 3 | rim (clap) en el 3 | hhc en semicorcheas; hho en cada "a" |
  | STEPPERS 75 | las cuatro negras | snare y rim en el 3 | hhc en cada "&" |
  | TWO TONE 160 | 1, el "&" del 1, 2, 3, el "&" del 3 y 4 | snare en 2 y 4 | hhc en corcheas; hho en cada "&" |
  | DIGITAL DANCEHALL 95 | 1, la "a" del 1, el "&" del 2, 3, la "a" del 3 y el "&" del 4 (3-3-2 doble) | snare en 2 y 4 | hhc en corcheas |
  | MODERN DANCEHALL 100 | 1, el "&" del 2 y el "&" del 3 | clap en 2 y 4; rim (snare) en la "a" del 2 y del 4 | hhc en cada "&" |

  En la tabla, "&" es la corchea a contratiempo, y "e" y "a" son la 2.ª y la 4.ª semicorchea de la negra.
- **Receta de groove** (cabecera de cada fuente): swing 58 en SPEED GARAGE, ROCKSTEADY, ROOTS REGGAE y DUB (hats); 56 en BASSLINE y ROCKERS; 54 en BREAKSTEP, SKA y STEPPERS; 52 en DEEP TECHNO, HYPNOTIC TECHNO y MODERN DANCEHALL; y 50 en el resto. El preview de la página de huellas lee esta receta.
- **Fila "UK garage"** (antes "UK garage / 2-step") con las filas Grime y Dubstep dentro, en el orden de la lista pedida: 2-step (garage_2step, Two-stepppo), SPEED GARAGE, BASSLINE, grime (GRIME140, Grimer140), dubstep (DUBSTEP140, DubSteppo, 101 STEPPA, RIDDIM 140), UK funky (uk_fungui), FUTURE GARAGE, 4x4 (garage_uk_4x4, uk_garbage), BREAKSTEP y WONKY. Desaparecen las filas "Grime" y "Dubstep". Ninguna spec nombra esas filas.
- **Fila "Techno" en orden cronológico, clásicos primero**: DETROIT TECHNO (1985–88), BLEEP TECHNO (Sheffield, 1990), AMBIENT TECHNO (1991–92), UK TECHNO (Birmingham, 1993), MINIMAL TECHNO, DUB TECHNO, HARDGROOVE, TRIBAL TECHNO, ACID TECHNO (mediados de los 90), SCHRANZ (finales de los 90), SCHAFFEL (2000s), DEEP TECHNO, HYPNOTIC TECHNO, PEAK TIME TECHNO, INDUSTRIAL TECHNO, HARD TECHNO (2010s–2020s), y al final los originales del editor: techAXX, TekkBooooring, TekkChungo, TekkThump. La página de huellas muestra los estilos en el orden de la tabla.
- **Fila nueva "Reggae / dancehall"**, también en orden cronológico: SKA, ROCKSTEADY, ROOTS REGGAE, DUB, ROCKERS, STEPPERS, TWO TONE, DIGITAL DANCEHALL, 101 DANCEHALL (que sale de la fila de reggaeton) y MODERN DANCEHALL. La fila "Reggaeton / dancehall" pasa a llamarse "Reggaeton / funk carioca" (101 RAGATON, 101 FUNK FAVELA, DEMBOW 120, FUNK DE RAIZ 130).
- **El reggae en 32 pasos**: un compás de one drop a 75 BPM cabe en el patrón como cualquier otro; el bombo y el rim en la negra 3 son lo que lo define, y el swing de la receta da el balanceo de los hats.
- **Sin patrones repetidos**: como pide `dedupe-generated-patterns`, ningún p6, p7 ni p8 puede repetir el de otro estilo generado. Esta vez VARIACIÓN y FILL se derivan de la propia base de cada estilo (su voz de caja, sus toms, su bombo), y se comprueba antes de generar; si aun así alguno coincide, se deja vacío.
- **Distancia medida** con bocetos de la rejilla `X` (kick, snare, clap, hhc y hho por separado, p4/p5): los 20 quedan a 8 pasos o más de cualquier otro estilo. Se retocaron SPEED GARAGE (4 de DEEP HOUSE 122), BASSLINE (4 de ITALO DISCO 120), BREAKSTEP (7 de UK DRILL 142), TRIBAL TECHNO (2 de AFRO HOUSE 122), SKA (4 de TRANCE 138), TWO TONE (4 de garage_uk_4x4), ROCKSTEADY, ROCKERS, STEPPERS y MODERN DANCEHALL. MELODIC TECHNO quedó fuera: a 2 de SPEED GARAGE, y su identidad está en los sintes.

## Risks / Trade-offs

- [Sin dinámica] Las fantasmas suenan a la velocidad de la voz. → Van en niveles bajos (`-`, `,`) para que solo entren con Density alta.
- [Parecido entre estilos] → Lo detecta la comprobación de distancia antes de escribir, y la escucha en REAPER después. Se retocan las fuentes, sin cambiar el plugin.
- [Interpretación musical] Se toma la gramática del género, no una grabación concreta. Las fuentes son texto plano y se regeneran en segundos.
- [Conocimiento del género] BREAKSTEP, WONKY, BLEEP TECHNO, HYPNOTIC TECHNO, ROCKERS, STEPPERS, DIGITAL DANCEHALL y TWO TONE se conocen menos. → Consultar referencias escritas antes de escribirlos y anotarlas en la cabecera.
- [Cambio en paralelo] `add-fingerprints-audio-preview` sigue abierto y también toca el README (los BPM de la tabla). → Este cambio se aplica encima; las entradas conservan su `(bpm)`.

## Verificación en REAPER

1. `sh tools/install.sh`.
2. Para cada estilo: pad en (0,0), Density y Div por defecto, y el swing de la receta. Grabar la salida MIDI del plugin durante 2 compases.
3. Comprobar que las notas de p4 y p5 caen donde marcan los `X` de la fuente.
4. Subir Density por encima de 52, 103, 154 y 205, y comprobar que en cada escalón se añade el nivel siguiente sin quitar golpes.
5. Escuchar los estilos del cambio seguidos y comprobar que se distinguen entre sí y del estilo existente más parecido.
