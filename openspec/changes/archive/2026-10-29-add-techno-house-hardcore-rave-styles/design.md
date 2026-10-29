## Context

- Cada patrón son 32 pasos, que con el Div por defecto equivalen a un compás de 4/4 en fusas. Una línea de 16 caracteres escribe semicorcheas.
- El plugin alterna p(2n) y p(2n+1) a cada compás, así que cada pareja (p4/p5, p2/p3…) forma una frase de 2 compases. p8 vale para los dos.
- Un paso suena si `256 − v < Density`. Con la escala de 5 niveles (`X=255 x=204 o=153 -=102 ,=51`), con Density por defecto (50) solo suena `X`, y cada nivel inferior entra al subir Density (>52, >103, >154, >205).
- La velocidad es fija por voz. El valor del paso solo decide si suena, no su volumen.
- El plugin no fija el tempo: el BPM va solo en el nombre. Por eso dos estilos con la misma rejilla suenan igual aunque su BPM sea distinto, y la diferencia tiene que estar en los golpes.
- El swing es global (50–75 %) con un amount por voz, y no se guarda en el estilo. Con swing 50 todo suena recto.

## Goals / Non-Goals

**Goals:**
- 42 estilos que se distingan entre sí y de los existentes con los valores por defecto (Density 50, pad en el centro).
- Que Density construya cada estilo por capas: ritmo esencial, luego adornos y fantasmas, luego redobles.

**Non-Goals:**
- Cambiar el plugin (velocidad por paso, tresillos, swing guardado en el estilo, frases de más de 2 compases).
- Reproducir una grabación concreta nota a nota.
- HARDSTYLE (igual que TRANCE 138 en la rejilla), DUB TECHNO (≈ MINIMAL TECHNO y GABBER), speedcore y frenchcore (solo cambian el BPM, que va en el nombre), schranz (≈ HARD TECHNO), jumpstyle, UK hardcore (≈ HAPPY HARDCORE y a 2 pasos de DETROIT TECHNO), bleep techno (a 4 de AFRO HOUSE 122), hardbass (≈ SCOUSE HOUSE) y futurepop (≈ TRANCE 138).

## Decisions

