## Context

- Cada patrón son 32 pasos, que con el Div por defecto equivalen a un compás de 4/4 en fusas. Una línea de 16 caracteres escribe semicorcheas.
- El plugin alterna p(2n) y p(2n+1) a cada compás, así que cada pareja (p4/p5, p2/p3…) forma una frase de 2 compases. p8 vale para los dos.
- Un paso suena si `256 − v < Density`. Con la escala de 5 niveles (`X=255 x=204 o=153 -=102 ,=51`), con Density por defecto (50) solo suena `X`, y cada nivel inferior entra al subir Density (>52, >103, >154, >205).
- La velocidad es fija por voz. El valor del paso solo decide si suena, no su volumen.
- El plugin no fija el tempo: el BPM va solo en el nombre. Por eso dos estilos con la misma rejilla suenan igual aunque su BPM sea distinto, y la diferencia tiene que estar en los golpes.
- El swing es global (50–75 %) con un amount por voz, y no se guarda en el estilo. Con swing 50 todo suena recto.

## Goals / Non-Goals

**Goals:**
- 36 estilos que se distingan entre sí y de los existentes con los valores por defecto (Density 50, pad en el centro).
- Que Density construya cada estilo por capas: ritmo esencial, luego adornos y fantasmas, luego redobles.

**Non-Goals:**
- Cambiar el plugin (velocidad por paso, tresillos, swing guardado en el estilo, frases de más de 2 compases).
- Reproducir una grabación concreta nota a nota.
- FADO CORRIDO, HORNPIPE, ranchera, norteño, corrido, slip jig, danzas balcánicas y turcas en 7, 9 u 11, hora y doina (ver Decisions).

## Decisions

