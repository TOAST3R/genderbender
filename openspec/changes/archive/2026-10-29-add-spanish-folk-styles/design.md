## Context

- Cada patrón son 32 pasos, que con el Div por defecto equivalen a un compás de 4/4 en fusas. Una línea de 16 caracteres escribe semicorcheas.
- El plugin alterna p(2n) y p(2n+1) a cada compás, así que cada pareja (p4/p5, p2/p3…) forma una frase de 2 compases. p8 vale para los dos.
- Un paso suena si `256 − v < Density`. Con la escala de 5 niveles (`X=255 x=204 o=153 -=102 ,=51`), con Density por defecto (50) solo suena `X`, y cada nivel inferior entra al subir Density (>52, >103, >154, >205).
- La velocidad es fija por voz. El valor del paso solo decide si suena, no su volumen.
- El plugin no fija el tempo: el BPM va solo en el nombre. Por eso dos estilos con la misma rejilla suenan igual aunque su BPM sea distinto, y la diferencia tiene que estar en los golpes.
- El swing es global (50–75 %) con un amount por voz, y no se guarda en el estilo. Con swing 50 todo suena recto.

## Goals / Non-Goals

**Goals:**
- 16 estilos que se distingan entre sí y de los existentes con los valores por defecto (Density 50, pad en el centro).
- Que Density construya cada estilo por capas: ritmo esencial, luego adornos y fantasmas, luego redobles.

**Non-Goals:**
- Cambiar el plugin (velocidad por paso, tresillos, swing guardado en el estilo, frases de más de 2 compases).
- Reproducir una grabación concreta nota a nota.
- **Sin percusión o de ritmo libre**: cantar de cego, cantares de pacheca / de sala, asturianada / tonada, danza prima, y los cantes libres flamencos (malagueña, granaína, rondeña, taranta / taranto, cartagenera).
- **Compases de 5** (no caben ni con tresillos): zortziko, rueda / baile a la rueda, charrada.
- **Gemelos en la rejilla** de uno que sí entra: muiñeira vella, carballesa y chula, ribeirana y alborada (≈ MUINEIRA); jota galega, navarra, catalana, castellana, extremeña y murciana / parranda, rondeña de Extremadura (≈ JOTA ARAGONESA); seguidilla castellana y canaria (≈ SEVILLANA); fandango vasco y verdiales (≈ FANDANGO DE HUELVA); alegrías (mismos acentos que la soleá); ball de bot, mateixa, copeo y parado (≈ jota y fandango); paloteo (≈ BALL DE BASTONS); sirinoque (≈ TAJARASTE); isa, folías y malagueña canaria (3/4 con poca percusión propia).
- **Sin referencias suficientes** sobre su percusión (se pueden añadir en otro cambio si aparecen): giraldilla, saltón, picayos, trepelete, maneo, panda, olivera, mutxikoak, ezpata-dantza, entradilla y son brincao.

## Decisions

