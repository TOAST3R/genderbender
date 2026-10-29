## Context

- Cada patrón son 32 pasos, que con el Div por defecto equivalen a un compás de 4/4 en fusas. Una línea de 16 caracteres escribe semicorcheas.
- El plugin alterna p(2n) y p(2n+1) a cada compás, así que cada pareja (p4/p5, p2/p3…) forma una frase de 2 compases. p8 vale para los dos.
- Un paso suena si `256 − v < Density`. Con la escala de 5 niveles (`X=255 x=204 o=153 -=102 ,=51`), con Density por defecto (50) solo suena `X`, y cada nivel inferior entra al subir Density (>52, >103, >154, >205).
- La velocidad es fija por voz. El valor del paso solo decide si suena, no su volumen.
- El plugin no fija el tempo: el BPM va solo en el nombre. Por eso dos estilos con la misma rejilla suenan igual aunque su BPM sea distinto, y la diferencia tiene que estar en los golpes.
- El swing es global (50–75 %) con un amount por voz, y no se guarda en el estilo. Con swing 50 todo suena recto.

## Goals / Non-Goals

**Goals:**
- 3 estilos que se distingan entre sí y de los existentes con los valores por defecto (Density 50, pad en el centro).
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
- **Uso de las voces:** kick = bombo; snare = caja; clap = palmas o capa sobre la caja; hhc/hho = hats; hitom/lotom = toms electrónicos, protagonistas en los fills.
- **Ritmo esencial (`X`) de cada BASE**, que es lo que distingue los estilos con Density por defecto:

  | Estilo | Kick | Snare / clap | Hats / toms |
  |---|---|---|---|
  | SYNTHWAVE 100 | 1 y 3 | snare en 2 y 4 (caja gated) | hhc en corcheas; fill de toms descendente en p8 |
  | DISCO 118 | las cuatro negras | snare en 2 y 4 | hho en cada "&"; hhc en semicorcheas en `x` |
  | ITALO DISCO 120 | las cuatro negras | clap en 2 y 4; snare solo en `x` | hhc en corcheas; hitom y lotom (Simmons) en el "&" y la "a" del 4 del compás 2 |

  En la tabla, "&" es la corchea a contratiempo, y "e" y "a" son la 2.ª y la 4.ª semicorchea de la negra.
- **Receta de groove** (cabecera de cada fuente): swing 50 en los tres (son rectos). Slide 0. En DISCO, amount del hho al 0 % si se sube el swing global.
- **Familia nueva "Synth / disco"** en el README para los tres.

## Risks / Trade-offs

- [Sin dinámica] Las fantasmas suenan a la velocidad de la voz. → Van en niveles bajos (`-`, `,`) para que solo entren con Density alta.
- [Parecido entre estilos] → Lo detecta la comprobación de distancia antes de escribir, y la escucha en REAPER después. Se retocan las fuentes, sin cambiar el plugin.
- [Interpretación musical] Se toma la gramática del género, no una grabación concreta. Las fuentes son texto plano y se regeneran en segundos.
- [DISCO ≈ house] Comparte el bombo a negras con `Chicago.Jouse 125`. → Se distingue por el hho en cada contratiempo y por la caja en vez del clap; la comprobación de distancia lo confirma.

## Verificación en REAPER

1. `sh tools/install.sh`.
2. Para cada estilo: pad en (0,0), Density y Div por defecto, y el swing de la receta. Grabar la salida MIDI del plugin durante 2 compases.
3. Comprobar que las notas de p4 y p5 caen donde marcan los `X` de la fuente.
4. Subir Density por encima de 52, 103, 154 y 205, y comprobar que en cada escalón se añade el nivel siguiente sin quitar golpes.
5. Escuchar los estilos del cambio seguidos y comprobar que se distinguen entre sí y del estilo existente más parecido.
