## Context

- Cada patrón son 32 pasos, que con el Div por defecto equivalen a un compás de 4/4 en fusas. Una línea de 16 caracteres escribe semicorcheas.
- El plugin alterna p(2n) y p(2n+1) a cada compás, así que cada pareja (p4/p5, p2/p3…) forma una frase de 2 compases. p8 vale para los dos.
- Un paso suena si `256 − v < Density`. Con la escala de 5 niveles (`X=255 x=204 o=153 -=102 ,=51`), con Density por defecto (50) solo suena `X`, y cada nivel inferior entra al subir Density (>52, >103, >154, >205).
- La velocidad es fija por voz. El valor del paso solo decide si suena, no su volumen.
- El plugin no fija el tempo: el BPM va solo en el nombre. Por eso dos estilos con la misma rejilla suenan igual aunque su BPM sea distinto, y la diferencia tiene que estar en los golpes.
- El swing es global (50–75 %) con un amount por voz, y no se guarda en el estilo. Con swing 50 todo suena recto.

## Goals / Non-Goals

**Goals:**
- 6 estilos que se distingan entre sí y de los existentes con los valores por defecto (Density 50, pad en el centro).
- Que Density construya cada estilo por capas: ritmo esencial, luego adornos y fantasmas, luego redobles.

**Non-Goals:**
- Cambiar el plugin (velocidad por paso, tresillos, swing guardado en el estilo, frases de más de 2 compases).
- Reproducir una grabación concreta nota a nota.

## Decisions

- **Escala de 5 niveles** (`X x o - ,`) y receta de groove (swing, amount por voz y slide) en un comentario de cabecera, como las cumbias y el drum & bass.
- **Reparto del pad** igual que las cumbias: p4/p5 BASE, p2/p3 ENERGÍA, p6/p7 VARIACIÓN, p0/p1 INTRO (hats y percusión, sin bombo ni caja completos) y p8 FILL (redoble de caja y toms).
- **Capas de Density:** el ritmo esencial en `X`; adornos, fantasmas y golpes extra en `x o - ,`, de más a menos importante.
- **Nombres en mayúsculas con el BPM** (`NOMBRE 120`), sin tildes ni eñes en el nombre de archivo, para no depender de cómo REAPER lee nombres no ASCII.
- **Distancia antes de escribir:** con un script de un solo uso (no se añade a `tools/`), comparar la rejilla `X` de cada BASE nueva con la de p4/p5 de todos los estilos existentes y de los otros estilos del cambio. Si dos coinciden en kick, snare y hats, se retoca la fuente nueva.
- **Uso de las voces:** kick = bombo o 808; snare = caja; clap = capa sobre la caja o rim; hhc = hat cerrado; hho = hat abierto; hitom/lotom = percusión o trozos del break, casi vacíos fuera de TRIP HOP.
- **Ritmo esencial (`X`) de cada BASE**, que es lo que distingue los estilos con Density por defecto:

  | Estilo | Kick | Snare / clap | Hats / toms |
  |---|---|---|---|
  | BOOM BAP 90 | 1, "a" del 2 y "&" del 3 | snare en 2 y 4 | hhc en corcheas |
  | LOFI HIPHOP 82 | 1 y "a" del 2 | rim (clap) en 2 y 4; snare vacío en `X` | hhc en corcheas sin el "&" del 4 |
  | TRIP HOP 88 | 1, "e" del 3 y "&" del 3 (doble kick arrastrado) | snare en 2 y 4 | hhc solo en las negras; hho en el "&" del 2 y del 4; lotom en la "a" del 4 |
  | NEW JACK SWING 104 | 1, "a" del 1, "&" del 2 y "&" del 3 | snare en 2 y 4 con clap doblado | hhc en semicorcheas |
  | TRAP 140 | 1 y "a" del 2, más el "&" del 4 en el compás 2 | snare + clap solo en el 3 (medio tiempo) | hhc en corcheas; redoble de fusas en la negra 4 del compás 2 |
  | UK DRILL 142 | 1 y "&" del 2 | snare en el 3, y en el compás 2 también en la "a" del 4 | hhc en 3-3-2 de semicorcheas |

  En la tabla, "&" es la corchea a contratiempo, y "e" y "a" son la 2.ª y la 4.ª semicorchea de la negra.
- **Receta de groove** (cabecera de cada fuente): swing 58 en BOOM BAP (hats y kick), 60 en LOFI, 54 en TRIP HOP, 64 en NEW JACK SWING (hats al 100 %, kick al 50 %), y 50 en TRAP y UK DRILL. Slide del snare entre +2 y +6 ms ("caja tarde") en BOOM BAP y LOFI.
- **Redobles en fusas (TRAP 140):** el redoble de hats usa líneas de 32 caracteres. Las corcheas van en `X`, las semicorcheas en `x` y las fusas en `o`, así que subir Density llena el redoble.
- **Hats de drill sin tresillos:** el drill real usa tresillos de semicorchea, que el plugin no tiene. Se aproximan con grupos 3-3-2 de semicorcheas, y la receta lo dice.
- **TRAP y UK DRILL van en la fila "R&B / trap"**, junto a `VAPORTRAP`; los otros cuatro abren la fila "Hip-hop".

## Risks / Trade-offs

- [Sin dinámica] Las fantasmas suenan a la velocidad de la voz. → Van en niveles bajos (`-`, `,`) para que solo entren con Density alta.
- [Parecido entre estilos] → Lo detecta la comprobación de distancia antes de escribir, y la escucha en REAPER después. Se retocan las fuentes, sin cambiar el plugin.
- [Interpretación musical] Se toma la gramática del género, no una grabación concreta. Las fuentes son texto plano y se regeneran en segundos.
- [Swing fuera del estilo] BOOM BAP, LOFI y NEW JACK SWING dependen del swing. Con ALL RND o swing 50 suenan rectos. → La receta de la cabecera lo indica; guardar el swing en el estilo queda fuera de alcance.
- [Distancia medida] Comparando la rejilla `X` de kick, snare, clap, hhc y hho en p4/p5 (diferencia simétrica de pasos), el par más cercano es TRAP 140 – `101 STEPPA` (7). TRIP HOP y NEW JACK SWING se retocaron porque con la primera versión quedaban a 2 de BOOM BAP/HARDSTEP y de DANCEFLOOR DNB.
- [BOOM BAP ≈ LOFI] Comparten tempo y gramática. → En `X` se distinguen por el rim en vez de la caja y por el kick más escaso.

## Verificación en REAPER

1. `sh tools/install.sh`.
2. Para cada estilo: pad en (0,0), Density y Div por defecto, y el swing de la receta. Grabar la salida MIDI del plugin durante 2 compases.
3. Comprobar que las notas de p4 y p5 caen donde marcan los `X` de la fuente.
4. Subir Density por encima de 52, 103, 154 y 205, y comprobar que en cada escalón se añade el nivel siguiente sin quitar golpes.
5. Escuchar los estilos del cambio seguidos y comprobar que se distinguen entre sí y del estilo existente más parecido.