- **Escala de 5 niveles** (`X x o - ,`) y receta de groove (swing, amount por voz y slide) en un comentario de cabecera, como las cumbias y el drum & bass.
- **Reparto del pad** igual que las cumbias: p4/p5 BASE, p2/p3 ENERGÍA, p6/p7 VARIACIÓN, p0/p1 INTRO (hats y percusión, sin bombo ni caja completos) y p8 FILL (redoble de caja y toms).
- **Capas de Density:** el ritmo esencial en `X`; adornos, fantasmas y golpes extra en `x o - ,`, de más a menos importante.
- **Nombres en mayúsculas con el BPM** (`NOMBRE 120`), sin tildes ni eñes en el nombre de archivo, para no depender de cómo REAPER lee nombres no ASCII.
- **Distancia antes de escribir:** con un script de un solo uso (no se añade a `tools/`), comparar la rejilla `X` de cada BASE nueva con la de p4/p5 de todos los estilos existentes y de los otros estilos del cambio. Si dos coinciden en kick, snare y hats, se retoca la fuente nueva.
- **Uso de las voces:** kick = bombo; snare = caja o rim; clap = palmas o rim; hhc = hat cerrado o shaker; hho = hat abierto; hitom/lotom = toms (bucles en HARD TECHNO y UK TECHNO, adornos y fills en el resto).
- **Ritmo esencial (`X`) de cada BASE**, que es lo que distingue los estilos con Density por defecto:

  | Estilo | Kick | Snare / clap | Hats / toms |
  |---|---|---|---|
  | DETROIT TECHNO 128 | las cuatro negras | clap en 2 y 4 | hhc en semicorcheas; hho en cada "&" |
  | MINIMAL TECHNO 126 | las cuatro negras | rim (clap) en la "a" del 2 y la "e" del 4 | hhc en cada "&" |
  | HARD TECHNO 145 | las cuatro negras | clap en el "&" del 2 y del 4 | hhc en corcheas; hho en cada "a"; toms en semicorcheas (rumble) |
  | ACID TECHNO 140 | las cuatro negras | snare en 2 y 4; clap en el "&" del 4 | hhc en semicorcheas; hho en cada "&" |
  | UK TECHNO 135 | las cuatro negras | rim (snare) en el "&" del 1, la "a" del 2, el "&" del 3 y la "a" del 4 | hhc en cada "&"; toms en bucle (sonido Birmingham) |
  | DEEP HOUSE 122 | las cuatro negras | clap en 2 y 4 | shaker (hhc) en las "e" y las "a"; hho en cada "&" |
  | TECH HOUSE 126 | las cuatro negras | clap en 2 y 4; rims (snare) en la "a" del 1, el "&" del 3 y la "a" del 4 | hhc en semicorcheas, sin hho |
  | GHETTOTECH 150 | las cuatro negras y cada "a" | clap en las cuatro negras | hhc en corcheas |
  | ACID HOUSE 124 | las cuatro negras | clap en 2 y 4; snare en la "a" del 4 | hhc en las negras; hho en el "&" del 1 y del 3 |
  | ITALO HOUSE 122 | las cuatro negras | snare en 2 y 4; clap en la "a" del 2 y del 4 | hhc en las "e" y las "a"; hho en cada "&" |
  | GABBER 180 | las cuatro negras | nada en `X` | hho en cada "&"; los redobles de bombo solo entran con Density |
  | GABBER ROLL 180 | las cuatro negras; en el compás 2, redoble en la "e", el "&" y la "a" del 4 | nada en `X` | hho en cada "&" |
  | HAPPY HARDCORE 170 | las cuatro negras | snare en 2, la "a" del 2 y 4; clap en 2 y 4 | hho en cada "&"; hhc en las negras |
  | GOA TRANCE 145 | las cuatro negras | snare en el "&" del 1 y del 3; en el compás 2, redoble en la negra 4 | hhc en semicorcheas; hho en cada "&"; toms tribales |
  | FULL-ON 145 | las cuatro negras | nada en `X` | hho en cada "&"; hhc en cada "a" |
  | PROGRESSIVE PSY 138 | las cuatro negras | rim (clap) en la "a" del 2 y del 4 | hhc en las "e" y las "a" |
  | DARK PSY 150 | las cuatro negras | rim (snare) en la "a" del 1 y del 3 | hhc en semicorcheas; hho en cada "&" |
  | FOREST PSY 150 | las cuatro negras | rim (snare) en el "&" del 2; clap en la "e" del 4 | hhc en las "e" y las "a"; hho en cada "&"; toms y percusión orgánica en semicorcheas |
  | PSYCORE 190 | las cuatro negras y la "a" del 4 | snare en 2 y 4 | hhc en semicorcheas; hho en cada "a" |
  | ZENONESQUE 135 | las cuatro negras | rim (snare) en la "a" del 1, del 2 y del 3 | hhc en las "e" y las "a"; hho en el "&" del 4 |
  | MINIMAL PSY 140 | las cuatro negras | rim (snare) en la "e" del 3 y la "e" del 4 | hhc en cada "&"; hho en la "a" del 4 |
  | HI-TECH 180 | las cuatro negras | snare en la "e", el "&" y la "a" del 4 en cada compás (fusas con Density) | hho en cada "&"; hhc en cada "e" |
  | NITZHONOT 150 | las cuatro negras | snare y clap en 2 y 4 (con redobles de caja en p2/p3 y p8) | hhc en corcheas; hho en cada "&" |
  | SUOMISAUNDI 150 | las cuatro negras, más la "a" del 3 y el "&" del 4 | snare en 2 y 4; clap en el "&" del 3 | hho en cada "&"; hhc irregular (1, "a" del 1, "&" del 2, "e" del 3, "a" del 4) |
  | PSYBREAKS 135 | 1 y el "&" del 3 | snare en 2 y 4 | hhc en corcheas; hho en cada "&" |
  | PSYDUB 100 | solo la 1 | snare en el 3 (medio tiempo) | hho en cada "&"; hhc en la "a" del 1 y del 3 |
  | UK HARD HOUSE 150 | las cuatro negras | clap en 2 y 4; snare en la "e" y la "a" del 2 y del 4 | hhc en semicorcheas; hho en cada "&" |
  | HARD NRG 155 | las cuatro negras y el "&" del 4 | snare en 2, la "a" del 2, 4 y la "a" del 4 | hhc en semicorcheas; hho en cada "&" |
  | SCOUSE HOUSE 150 | las cuatro negras | clap en 2 y 4; snare en la "e" y la "a" del 1 y del 3 | hho en cada "&"; "donk" en hitom a contratiempo |
  | CHICAGO HARD HOUSE 135 | las cuatro negras | clap en 2, 4 y la "a" del 4; snare en el "&" del 1 y del 3 | hhc en semicorcheas; toms tribales |
  | DUTCH HOUSE 128 | las cuatro negras | clap en cada "&" | hhc en las negras |
  | EBM 120 | corcheas (bombo en cada corchea) | snare en 2 y 4 | hhc en las negras |
  | BELGIAN EBM 118 | 1, la "a" del 1, 3 y la "a" del 3 | snare y clap en 2 y 4 | hhc en las negras |
  | NEW BEAT 110 | las cuatro negras | snare en 2 y 4 | hhc en cada "a" |
  | AGGROTECH 140 | las cuatro negras, el "&" y la "a" del 4 | snare y clap en 2 y 4 | hhc en semicorcheas |
  | DARK ELECTRO 125 | 1, el "&" del 2 y el "&" del 3 | snare en el 3 (medio tiempo) | hhc en corcheas |
  | EBM TECHNO 130 | las cuatro negras | clap en 2 y 4; snare en el "&" del 2 y del 4 | hhc en las "e" y las "a" |
  | RAVE 91 130 | las cuatro negras | snare en 2, el "&" del 3 y 4 (break tipo Funky Drummer) | hhc en corcheas; hho en el "&" del 4 |
  | HARDCORE TECHNO 145 | las cuatro negras y la "a" del 4; en el compás 2 solo las negras | clap en 2 y 4; en el compás 2, redoble de snare en la negra 4 | hhc en semicorcheas |
  | BREAKBEAT HARDCORE 145 | las cuatro negras; en el compás 2 el kick sigue al break (1, 2, "&" del 3 y 4) | snare tipo amen: 2, la "a" del 2, la "e" del 3 y 4 | hhc en corcheas |
  | DARKCORE 155 | 1, la "a" del 2 y el "&" del 3 | snare en 2, 4 y el "&" del 4 | hhc en las "e" y las "a" |
  | DRILL N BASS 175 | 1, la "a" del 1 y el "&" y la "a" del 3, con dobles en fusas | redobles de fusas en las negras 2 y 4 de cada compás | hhc troceado (1, "&" del 1, 3 y "e" del 3) |

  En la tabla, "&" es la corchea a contratiempo, y "e" y "a" son la 2.ª y la 4.ª semicorchea de la negra.
