## Context

- Cada patrón son 32 pasos, que con el Div por defecto equivalen a un compás de 4/4 en fusas. Una línea de 16 caracteres escribe semicorcheas.
- El plugin alterna p(2n) y p(2n+1) a cada compás, así que cada pareja (p4/p5, p2/p3…) forma una frase de 2 compases. p8 vale para los dos.
- Un paso suena si `256 − v < Density`. Con la escala de 5 niveles (`X=255 x=204 o=153 -=102 ,=51`), con Density por defecto (50) solo suena `X`, y cada nivel inferior entra al subir Density (>52, >103, >154, >205).
- La velocidad es fija por voz. El valor del paso solo decide si suena, no su volumen.
- El plugin no fija el tempo: el BPM va solo en el nombre. Por eso dos estilos con la misma rejilla suenan igual aunque su BPM sea distinto, y la diferencia tiene que estar en los golpes.
- El swing es global (50–75 %) con un amount por voz, y no se guarda en el estilo. Con swing 50 todo suena recto.

## Goals / Non-Goals

**Goals:**
- 9 estilos que se distingan entre sí y de los existentes con los valores por defecto (Density 50, pad en el centro).
- Que Density construya cada estilo por capas: ritmo esencial, luego adornos y fantasmas, luego redobles.

**Non-Goals:**
- Cambiar el plugin (velocidad por paso, tresillos, swing guardado en el estilo, frases de más de 2 compases).
- Reproducir una grabación concreta nota a nota.
- Reparar los cuatro estilos rotos conservando su nombre (habría que reescribir su `.txt`).
- Electro-disco, space electro y French electro: en este plugin sonarían como otro estilo.

## Decisions

- **Escala de 5 niveles** (`X x o - ,`) y receta de groove (swing, amount por voz y slide) en un comentario de cabecera, como las cumbias y el drum & bass.
- **Reparto del pad** igual que las cumbias: p4/p5 BASE, p2/p3 ENERGÍA, p6/p7 VARIACIÓN, p0/p1 INTRO (hats y percusión, sin bombo ni caja completos) y p8 FILL (redoble de caja y toms).
- **Capas de Density:** el ritmo esencial en `X`; adornos, fantasmas y golpes extra en `x o - ,`, de más a menos importante.
- **Nombres en mayúsculas con el BPM** (`NOMBRE 120`), sin tildes ni eñes en el nombre de archivo, para no depender de cómo REAPER lee nombres no ASCII.
- **Distancia antes de escribir:** con un script de un solo uso (no se añade a `tools/`), comparar la rejilla `X` de cada BASE nueva con la de p4/p5 de todos los estilos existentes y de los otros estilos del cambio. Si dos coinciden en kick, snare y hats, se retoca la fuente nueva.
- **Uso de las voces:** kick = bombo 808 (largo en el electro-bass); snare = caja; clap = palmas 808; hhc/hho = hats; hitom = cencerro 808 (electro-funk) o tom; lotom = tom.
- **Ritmo esencial (`X`) de cada BASE**, que es lo que distingue los estilos con Density por defecto:

  | Estilo | Kick | Snare / clap | Hats / toms |
  |---|---|---|---|
  | CYBOTRON ELECTRO 125 | 1, el "&" del 2 y el "&" del 3 | snare y clap en 2 y 4 | hhc en las "e" y las "a"; hho en cada "&" |
  | ELECTRO FUNK 127 | 1, la "a" del 2 y el "&" del 3 | clap en 2 y 4 | hhc en corcheas; hho en la "a" del 1 y del 3; cencerro (hitom) |
  | DARKWAVE 120 | 1, el "&" del 2 y 3 | snare en 2 y 4 | hhc en semicorcheas |
  | ELECTRO BASS 130 | 1, la "a" del 2, el "&" del 3 y el "&" del 4 (808 largo) | clap en 2 y 4 | hhc en semicorcheas, con redobles de fusas que entran con Density |
  | DETROIT ELECTRO 130 | 1, la "a" del 1, la "a" del 3 y el "&" del 4 | snare en 2 y 4 | hhc en semicorcheas |
  | ELECTROCLASH 125 | 1, la "a" del 1, 3 y el "&" del 3 | snare en 2 y 4; clap en el 4 | hhc en corcheas; hho en el "&" del 2 y del 4 |
  | ELECTRO HOUSE 128 | las cuatro negras | clap en 2 y 4; snare en el "&" del 4 | hho en cada "a" |
  | OUTRUN 118 | las cuatro negras | snare y clap en 2 y 4 (caja gated) | hhc en cada "a"; hho en cada "&" |
  | INDUSTRIAL ELECTRO 130 | 1, la "a" del 1, 3 y la "a" del 3 | snare en 2 y 4; clap en la "a" del 2 | hhc en cada "&" |

  En la tabla, "&" es la corchea a contratiempo, y "e" y "a" son la 2.ª y la 4.ª semicorchea de la negra.
