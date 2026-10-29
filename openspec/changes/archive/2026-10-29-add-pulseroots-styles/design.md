## Context

- Cada patrón son 32 pasos, que con el Div por defecto equivalen a un compás de 4/4 en fusas. Una línea de 16 caracteres escribe semicorcheas.
- El plugin alterna p(2n) y p(2n+1) a cada compás, así que cada pareja (p4/p5, p2/p3…) forma una frase de 2 compases. p8 vale para los dos.
- Un paso suena si `256 − v < Density`. Con la escala de 5 niveles (`X=255 x=204 o=153 -=102 ,=51`), con Density por defecto (50) solo suena `X`, y cada nivel inferior entra al subir Density (>52, >103, >154, >205).
- La velocidad es fija por voz. El valor del paso solo decide si suena, no su volumen.
- El plugin no fija el tempo: el BPM va solo en el nombre. Por eso dos estilos con la misma rejilla suenan igual aunque su BPM sea distinto, y la diferencia tiene que estar en los golpes.
- El swing es global (50–75 %) con un amount por voz, y no se guarda en el estilo. Con swing 50 todo suena recto.

## Goals / Non-Goals

**Goals:**
- 31 estilos que se distingan entre sí y de los existentes con los valores por defecto (Density 50, pad en el centro).
- Que Density construya cada estilo por capas: ritmo esencial, luego adornos y fantasmas, luego redobles.

**Non-Goals:**
- Cambiar el plugin (velocidad por paso, tresillos, swing guardado en el estilo, frases de más de 2 compases).
- Reproducir una grabación concreta nota a nota.
- Los ~130 subgéneros de PulseRoots que solo cambian el sonido respecto a un estilo existente, los ~60 sin batería, y los que piden tresillos o dinámica real (jazzstep, drumfunk, witch house, hyperpop).

## Decisions