- **Escala de 5 niveles** (`X x o - ,`) y receta de groove (swing, amount por voz y slide) en un comentario de cabecera, como las cumbias y el drum & bass.
- **Reparto del pad** igual que las cumbias: p4/p5 BASE, p2/p3 ENERGÍA, p6/p7 VARIACIÓN, p0/p1 INTRO (hats y percusión, sin bombo ni caja completos) y p8 FILL (redoble de caja y toms).
- **Capas de Density:** el ritmo esencial en `X`; adornos, fantasmas y golpes extra en `x o - ,`, de más a menos importante.
- **Nombres en mayúsculas con el BPM** (`NOMBRE 120`), sin tildes ni eñes en el nombre de archivo, para no depender de cómo REAPER lee nombres no ASCII.
- **Distancia antes de escribir:** con un script de un solo uso (no se añade a `tools/`), comparar la rejilla `X` de cada BASE nueva con la de p4/p5 de todos los estilos existentes y de los otros estilos del cambio. Si dos coinciden en kick, snare y hats, se retoca la fuente nueva.
- **Uso de las voces:** kick = bombo, tambor grave o cajón grave; snare = tamboril, tarola, tambor de procesión o cajón agudo; clap = palmas, castañuelas o golpe de bastones; hhc = pandereta, pandeireta, sonajas, chácaras o palmas sordas; hho = pandereta abierta o plato; hitom/lotom = redobles y fills de tambor.
- **Ritmo esencial (`X`) de cada BASE**, que es lo que distingue los estilos con Density por defecto:

  | Estilo | Kick | Snare / clap | Hats / toms |
  |---|---|---|---|
  | MUINEIRA 120 | bombo en el 1 de cada 6/8 (tresillos 0 y 6) | tamboril en las corcheas 3, 4 y 6 de cada 6/8 | pandeireta en todas las corcheas; abierta en la 4.ª de cada 6/8 |
  | PASACORREDOIRA 110 | bombo en el 1 de cada 2/4 | tamboril "ta-rá-ta" (la "a" del 1, el 2 y el "&" del 2) | pandeireta en corcheas |
  | MARCHA PROCESIONAL 70 | bombo en el 1 de cada 2/4 | redoble de tambor de procesión al principio de la frase y en el 4 | plato (hho) en el 3 |
  | ARIN-ARIN 130 | bombo en el 1 de cada 2/4 | pandero a contratiempo; palmas en el 2 | sonajas del pandero (hhc) en semicorcheas |
  | BIRIBILKETA 110 | bombo en el 1 de cada 2/4 | tamboril de txistulari: 1, "&" del 1, "a" del 1, 2, 3, "&" del 3, "a" del 3, 4 | palmas en el "&" del 2 y del 4 |
  | JOTA ARAGONESA 60 | bombo en el 1 de cada 3/4 | castañuelas (clap) en el 2 y el 3 de cada 3/4 | pandereta en las tres negras de cada 3/4 |
  | SARDANA 100 | bombo en el 1 de cada 6/8 | tamborí en la 3.ª y 6.ª corchea | hhc en cada negra con puntillo |
  | BALL DE BASTONS 110 | bombo en el 1 de cada 2/4 | golpes de bastones (clap) en el 1, el 2 y el "&" del 2 | — |
  | TANGOS 100 | 1 y la "a" del 2 (cajón grave) | cajón agudo (snare) en 2 y 4; palmas en 2, 3 y 4 | — |
  | TIENTOS 75 | 1, la "a" del 2 y el "&" del 3 | cajón agudo en el 4; palmas en 2, 3, la "a" del 3 y 4 | palmas sordas (hhc) a contratiempo |
  | BULERIA 80 | cajón grave en los tiempos 3, 8 y 12 del compás | palmas en los acentos 3, 6, 8, 10 y 12; cajón agudo en el 6 y el 10 | palmas sordas (hhc) en los 12 tiempos |
  | SOLEA 50 | cajón grave en el 1 y en los acentos | palmas en los acentos 3, 6, 8, 10 y 12 | — |
  | SEGUIRIYA 45 | cajón grave en el 1 y el 8 | palmas en 1, 3, 5, 8 y 11 (2+2+3+3+2) | — |
  | SEVILLANA 65 | bombo en el 1 de los compases 1 y 3 | palmas en las tres negras; caja en el 1 de los compases 2 y 4 | — |
  | FANDANGO DE HUELVA 60 | bombo en el 1 de los compases 1 y 3 | palmas en hemiola: 1, 3 y 5 de cada par de compases, y el 1 del siguiente | pandereta en las negras |
  | TAJARASTE 110 | tambor grave en cada negra con puntillo | tambor agudo en la 3.ª corchea de cada pulso | chácaras (hhc) en la 2.ª y 3.ª corchea de cada pulso |

  En la tabla, "&" es la corchea a contratiempo, y "e" y "a" son la 2.ª y la 4.ª semicorchea de la negra.
