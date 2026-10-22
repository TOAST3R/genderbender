## Context

- Cada patrón son 32 pasos, que con el Div por defecto equivalen a un compás de 4/4 en fusas. Una línea de 16 caracteres escribe semicorcheas.
- El plugin alterna p(2n) y p(2n+1) a cada compás, así que cada pareja (p4/p5, p2/p3…) forma una frase de 2 compases. p8 vale para los dos.
- Un paso suena si `256 − v < Density`. Con la escala de `five-level-density-scale` (`X=255 x=204 o=153 -=102 ,=51`), con Density por defecto (50) solo suena `X`, y cada nivel inferior entra al subir Density (>52, >103, >154, >205).
- La velocidad es fija por voz (un slider por voz). El valor del paso no cambia el volumen, así que una nota fantasma suena tan fuerte como un golpe principal: solo se puede controlar si suena o no.
- El plugin no fija el tempo: el BPM va solo en el nombre.

## Goals / Non-Goals

**Goals:**
- Siete estilos que se distingan entre sí con los valores por defecto (Density 50, pad en el centro).
- Que Density construya cada estilo por capas: ritmo esencial, luego adornos y fantasmas, luego redobles.

**Non-Goals:**
- Cambiar el plugin (velocidad por paso, tresillos, frases de más de 2 compases).
- Reproducir un break concreto nota a nota. Se toma su gramática, no la grabación.
- Los sub-géneros que en este plugin sonarían casi igual que otro (Neurofunk ≈ Techstep, Darkstep ≈ Jungle, Synthwave DnB ≈ two-step), y los que piden lo que el plugin no tiene: fantasmas con dinámica (Liquid, Jazzstep) o tresillos (Footwork Jungle).

## Decisions

- **Escala de 5 niveles.** Las fuentes se escriben con `X x o - ,` después de aplicar `five-level-density-scale`. Alternativa descartada: `[n]` exactos con la escala actual. Funciona sin dependencia, pero las fuentes se leen peor, y el cambio de escala ya está propuesto.
- **Uso de las voces:**
  - kick = bombo
  - snare = caja
  - clap = capa sobre la caja o rim (aro)
  - hhc = hat cerrado
  - hho = hat abierto o ride
  - hitom/lotom = trozos del break en jungle y hardstep, percusión en ragga, y casi vacíos en techstep
- **Reparto del pad** igual que las cumbias: p4/p5 BASE, p2/p3 ENERGÍA, p6/p7 VARIACIÓN, p0/p1 INTRO (hats y percusión, sin bombo ni caja completos) y p8 FILL (redoble de caja y toms).
- **Ritmo esencial (`X`) de cada BASE**, que es lo que distingue los estilos con Density por defecto:

  | Estilo | Kick | Snare | Hats / extra |
  |---|---|---|---|
  | JUNGLE 165 | 1, "&" del 1 y "&" del 3 | 2 y 4, más la "a" del 2 y la "e" del 3 (estilo amen) | hhc en corcheas, toms troceados en x/o |
  | RAGGA JUNGLE 165 | como JUNGLE | como JUNGLE | clap en tresillo 3-3-2 de dancehall (pasos 0, 3 y 6 de 8) |
  | HARDSTEP 172 | 1, "&" del 2 y "&" del 3 | 2 y 4, golpe seco y sin fantasmas en X | hhc en corcheas, hho en el "&" del 4 |
  | JUMP-UP 174 | two-step: 1 y "&" del 3, más la "a" del 1 en el compás 2 | 2 y 4, con clap doblado | hhc a contratiempo |
  | DANCEFLOOR DNB 174 | two-step: 1 y "&" del 3 | 2 y 4, con clap doblado | hho en cada contratiempo y hhc en semicorcheas |
  | TECHSTEP 172 | two-step: 1 y "&" del 3 | 2 y 4 | hhc escaso (solo negras) y rim en la "a" del 4 |
  | HALFTIME 174 | 1, más la "&" del 2 en el compás 2 | solo en el 3 | hhc en semicorcheas |

  Los adornos (fantasmas de caja, kicks extra, aperturas de hat) van en `x`, `o`, `-` y `,`, por orden de importancia.
- **Receta de groove en la cabecera** de cada fuente, como en las cumbias: swing ~54 en JUNGLE, RAGGA y HALFTIME (solo hats), y 50–52 en el resto, que son más rectos. Slide del snare entre −3 y 0 ms en los estilos que empujan.
- **Nombres en mayúsculas con el BPM**, como las cumbias. `JUMP-UP` lleva guion, que no da problemas en el nombre de archivo (`Two-stepppo` ya lo tiene).

## Risks / Trade-offs

- [Sin dinámica] Las fantasmas suenan a la velocidad de la voz. → Van en niveles bajos (`-`, `,`) para que solo aparezcan con Density alta, y la receta sugiere bajar la velocidad del snare en los estilos con más fantasmas.
- [Parecido entre estilos] JUMP-UP, DANCEFLOOR y TECHSTEP comparten el kick two-step. → Se distinguen por los hats y la caja de la tabla. Si en REAPER no se distinguen lo suficiente, se retocan las fuentes, sin cambiar el plugin.
- [Interpretación musical] Las fuentes son texto plano y se regeneran en segundos.
- [Dependencia] Si `five-level-density-scale` no está aplicado, `build` falla con el símbolo `,`, y eso es lo que se quiere: un error, no un estilo con umbrales equivocados.

## Verificación en REAPER

1. `sh tools/install.sh`.
2. En una pista, para cada estilo: pad en (0,0), Density por defecto y Div por defecto. Grabar la salida MIDI del plugin durante 2 compases.
3. Comprobar que las notas de p4 y p5 caen donde marcan los `X` de la fuente.
4. Subir Density por encima de 52, 103, 154 y 205, y comprobar que en cada escalón se añade el nivel siguiente.
5. Escuchar los siete seguidos y comprobar que se distinguen.