- **Receta de groove** (cabecera de cada fuente): swing 56 en DEEP HOUSE (hhc), 54 en TECH HOUSE, ACID HOUSE e ITALO HOUSE (hhc), 52 en UK TECHNO, y 50 en el resto. Slide 0, salvo el snare de BREAKBEAT HARDCORE y DARKCORE (entre −3 y 0 ms, empuja).
- **Fila "Hard dance" → "Hardcore / hard dance"**: el hardcore merece su sección, junto a TRANCE y MAKINA. Se renombra la fila y se le añaden GABBER 180, GABBER ROLL 180 y HAPPY HARDCORE 170. Modifica el requisito de README de `hard-dance-styles`.
- **Fila nueva "Rave / oldskool"** para RAVE 91, HARDCORE TECHNO, BREAKBEAT HARDCORE y DARKCORE. Filas nuevas también para **Psytrance** (13 subgéneros), **Hard house** (5 variantes) y **EBM / industrial** (6 variantes). Los de techno y house van a sus filas existentes, y DRILL N BASS 175 a Breaks, junto a BREAKCORE 190. TRANCE 138 se queda en Hardcore / hard dance.
- **Dos variantes de GABBER**: GABBER 180 desnudo con Density por defecto (bombo y hho) y redobles de bombo por capas (semicorcheas en `x`, fusas en `o`), como la subida de TRANCE; GABBER ROLL 180 con el redoble ya en `X` al final del compás 2. Es la única pareja que se permite quedar cerca (3 pasos entre sí, y GABBER 180 a 4 de DISCO 118 y TRANCE 138).
- **HARDCORE TECHNO = hoover belga / R&S, 1991** (Joey Beltram, "Mentasm"): reúne "hardcore techno" y "Belgian hoover" en un solo estilo, en la fila Rave / oldskool.
- **ITALO HOUSE = piano house / Italo house** (1989–92): un solo estilo para los dos.
- **DRILL N BASS** (Aphex Twin, Squarepusher): breaks troceados con redobles de fusas en `X` en las negras 2 y 4 de cada compás, no solo al final como BREAKCORE 190. Líneas de 32 caracteres; Density añade más fusas.
- **EBM 120** es el único estilo con bombo en corcheas en `X` (estilo Nitzer Ebb / DAF).
- **Psytrance: lo que cambia es el bajo.** En el psy el bombo casi siempre va a negras y el bajo rodante lo pone el sintetizador. Los trece subgéneros se distinguen en la rejilla por los rims (DARK PSY, FOREST PSY, ZENONESQUE, MINIMAL PSY, PROGRESSIVE PSY), los redobles (GOA TRANCE, NITZHONOT, HI-TECH y PSYCORE, con fusas que entran con Density), el bombo con golpes de más (SUOMISAUNDI: según Wikipedia su única base fija es el bombo a negras, y lo raro va en fills y breaks) o roto (PSYBREAKS) y el medio tiempo (PSYDUB). FOREST PSY lleva además percusión orgánica en los toms; ZENONESQUE es el dark progressive de Zenon Records; NITZHONOT es el goa israelí de los 90, con caja y palmas en 2 y 4.
- **Hard house:** UK HARD HOUSE con caja en las "e" y "a", HARD NRG con doble bombo en el "&" del 4, SCOUSE HOUSE con el "donk" a contratiempo en hitom, CHICAGO HARD HOUSE con toms tribales y DUTCH HOUSE con palmas en cada contratiempo.
- **EBM:** EBM 120 (DAF, bombo en corcheas), BELGIAN EBM (Front 242), NEW BEAT (Bélgica, 1988, lento), AGGROTECH (bombo con doble al final), DARK ELECTRO (medio tiempo) y EBM TECHNO (techno de cuerpo actual).
- **Acid sin 303**: el plugin no toca la línea de bajo, así que ACID HOUSE y ACID TECHNO se distinguen por la batería de la 808/909 que los acompaña.
- **Distancia medida en el explore** con bocetos de la rejilla `X` (kick, snare, clap, hhc y hho por separado, p4/p5): todos quedan a 8 pasos o más de cualquier otro estilo salvo la pareja de GABBER. DRILL N BASS queda a 24 de SAMBASS 172, el más cercano. En psytrance, hard house y EBM se retocaron GOA TRANCE, MINIMAL PSY, PSYCORE, ZENONESQUE, SUOMISAUNDI, UK HARD HOUSE, HARD NRG, SCOUSE HOUSE, CHICAGO HARD HOUSE, BELGIAN EBM y EBM TECHNO, que en la primera versión quedaban a 4–7 pasos de otro estilo; el par más justo ahora es HARD NRG – ACID TECHNO 140 (8). Los pares más justos: MINIMAL TECHNO – AFRO HOUSE 122 (8), BREAKBEAT HARDCORE – JUNGLE 165 (8), RAVE 91 – SYNTHWAVE 100 (8), TECH HOUSE – HARDCORE TECHNO (9) e ITALO HOUSE – MAKINA 170 (9). ACID TECHNO, ITALO HOUSE, DARKCORE, HAPPY HARDCORE, PSYTRANCE, HARD HOUSE y EBM se retocaron porque la primera versión quedaba a 2–7 pasos de otro estilo (HARD HOUSE sin las semicorcheas de hhc quedaba a 6 de TRANCE 138).