- **Escala de 5 niveles** (`X x o - ,`) y receta de groove (swing, amount por voz y slide) en un comentario de cabecera, como las cumbias y el drum & bass.
- **Reparto del pad** igual que las cumbias: p4/p5 BASE, p2/p3 ENERGÍA, p6/p7 VARIACIÓN, p0/p1 INTRO (hats y percusión, sin bombo ni caja completos) y p8 FILL (redoble de caja y toms).
- **Capas de Density:** el ritmo esencial en `X`; adornos, fantasmas y golpes extra en `x o - ,`, de más a menos importante.
- **Nombres en mayúsculas con el BPM** (`NOMBRE 120`), sin tildes ni eñes en el nombre de archivo, para no depender de cómo REAPER lee nombres no ASCII.
- **Distancia antes de escribir:** con un script de un solo uso (no se añade a `tools/`), comparar la rejilla `X` de cada BASE nueva con la de p4/p5 de todos los estilos existentes y de los otros estilos del cambio. Si dos coinciden en kick, snare y hats, se retoca la fuente nueva.
- **Uso de las voces:** kick = bombo, contrabajo, tambora, surdo, zabumba, alfaia, bombo legüero, dhol grave o bayan; snare = caja, escobillas, bodhrán, tamborim, caixa, repique o dhol agudo; clap = palmas, clave, chop de mandolina, slap del contrabajo o aro del bombo; hhc/hho = hats, ride, bongó, campana, güira, ganzá, tabla de lavar o triángulo; hitom/lotom = congas, timbales y toms.
- **Ritmo esencial (`X`) de cada BASE**, que es lo que distingue los estilos con Density por defecto:

  | Estilo | Kick | Snare / clap | Hats / toms |
  |---|---|---|---|
  | BLUES SHUFFLE 100 | las cuatro negras (tresillos) | snare en 2 y 4 | hho en shuffle (largo-corto) |
  | WESTERN SWING 170 | las cuatro negras (tresillos) | snare en 2 y 4 | ride (hhc) "spang-a-lang": 1, 2, la "a" del 2, 3, 4, la "a" del 4 |
  | BLUEGRASS 120 | 1 y 3 (el contrabajo) | chop de mandolina (snare y clap) en 2 y 4 | rasgueo de guitarra (hho) a contratiempo |
  | COUNTRY SHUFFLE 120 | 1 y 3 (tresillos) | snare en 2 y 4 | hhc en shuffle (largo-corto) |
  | TRAIN BEAT 110 | 1 y 3 | escobillas (snare) en las 16 semicorcheas | — |
  | ROCKABILLY 180 | 1, 3 y el "&" del 3 | snare en 2 y 4; slap del contrabajo (clap) a contratiempo | hhc en corcheas |
  | ZYDECO 120 | 1 y 3 | snare en 2, la "a" del 2, 4 y la "a" del 4 | tabla de lavar (hhc) en semicorcheas; hho en el "&" del 2 y del 4 |
  | TWO-STEP 140 | 1 y 3 | snare y clap en 2 y 4 | ride (hho) en corcheas |
  | REEL 110 | 1 y 3 | bodhrán (snare) en 1, la "a" del 1, 2, la "a" del 2… (8 golpes) | — |
  | JIG 115 | el 1 de cada 6/8 (tresillos) | bodhrán en las 12 corcheas; acento (clap) en cada negra con puntillo | — |
  | STRATHSPEY 120 | 1 y 3 | Scotch snap (snare): semicorchea en la negra y la siguiente | — |
  | IRISH POLKA 140 | el 1 de cada 2/4 | snare a contratiempo; palmas en 2 y 4 | — |
  | SON 95 | bajo anticipado en el "&" del 2 y en el 4 | clave 3-2 (clap) | bongó martillo (hhc) en corcheas |
  | RUMBA GUAGUANCO 100 | tumbadora grave (kick) en la "a" del 3 | clave de rumba 3-2 (clap) | congas (toms) con el resto del toque |
  | BOLERO 80 | 1 y 3 | clave 2-3 (clap) | bongó (hhc) en corcheas |
  | MERENGUE 130 | las cuatro negras (tambora) | tambora (snare) en 2, 4, el "&" del 4 y la "a" del 4; slap (clap) en la "a" del 2 y del 4 | güira (hhc) en semicorcheas |
  | MAMBO 190 | bajo anticipado en el "&" del 2 y en el 4 | clave 2-3 (clap) | campana (hhc) en las negras |
  | CHA-CHA-CHA 120 | 1 y 3 | el "cha-cha" (snare) en 4 y el "&" del 4 | campana (hhc) en las negras |
  | KOMPA 120 | 1, el "&" del 2, 3 y el "&" del 4 | snare en 2 y 4 | platillo (hho) a contratiempo |
  | SALSA 180 | bajo anticipado en el "&" del 2 y en el 4 | clave 3-2 (clap) | cáscara (hhc) |
  | BACHATA 130 | 1, 2 y 3 | golpe (snare) en el 4 | güira (hhc) en 1, 2, el "&" del 2, 3, 4 y el "&" del 4 |
  | MARACATU 90 | alfaias (kick) en 1, la "a" del 1, el "&" del 2, 3, el "&" del 3 y la "e" del 4 | caixa (snare) en las 16 semicorcheas | — |
  | FREVO 140 | 1, el "&" del 2, 3 y el "&" del 4 | caixa (snare) en las 16 semicorcheas | hho en el "&" del 1 y del 3 |
  | SAMBA 100 | surdo en 2 y 4 | tamborim (snare) en teleco-teco | ganzá (hhc) en semicorcheas |
  | BAIAO 100 | zabumba en 1, la "a" del 1, 3 y la "a" del 3 | bacalhau (snare) en 2 y 4 | triángulo: cerrado (hhc) en semicorcheas y abierto (hho) a contratiempo |
  | AXE 130 | surdo en 1, la "a" del 1, 3 y la "a" del 3 | caixa (snare) en 2, el "&" del 3 y 4 | hho en el "&" del 1 y del 3 |
  | CANDOMBE 110 | tambor piano (kick) en 2 y 4 | repique (snare) en la "a" del 1, el "&" del 2, la "a" del 3 y el "&" del 4; madera (clap) en clave 3-2 | — |
  | TANGO 64 | marcato en las cuatro negras | arrastre (snare) en la "a" del 1 y del 3; acento (clap) en 1 y 3 | — |
  | MILONGA 90 | 1, el "&" del 2, 3 y el "&" del 4 (3-3-2) | snare en la "a" del 1 y del 3 | — |
  | CHACARERA 70 | bombo legüero (parche) en los tresillos 1, 5, 7 y 11 (hemiola 6/8 + 3/4) | aro del bombo (clap) en los tresillos 3, 6, 9 y 12 | — |
  | HUAYNO 90 | 1, la "a" del 1, 2, 3, la "a" del 3 y 4 (largo-corto) | — | hhc en corcheas |
  | HUAPANGO 110 | el 1 de cada 6/8 (tresillos) | rasgueo en hemiola (clap); zapateado (snare) en el 2 y el 4 | hhc en las 12 corcheas |
  | SON JAROCHO 120 | el 1 de cada 6/8 (tresillos) | zapateado (snare) en shuffle; palmas en la 4.ª corchea de cada 6/8 | — |
  | FREYLEKHS 130 | bulgar 3-3-2: 1, el "&" del 2 y 4 | snare en 2, 3 y el "&" del 4 | hhc en corcheas |
  | BHANGRA 95 | dhol grave en la chaal (tresillos 1, 3, 4, 7, 9 y 10) | dhol agudo en los tresillos 2, 5, 6, 8, 11 y 12 | — |
  | KEHERWA 100 | bayan (kick) en 1, el "&" del 1 y 3 | dayan (snare) en 2, el "&" del 2, 4 y el "&" del 4 | — |

  En la tabla, "&" es la corchea a contratiempo, y "e" y "a" son la 2.ª y la 4.ª semicorchea de la negra.