- **Escala de 5 niveles** (`X x o - ,`) y receta de groove (swing, amount por voz y slide) en un comentario de cabecera, como las cumbias y el drum & bass.
- **Reparto del pad** igual que las cumbias: p4/p5 BASE, p2/p3 ENERGÍA, p6/p7 VARIACIÓN, p0/p1 INTRO (hats y percusión, sin bombo ni caja completos) y p8 FILL (redoble de caja y toms).
- **Capas de Density:** el ritmo esencial en `X`; adornos, fantasmas y golpes extra en `x o - ,`, de más a menos importante.
- **Nombres en mayúsculas con el BPM** (`NOMBRE 120`), sin tildes ni eñes en el nombre de archivo, para no depender de cómo REAPER lee nombres no ASCII.
- **Distancia antes de escribir:** con un script de un solo uso (no se añade a `tools/`), comparar la rejilla `X` de cada BASE nueva con la de p4/p5 de todos los estilos existentes y de los otros estilos del cambio. Si dos coinciden en kick, snare y hats, se retoca la fuente nueva.
- **Uso de las voces:** kick = bombo u 808; snare = caja, rim o tarola; clap = palmas, rim o clave; hhc = hat cerrado o shaker; hho = hat abierto o ride; hitom = cencerro (phonk, hardgroove) o tom; lotom = tom o cola del bombo (hardstyle).
- **Ritmo esencial (`X`) de cada BASE**, que es lo que distingue los estilos con Density por defecto:

  | Estilo | Kick | Snare / clap | Hats / toms |
  |---|---|---|---|
  | GLITCH HOP 110 | 1 y el "&" del 3 | snare en el 3 y la "a" del 4 (tartamudeos de fusas en `x`/`o`) | hhc en las "e" y las "a"; hho en el "&" del 2 |
  | IDM 120 | 1, la "a" del 1, el "&" del 2 y la "a" del 3 | snare en 2, la "e" del 3 y el "&" del 4 | hhc irregular (1, "&" del 1, "e" del 2, 3, "e" del 4) |
  | SKWEEE 100 | 1, la "a" del 2 y 3 | snare en 2 y 4 | hhc en cada "&" |
  | DECONSTRUCTED CLUB 130 | 1, la "e" del 2 y la "a" del 3 | clap (disparo) en la "a" del 1 y la "e" del 3 | hho en el "&" del 4; sin hats regulares |
  | MICROHOUSE 124 | las cuatro negras | rims (snare) en la "e" del 1, el "&" del 2 y la "a" del 3 | hhc en cada "a" |
  | DUB TECHNO 118 | las cuatro negras | clap en el "&" del 2 y la "e" del 3 (eco del acorde) | hho en la "a" del 1 y del 3 |
  | SCHRANZ 150 | las cuatro negras | clap en cada "&" | hhc en semicorcheas; toms en bucle |
  | HARDGROOVE 135 | las cuatro negras | clap en la "a" del 1 y del 3 | hhc en semicorcheas; toms y cencerro (hitom) en bucle |
  | FRENCHCORE 200 | las cuatro negras | snare en 2 y 4; clap en el "&" del 2 y del 4 | hho en cada "&"; hhc en cada "a" |
  | INDUSTRIAL HARDCORE 150 | 1, 2, 3, el "&" del 3 y 4 | snare en 2 y 4; clap metálico en la "a" del 2 y del 4 | sin hats |
  | HARDSTYLE 150 | las cuatro negras | clap en 2 y 4 | sin hats; lotom a contratiempo como cola del bombo (reverse bass) |
  | BAKALAO 125 | las cuatro negras | snare en 2 y 4 | hhc en semicorcheas; hho en el "&" del 4 |
  | BOOGIE 110 | 1, la "a" del 2, 3 y el "&" del 3 | snare y clap en 2 y 4 | hhc en semicorcheas |
  | MOTORIK 120 | todas las corcheas menos la 2 y la 4 (1, "&" del 1, "&" del 2, 3, "&" del 3 y "&" del 4) | snare en 2 y 4 | hhc en corcheas |
  | FUTURE GARAGE 130 | 1 y la "a" del 3 | snare en 2 y la "e" del 4 | hhc en el "&" del 1, la "e" del 2, el "&" del 3 y la "e" del 4 |
  | PSYBIENT 100 | 1 y el "&" del 2 | snare en el 3 (medio tiempo) | hhc en el "&" del 1 y del 3; hho en el "&" del 4 |
  | NEUROFUNK 174 | 1, el "&" del 3 y la "e" del 4 | snare en 2 y 4 | hhc en semicorcheas |
  | LIQUID DNB 174 | 1 y el "&" del 3 | snare en 2 y 4 (fantasmas en `-` y `,`) | ride (hho) en corcheas |
  | RIDDIM 140 | 1, la "a" del 1 y el "&" del 2 (repetitivo) | snare en el 3 | hhc en las negras |
  | FUTURE BASS 150 | 1, la "a" del 1 y el "&" del 3 | snare y clap en el 3 | hhc en cada "&" |
  | MIDTEMPO BASS 105 | 1, la "a" del 1 y el "&" del 3 | snare y clap en el 3 | hhc en semicorcheas; hho en el "&" del 4 |
  | PHONK 130 | 1 y la "a" del 2 | snare en el 3; clap en el 3 y la "a" del 4 | sin hats: el cencerro (hitom) los sustituye |
  | DRIFT PHONK 155 | 1, el "&" del 2, 3 y el "&" del 4 | clap en 2 y 4 | hhc en cada "&"; cencerro (hitom) |
  | BRAZILIAN PHONK 130 | 1, la "a" del 1, el "&" del 2 y el "&" del 3 (tamborzão) | clap en 2 y 4 | hhc en corcheas; cencerro (hitom) |
  | BROKEN BEAT 120 | 1, la "a" del 2 y la "a" del 3 | snare en 2, la "e" del 3 y el "&" del 4 | hhc en corcheas |
  | BOSSA NOVA CHILL 100 | 1, la "a" del 1, 3 y la "a" del 3 (surdo) | rim (clap) en la clave de bossa: 1, la "a" del 1, el "&" del 2, el "&" del 3 y 4 | shaker (hhc) en semicorcheas |
  | DEMBOW 120 | las cuatro negras | snare dembow: la "a" del 1, el "&" del 2, la "a" del 3 y el "&" del 4 | hhc en semicorcheas |
  | FUNK DE RAIZ 130 | 1, la "a" del 1, 3 y la "a" del 3 (Volt Mix, 808) | clap en 2 y 4 | hhc en corcheas |
  | SINGELI 200 | las cuatro negras | snare en cada "&" | toms en semicorcheas troceadas |
  | NORTEC 125 | las cuatro negras | snare en cada "&" (tarola norteña) | hhc en semicorcheas |
  | ACID JAZZ 105 | 1, el "&" del 2 y el "&" del 3 | snare en 2 y 4 | hhc en las "e" y las "a"; hho en el "&" del 4 |

  En la tabla, "&" es la corchea a contratiempo, y "e" y "a" son la 2.ª y la 4.ª semicorchea de la negra.