- **Receta de groove** (cabecera de cada fuente): swing 54 en ELECTRO FUNK y ELECTRO BASS (hhc), 52 en CYBOTRON ELECTRO y DETROIT ELECTRO, y 50 en el resto (el electro es casi siempre recto). Slide 0.
- **Borrar en vez de reparar**: AGENTS.md prohíbe reescribir un `.txt` existente, y los cuatro rotos no tienen fuente. Se borran `ELECTRO CYBOTRON`, `ELECTRO UR 138`, `BASS 101` y `AFRO BEAT` (completamente vacío; se queda `AFRO BEAT & JU JU`), y los tres de electro se sustituyen por estilos nuevos con fuente: CYBOTRON ELECTRO 125, DETROIT ELECTRO 130 (el sonido de Underground Resistance, Model 500 y Drexciya) y ELECTRO BASS 130.
- **Fila "Electro"** (antes "Electro / Miami bass") en orden cronológico: CYBOTRON ELECTRO (1981–83), ELECTRO FUNK (Planet Rock, 1982), DARKWAVE (80s), ELECTRO BASS (Miami, mediados de los 80), DETROIT ELECTRO (Model 500, 1985; Drexciya, 90s), DARK ELECTRO 125, GHETTOTECH 150 (90s), ELECTROCLASH (~2000), ELECTRO HOUSE (2000s), SYNTHWAVE 100 y OUTRUN (2010s) e INDUSTRIAL ELECTRO (hoy).
- **Se mueven** a Electro, sin tocar sus `.txt`: SYNTHWAVE 100 (desde "Synth / disco"), DARK ELECTRO 125 (desde "EBM / industrial") y GHETTOTECH 150 (desde "House"). Un estilo solo puede estar en una familia. Modifica los requisitos de README de `synth-disco-styles` y `techno-house-hardcore-rave-styles`.
- **Guarda nueva en `check_styles.py`**: falla si un estilo tiene p4 o p5 vacíos, que es lo que suena en el centro del pad y en el preview. Habría detectado los cuatro rotos.
- **VARIACIÓN y FILL** se derivan de la base de cada estilo y se comprueba que ningún p6, p7 ni p8 repite el de otro estilo (`dedupe-generated-patterns`).
- **Distancia medida** con bocetos de la rejilla `X` (kick, snare, clap, hhc y hho por separado, p4/p5), sin contar los cuatro que se borran: los nueve quedan a 8 pasos o más de cualquier otro estilo. Se retocaron todos menos ELECTRO HOUSE e INDUSTRIAL ELECTRO; el primer boceto de DETROIT ELECTRO quedaba a 4 de NEW JACK SWING 104, ELECTRO BASS a 4 de BRAZILIAN PHONK 130, OUTRUN a 4 de AGGROTECH 140 y ELECTROCLASH a 4 de SKWEEE 100. Los pares más justos: CYBOTRON ELECTRO – CUMBIA DIGITAL 100, DARKWAVE – BAKALAO 125 y ELECTRO BASS – BOOGIE 110 (8).

## Risks / Trade-offs

- [Sin dinámica] Las fantasmas suenan a la velocidad de la voz. → Van en niveles bajos (`-`, `,`) para que solo entren con Density alta.
- [Parecido entre estilos] → Lo detecta la comprobación de distancia antes de escribir, y la escucha en REAPER después. Se retocan las fuentes, sin cambiar el plugin.
- [Interpretación musical] Se toma la gramática del género, no una grabación concreta. Las fuentes son texto plano y se regeneran en segundos.
- [Presets] Un preset o proyecto que usara uno de los cuatro estilos borrados deja de encontrarlo. → Ya no sonaban (BASE vacía); se dice en el README.
- [Conocimiento del género] Se consultan referencias de Cybotron, Planet Rock, Model 500/Drexciya, Miami bass, electroclash, darkwave y outrun antes de escribirlos, y se anotan en la cabecera.

## Verificación en REAPER

1. `sh tools/install.sh`.
2. Para cada estilo: pad en (0,0), Density y Div por defecto, y el swing de la receta. Grabar la salida MIDI del plugin durante 2 compases.
3. Comprobar que las notas de p4 y p5 caen donde marcan los `X` de la fuente.
4. Subir Density por encima de 52, 103, 154 y 205, y comprobar que en cada escalón se añade el nivel siguiente sin quitar golpes.
5. Escuchar los estilos del cambio seguidos y comprobar que se distinguen entre sí y del estilo existente más parecido.