- **Receta de groove** (cabecera de cada fuente): los ternarios (BLUES SHUFFLE, WESTERN SWING, COUNTRY SHUFFLE, JIG, CHACARERA, HUAPANGO, SON JAROCHO y BHANGRA) **piden swing global 67**; los binarios llevan el de su género (58 en BOLERO y SON, 56 en SAMBA, BAIAO y CANDOMBE, 54 en SALSA, MAMBO, CHA-CHA-CHA y BACHATA, y 50 en el resto). El preview de la página lo aplica solo.
- **Seis familias nuevas**, cada una en orden cronológico: "Country / Americana" (8), "Celtic" (4), "Latin / Caribbean" (9), "Brazil" (5), "South America" (5) y "World folk" (5: México, klezmer e India).
- **Tresillos con swing 67** (la técnica de `add-spanish-folk-styles`) para los shuffles y los 6/8. En los shuffles, una negra del plugin es una negra real; en JIG, CHACARERA, HUAPANGO y SON JAROCHO, una negra con puntillo.
- **Claves en el clap**: 3-2 (SON, SALSA, la madera del CANDOMBE), 2-3 (BOLERO, MAMBO) y la clave de rumba (RUMBA GUAGUANCO). La clave 3-2 del son coincide con la de BOSSA NOVA CHILL; lo que los separa es el resto de voces.
- **Fuera por gemelos o por no caber**: FADO CORRIDO (sin percusión, salía a 4 de AFRO HOUSE 122: es una polka), HORNPIPE (en la rejilla ≈ JIG o REEL), ranchera (vals 3/4 ≈ JOTA ARAGONESA), norteño y corrido (≈ NORTEC 125), slip jig (9/8), danzas balcánicas y turcas en 7, 9 u 11 (rachenitsa, kopanitsa, karşılama, zeibekiko), hora y doina (ritmo libre o compás irregular).
- **VARIACIÓN y FILL** derivados de la base de cada estilo, sin salirse de la rejilla de tresillos en los ternarios, y sin repetir ningún p6, p7 ni p8 de otro estilo.
- **Distancia medida** con bocetos (kick, snare, clap, hhc y hho por separado, p4/p5): los 36 quedan a 8 pasos o más de cualquier otro estilo. Se retocaron 16: los country se parecían entre sí (COUNTRY SHUFFLE, BLUES SHUFFLE y WESTERN SWING a 4), ROCKABILLY salía a 2 de SYNTHWAVE 100, ZYDECO a 2 de DARKWAVE 120, BLUEGRASS idéntico a IRISH POLKA y FREYLEKHS idéntico a DIGITAL DANCEHALL 95, entre otros. El par más justo: BACHATA – CHA-CHA-CHA (8).

## Risks / Trade-offs

- [Sin dinámica] Las fantasmas suenan a la velocidad de la voz. → Van en niveles bajos (`-`, `,`) para que solo entren con Density alta.
- [Parecido entre estilos] → Lo detecta la comprobación de distancia antes de escribir, y la escucha en REAPER después. Se retocan las fuentes, sin cambiar el plugin.
- [Interpretación musical] Se toma la gramática del género, no una grabación concreta. Las fuentes son texto plano y se regeneran en segundos.
- [Swing obligatorio] Los ocho ternarios suenan desfigurados con swing 50. → Cabecera en mayúsculas, nota del README y preview que lo aplica solo.
- [Conocimiento del género] Muchos son toques de percusión de mano (congas, surdos, dhol, tabla) reducidos a 7 voces. → Consultar referencias escritas de cada uno antes de escribirlo y anotarlas en la cabecera; los que no tengan fuente lo dirán.
- [Cambio grande] 36 estilos. → Tareas por familia; se puede aplicar y comprobar por bloques.

## Verificación en REAPER

1. `sh tools/install.sh`.
2. Para cada estilo: pad en (0,0), Density y Div por defecto, y el swing de la receta. Grabar la salida MIDI del plugin durante 2 compases.
3. Comprobar que las notas de p4 y p5 caen donde marcan los `X` de la fuente.
4. Subir Density por encima de 52, 103, 154 y 205, y comprobar que en cada escalón se añade el nivel siguiente sin quitar golpes.
5. Escuchar los estilos del cambio seguidos y comprobar que se distinguen entre sí y del estilo existente más parecido.
