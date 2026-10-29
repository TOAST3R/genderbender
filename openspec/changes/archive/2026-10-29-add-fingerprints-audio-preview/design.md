## Context

- `tools/view_styles.py` genera `docs/fingerprints.html`, un archivo autocontenido: los datos de todos los estilos van en JSON (`DATA.groups`, cada patrón como 7 voces × 32 pasos en hex) y un script pinta las tiras. `check_styles.py` falla si la página no coincide con lo que genera el script.
- La cabecera fija ya tiene el selector de género, el recuento y el slider de Density.
- En el plugin, cada patrón son 32 pasos (fusas con el Div por defecto), p(2n) y p(2n+1) se alternan a cada compás, un paso suena si `256 − v < Density`, y la velocidad es fija por voz.
- `families()` ya lee el `(bpm)` de cada entrada de la tabla del README.

## Goals / Non-Goals

**Goals:**
- Oír el ritmo de cualquier estilo a su tempo, con un clic, sin salir de la página.
- Que Density y el swing suenen como en el plugin.

**Non-Goals:**
- Reproducir el sonido del sampler o dar velocidad por paso.
- Leer el slide de la receta de groove.
- Campo para cambiar el BPM, exportar MIDI o grabar.

## Decisions

- **Sonido sintetizado con Web Audio**, una función por voz:
  - kick: seno de 150 a 45 Hz en 0,35 s;
  - snare: ruido con paso alto a 1 kHz más un tono de 180 Hz, 0,15 s;
  - clap: tres ráfagas de ruido con paso banda a 1,2 kHz;
  - hhc: ruido con paso alto a 7 kHz, 0,05 s;
  - hho: igual, 0,3 s, y un hhc lo corta;
  - hitom: seno de 220 a 160 Hz; lotom: seno de 140 a 100 Hz.

  Alternativa descartada: muestras en base64, que añadirían cientos de KB y una licencia.
- **Planificador con look-ahead**: un temporizador cada 25 ms programa en el `AudioContext` los pasos de los próximos 100 ms. El paso dura `60 / BPM / 8` s (una fusa). Density se lee en cada paso, así que mover el slider se oye al momento.
- **Swing global** de 50 a 75 % (50 por defecto) con la deformación de `groove-swing`: dentro de cada corchea, el tramo [0, 0,25) negras pasa a [0, p) y el tramo [0,25, 0,5) a [p, 0,5), con `p = S/100 × 0,5`. Se aplica a todas las voces.
- **Swing por estilo, automático:** `view_styles.py` lee de la cabecera de cada `styles_src/*.style` el swing (`swing NN` o `swing global NN`) y el amount por voz (`amount: hhc 100, kick 0, resto 0`; `resto` vale para las voces no nombradas, y sin `amount` todas van al 100 %). Al pulsar Play, el slider de swing pasa al valor del estilo, y cada voz usa `S_voz = 50 + (S − 50) × amount / 100`, como el plugin. El slider se puede seguir moviendo a mano mientras suena. Los estilos sin fuente (los antiguos y los dos garage) van a 50.
- **Qué suena:** el botón de la tira toca p4/p5 alternando a cada compás; los ▶ de la vista ampliada tocan un solo patrón en bucle. Un patrón vacío no suena (FILL vacío).
- **Uno a la vez:** un único estado de reproducción. Play en otro estilo o patrón para el actual y cambia su botón a ▶. Esc, cerrar la vista ampliada o cambiar de género no la paran, solo ■ Stop, Play en otro o Esc fuera de la vista ampliada.
- **Indicador:** mientras suena, el patrón que se está tocando lleva un borde del color de acento.
- **BPM calculado en Python** y guardado en `DATA` por estilo: número final del nombre (2 o 3 cifras entre 60 y 220, con o sin espacio o guion bajo delante: `GRIME140`, `DURUMBREAK_160`) → `(bpm)` de su entrada del README → 120. El BPM se muestra junto al botón.
- **BPM de las 35 entradas sin tempo**, por género (a revisar por el usuario):

  | BPM | Estilos |
  |---|---|
  | 70 | VAPORTRAP |
  | 90 | RB, 101 ZOUK KIZOMBA, ZOUK KIZOMBA 2 |
  | 95 | 101 DANCEHALL, 101 RAGATON, CUMBION, NEW ORLEANS |
  | 100 | BELLY DANCE, MOTOWN BREAKS, NEW ORLEANS BOUNCE |
  | 110 | AFRO BEAT, AFRO BEAT & JU JU |
  | 120 | 101 SPARSE, ZZZ BLACK (sin género claro) |
  | 122 | GQOM |
  | 125 | ELECTRO CYBOTRON |
  | 130 | 101 FUNK FAVELA, techAXX, TekkBooooring, TekkChungo, TekkThump, uk_fungui |
  | 132 | garage_2step, garage_uk_4x4, Two-stepppo, uk_garbage |
  | 140 | 101 STEPPA, DubSteppo, JERSEY BASICS |
  | 155 | SOCA |
  | 160 | 101 FOOTWORK, 101 JUKE, 102 JUKE |
  | 174 | drumbass |

## Risks / Trade-offs

- [Autoplay] Los navegadores solo dejan sonar tras un gesto del usuario. → El `AudioContext` se crea o reanuda al pulsar Play.
- [Sonido distinto del de REAPER] → Se dice en la propia página ("preview sintetizado") y en el README.
- [Carga de CPU] Más de 150 tiras no suenan a la vez: solo hay una reproducción activa.
- [BPM supuestos] Los 35 tempos son estimaciones por género. → Van en el README, donde se corrigen sin tocar código.

## Verificación

No toca el plugin, así que no hace falta REAPER. En un navegador (Playwright): pulsar Play en un estilo crea el contexto de audio y programa notas; pulsar Play en otro deja solo uno sonando; Stop y Esc paran; el BPM mostrado coincide con el nombre o con el README. Escuchar unos cuantos estilos y comprobar que el ritmo coincide con la tira.