- **Receta de groove** (cabecera de cada fuente): swing 58 en ACID JAZZ y FUTURE GARAGE, 56 en BOOGIE y BROKEN BEAT, 54 en SKWEEE, MICROHOUSE, LIQUID DNB (hho) y BOSSA NOVA CHILL, 52 en DUB TECHNO, y 50 en el resto. Slide del snare entre −3 y 0 ms en NEUROFUNK y LIQUID DNB.
- **Fuente de la lista**: `pulseroots.genres.json` (293 subgéneros en 14 familias). Se descartan: los que ya hay (Detroit, acid house, gqom, kuduro, jungle, footwork…), los que no tienen batería (ambient, drone, noise, musique concrète, clásica, post-rock…) y los que solo cambian el sonido respecto a un estilo existente (soulful, tropical, slap, big room y progressive house; uplifting, vocal, orchestral y hard trance; brostep, melodic dubstep y chillstep; hi-NRG, Eurobeat, nu-disco, synth-pop, darkwave, Eurodance…).
- **Tabla en orden alfabético**: las filas nuevas ("Bass music", "Downtempo / chill", "IDM / experimental" y "Phonk") se insertan en su sitio alfabético y "Other" sigue al final, como dejó el commit `afd4e13`.
- **Antes excluidos, ahora con rejilla propia**: HARDSTYLE (bombo y clap sin hats, a 8 de TRANCE 138), DUB TECHNO (palmas de eco), SCHRANZ (clap en cada "&") y NEUROFUNK y LIQUID DNB (semicorcheas de hhc y ride en corcheas). LIQUID DNB pone las fantasmas en `-` y `,`: con Density alta suenan a la velocidad de la voz, así que la receta sugiere bajar la del snare.
- **Referencias consultadas** (tarea 1.3): Wikipedia ("Motorik": bombo en todas las corcheas menos la 2 y la 4), guías de phonk (en el phonk de Memphis el cencerro sustituye al hi-hat; drift phonk a 140–170 BPM, por eso DRIFT PHONK pasa de 125 a 155), Billboard Brasil (Volt Mix: célula 808 seca y repetitiva), Wikipedia ("Nortec": tarola y redobles polirrítmicos sobre 4/4; "Deconstructed club": cambios de ritmo constantes) y guías de skweee y singeli (80–110 y 180–300 BPM). Para BAKALAO y HARDGROOVE no se encontró una fuente fiable.
- **Cencerro en hitom** para los tres phonk: la melodía de cencerro es su firma; aquí solo se escribe el ritmo, la nota la decide el sampler.
- **BAKALAO** (ruta del bakalao, Valencia, finales de los 80 y 90) va en Hardcore / hard dance junto a MAKINA.
- **Distancia medida** con bocetos de la rejilla `X` (kick, snare, clap, hhc y hho por separado, p4/p5): los 31 quedan a 8 pasos o más de cualquier otro estilo. Se retocaron MOTORIK (2 de SYNTHWAVE 100), MIDTEMPO BASS y PHONK (3 de HALFTIME 174), GLITCH HOP (4 de DARK ELECTRO 125), NEUROFUNK (4 de BOOM BAP 90), FRENCHCORE (2 de ACID TECHNO 140 y 4 de DISCO 118), BAKALAO, BROKEN BEAT e INDUSTRIAL HARDCORE. Los pares más justos: ACID JAZZ – DARKCORE 155, BAKALAO – ACID TECHNO 140 y BOOGIE – NEW JACK SWING 104 (8).

## Risks / Trade-offs

- [Sin dinámica] Las fantasmas suenan a la velocidad de la voz. → Van en niveles bajos (`-`, `,`) para que solo entren con Density alta.
- [Parecido entre estilos] → Lo detecta la comprobación de distancia antes de escribir, y la escucha en REAPER después. Se retocan las fuentes, sin cambiar el plugin.
- [Interpretación musical] Se toma la gramática del género, no una grabación concreta. Las fuentes son texto plano y se regeneran en segundos.
- [Conocimiento del género] SKWEEE, DECONSTRUCTED CLUB, SINGELI, NORTEC, BAKALAO, HARDGROOVE, FUNK DE RAIZ, MOTORIK y los phonk se conocen menos. → Consultar referencias escritas antes de escribirlos y anotarlas en la cabecera.
- [Ritmos sin rejilla] IDM y DECONSTRUCTED CLUB son irregulares por definición. → Se fija una rejilla rara pero estable; la variedad la da Density y los patrones del pad.
- [Tempo extremo] SINGELI (200) y FRENCHCORE (200) solo difieren del resto por la rejilla; el BPM va en el nombre.

## Verificación en REAPER

1. `sh tools/install.sh`.
2. Para cada estilo: pad en (0,0), Density y Div por defecto, y el swing de la receta. Grabar la salida MIDI del plugin durante 2 compases.
3. Comprobar que las notas de p4 y p5 caen donde marcan los `X` de la fuente.
4. Subir Density por encima de 52, 103, 154 y 205, y comprobar que en cada escalón se añade el nivel siguiente sin quitar golpes.
5. Escuchar los estilos del cambio seguidos y comprobar que se distinguen entre sí y del estilo existente más parecido.