## Risks / Trade-offs

- [Sin dinámica] Las fantasmas suenan a la velocidad de la voz. → Van en niveles bajos (`-`, `,`) para que solo entren con Density alta.
- [Parecido entre estilos] → Lo detecta la comprobación de distancia antes de escribir, y la escucha en REAPER después. Se retocan las fuentes, sin cambiar el plugin.
- [Interpretación musical] Se toma la gramática del género, no una grabación concreta. Las fuentes son texto plano y se regeneran en segundos.
- [Cambio grande] 42 estilos en un solo cambio. → Las tareas van por familia (se puede aplicar por bloques y comprobar cada uno), y la comprobación de distancia se repite con los `.txt` generados.
- [Conocimiento del género] UK TECHNO, HARDCORE TECHNO, DARKCORE, DRILL N BASS, SUOMISAUNDI, FOREST PSY, ZENONESQUE, NITZHONOT, SCOUSE HOUSE, DUTCH HOUSE, BELGIAN EBM y AGGROTECH se conocen menos. → Antes de escribirlos, consultar referencias escritas y anotar en la cabecera de la fuente de dónde sale el ritmo.
- [Todo a negras] Treinta y tres estilos tienen el mismo bombo. → Lo que los separa está en `X` (clap, hats, rims); la escucha en REAPER tiene que confirmar que se distinguen.

## Verificación en REAPER

1. `sh tools/install.sh`.
2. Para cada estilo: pad en (0,0), Density y Div por defecto, y el swing de la receta. Grabar la salida MIDI del plugin durante 2 compases.
3. Comprobar que las notas de p4 y p5 caen donde marcan los `X` de la fuente.
4. Subir Density por encima de 52, 103, 154 y 205, y comprobar que en cada escalón se añade el nivel siguiente sin quitar golpes.
5. Escuchar los estilos del cambio seguidos y comprobar que se distinguen entre sí y del estilo existente más parecido.