- **Receta de groove** (cabecera de cada fuente): los ternarios (MUINEIRA, JOTA ARAGONESA, SARDANA, BULERIA, SOLEA, SEGUIRIYA, SEVILLANA, FANDANGO DE HUELVA y TAJARASTE) **piden swing global 67** con amount 100 en todas las voces; sin él suenan desfigurados. Los binarios: swing 54 en TIENTOS, 52 en TANGOS y 50 en el resto.
- **Compases ternarios con tresillos de swing 67**: dentro de cada negra del plugin, los pasos 0, 2 y 5 (de 8) caen con swing 67 en 0, 0,335 y 0,6675 de la negra (el tresillo exacto es 0, 1/3, 2/3; el error es de unos 2 ms). Un tresillo j (0–11) del compás va al paso `(j // 3) × 8 + (0, 2, 5)[j % 3]`. Así: 6/8 = dos compases por patrón (una negra del plugin = una negra con puntillo); 3/4 = cuatro compases por patrón (una negra del plugin = un compás de 3/4, con sus tres negras en tresillo); compás flamenco de 12 = un compás por patrón (los 12 tiempos en 4 tresillos).
- **El BPM del nombre es el del plugin**, no el del baile: MUINEIRA 120 = 120 negras con puntillo por minuto; JOTA ARAGONESA 60 = 60 compases de 3/4 por minuto (180 negras); BULERIA 80 = 240 tiempos de compás por minuto. La cabecera lo dice, y el preview de la página toca al tempo bueno porque usa el BPM del nombre y el swing de la receta.
- **Familias nuevas** "Flamenco" (TANGOS, TIENTOS, BULERIA, SOLEA, SEGUIRIYA, SEVILLANA, FANDANGO DE HUELVA) y "Folk ibérico" (MUINEIRA, PASACORREDOIRA, MARCHA PROCESIONAL, ARIN-ARIN, BIRIBILKETA, JOTA ARAGONESA, SARDANA, BALL DE BASTONS, TAJARASTE), en el orden de norte a sur de la lista pedida. Nombres sin tildes ni eñes en el archivo (MUINEIRA, BULERIA, SOLEA).
- **Selección**: de unos 70 nombres de la lista se quedan los 16 con una rejilla de percusión propia que cabe en el plugin. Ver Non-Goals para el resto y el motivo.
- **VARIACIÓN y FILL** se derivan de la base de cada estilo y se comprueba que ningún p6, p7 ni p8 repite el de otro (`dedupe-generated-patterns`). En los ternarios se derivan sobre la rejilla de tresillos para no salirse de ella.
- **Distancia medida** con bocetos (kick, snare, clap, hhc y hho por separado, p4/p5): los 16 quedan a 8 pasos o más de cualquier otro estilo. Los ternarios quedan a 14 o más de todo (caen en pasos que ningún otro estilo usa). Se retocaron cuatro binarios: ARIN-ARIN salía idéntico a NORTEC 125 (los dos son polkas), PASACORREDOIRA a 4 de SYNTHWAVE 100, TANGOS a 3 de JUMP-UP 174 y TIENTOS a 7.

## Risks / Trade-offs

- [Sin dinámica] Las fantasmas suenan a la velocidad de la voz. → Van en niveles bajos (`-`, `,`) para que solo entren con Density alta.
- [Parecido entre estilos] → Lo detecta la comprobación de distancia antes de escribir, y la escucha en REAPER después. Se retocan las fuentes, sin cambiar el plugin.
- [Interpretación musical] Se toma la gramática del género, no una grabación concreta. Las fuentes son texto plano y se regeneran en segundos.
- [Swing obligatorio] El swing es global en el plugin y no se guarda en el estilo: si se carga un estilo ternario con swing 50, los tresillos suenan desfigurados (0, 0,25, 0,625). → La cabecera de cada fuente lo dice en mayúsculas; el preview lo pone solo; se menciona en el README.
- [Swing para todo] Con swing 67 se mueven todas las voces. En los ternarios no hay notas fuera de la rejilla de tresillos, así que no afecta.
- [Conocimiento del género] La percusión tradicional varía de un pueblo a otro. → Consultar referencias escritas de cada estilo antes de escribirlo y anotarlas en la cabecera; los que no tengan fuente lo dirán.

## Verificación en REAPER

1. `sh tools/install.sh`.
2. Para cada estilo: pad en (0,0), Density y Div por defecto, y el swing de la receta. Grabar la salida MIDI del plugin durante 2 compases.
3. Comprobar que las notas de p4 y p5 caen donde marcan los `X` de la fuente.
4. Subir Density por encima de 52, 103, 154 y 205, y comprobar que en cada escalón se añade el nivel siguiente sin quitar golpes.
5. Escuchar los estilos del cambio seguidos y comprobar que se distinguen entre sí y del estilo existente más parecido.
