## Context

- El tempo de cada estilo es `st.bpm` (del nombre, del README o 120). El planificador usa `P.bpm`, que en A/B cambia al de cada estilo; el delay lo sigue (`delayBpm`) y el MIDI escribe `st.bpm` en el evento de tempo.
- Los pasos se programan en `P.barStart + stepTime(step, P.bpm)`; cambiar `P.bpm` a mitad de compás movería la posición actual.
- La cola de pasos (`P.q`, `{t, mark, step, hits}`) y el `AnalyserNode` (`FXB.an`) ya existen, y un bucle `requestAnimationFrame` corre mientras suena.
- `FAM_KIT` asigna a cada familia uno de 9 grupos de kit. La paleta sale de las variables `--bg`, `--fg`, `--cell`, `--ink`, `--line`, en claro y en oscuro.
- La vista ampliada es un `<dialog>` modal: lo fijo de la página queda debajo de su `::backdrop`.

## Goals / Non-Goals

**Goals:**
- Cambiar el tempo con un slider sin perder el BPM de cada estilo, y que todo lo siga (planificador, A/B, delay, cursor, MIDI, escenas).
- Una escena animada con carácter propio por grupo, al tempo y con los golpes, legible y segura.

**Non-Goals:**
- WebGL, librerías o imágenes externas.
- Una escena distinta para cada una de las 35 familias.
- Guardar un BPM fijo entre estilos (bloqueo): el slider vuelve al BPM del estilo al pulsar Play.

## Decisions

### BPM

- **Estado**: `bpmOverride` (null o número). El BPM efectivo es `bpmOverride ?? st.bpm`. `start()` lo pone a null y coloca el slider en `st.bpm`. Mover el slider fija `bpmOverride`; ↺ lo vuelve a null.
- **A/B**: en `tick`, al cambiar de estilo, `P.bpm = bpmOverride ?? P.cur.st.bpm`. Con override, los dos estilos van al mismo tempo.
- **Sin saltos**: al cambiar el BPM a mitad de compás, se recalcula `P.barStart` para que la posición del paso actual en el tiempo no cambie: `P.barStart = tPasoActual - stepTime(P.step, nuevo)`. Los pasos ya programados (unos 100 ms) suenan al tempo anterior.
- **Slider**: `<input type="range">` 40–240, con la salida numérica y el botón ↺, en la cabecera y en la vista ampliada (mismo patrón que Density y Swing). La etiqueta `NNN BPM` de cada estilo sigue mostrando su BPM propio.
- **MIDI**: el evento de tempo usa el BPM efectivo; las notas, en ticks, no cambian.
- **Permalink**: `bpm` solo si hay override; al cargar, si el enlace trae estilo y `bpm`, se aplica.

### Escenas

- **Estructura**: `SCENES[id] = draw(g, s)`; la imagen fija es la misma función con un estado en reposo (`calm`), con el mismo `id` que los kits (`FAM_KIT`). `s` = `{t, beat, bar, hits, bands, bpm, w, h, dark}`: `beat` es la fase dentro de la negra (0–1), calculada con el tiempo de audio y el BPM efectivo; `hits` son los golpes del último paso que ha sonado, sacados de la cola; `bands` es la energía en graves, medios y agudos del analizador.
- **Lienzo**: un `canvas` fijo detrás de todo (`z-index:-1`). Con la vista ampliada abierta, la escena se ve alrededor del `<dialog>` a través de un `::backdrop` más claro (30 % de negro en lugar de 50 %); no hace falta mover el canvas. La cabecera, las secciones de familia y el contenido del diálogo pasan a tarjetas con fondo sólido (`var(--bg)` con algo de opacidad máxima), para que las huellas no se lean sobre el movimiento.
- **Qué escena**: la del estilo que suena (por compás, así A/B cambia con el estilo); si no suena nada, la del género del filtro; si no hay filtro, Otros. Al cambiar, fundido de 400 ms entre la imagen anterior y la nueva.
- **Recetas** (Canvas 2D; se ajustan de oído y de vista):

  | Escena | Imagen | Movimiento |
  |---|---|---|
  | 909 | panel oscuro en perspectiva con potes y una tira de 16 botones | el botón encendido sigue al paso; el panel "respira" hacia delante en cada bombo |
  | 808 | túnel de anillos | los anillos avanzan al tempo; el bombo lanza una onda gruesa con caída larga; los graves hacen ondular el túnel |
  | Acústico | batería vista desde arriba (bombo, caja, toms y platos como círculos) | el parche de cada voz ondula cuando golpea |
  | Lo-fi | vinilo con etiqueta y brazo, grano y viñeta cálida | gira a 33⅓ rpm escalado por BPM / 90; motas de polvo con los hats |
  | Hardcore | franjas de aviso y un suelo áspero | las franjas pasan al BPM; el bombo da una sacudida de cámara corta y amortiguada |
  | 80s | rejilla de neón en perspectiva con sol a franjas en el horizonte | la rejilla avanza al tempo; la caja da un brillo en el horizonte; estrellas con los hats |
  | Percusión | tejido de colores en perspectiva | cada golpe deja caer una "piedra" con ondas circulares, de un color por voz |
  | Chiptune | CRT con líneas de barrido, pantalla algo curvada | ecualizador de bloques con el espectro; un sprite que salta con el bombo |
  | Otros | grano suave | — |

- **Colores**: cada escena usa las variables del tema y un acento propio, en claro y en oscuro (`dark` en `s`).
- **Seguridad**: ningún cambio de brillo a pantalla completa ligado al ritmo; los cambios de luz son locales y pequeños (por debajo de lo que WCAG 2.3.1 considera destello). El Hardcore a 200 BPM son unos 3,3 bombos por segundo: por eso la sacudida mueve la imagen en lugar de encenderla.
- **Movimiento reducido**: `still(g)` una vez, sin animación.
- **Coste**: el fondo se dibuja como mucho a 30 fps, dentro del bucle `rAF` actual; sin reproducción se dibuja `still` una vez y al cambiar de filtro o de tema; con la pestaña oculta no se dibuja nada. El canvas se dimensiona al tamaño de la ventana por `devicePixelRatio`, con un máximo de 2.

## Risks / Trade-offs

- [Legibilidad] Un fondo con movimiento distrae. → Tarjetas sólidas bajo el contenido y escenas con poco contraste fuera de su acento.
- [CPU / batería] Nueve escenas a pantalla completa. → 30 fps, un solo canvas y nada fuera de la reproducción; se mide en el navegador.
- [A/B] Cambios de escena cada dos compases. → Fundido de 400 ms; si los dos estilos son del mismo grupo no cambia nada.
- [Tempo] Cambiar el BPM con pasos ya programados. → Solo afecta a los ~100 ms ya programados; la posición se mantiene con `P.barStart`.
- [Tamaño] La página crece unos 15–25 KB. → Aceptable para un solo archivo de ~950 KB.

## Verificación

No toca el plugin. En un navegador (Playwright):
- BPM: el slider arranca en el BPM del estilo y vuelve a él al pulsar Play en otro; ↺ vuelve al del estilo; con override, A/B toca los dos al mismo tempo y sin override cada uno al suyo; cambiar el BPM a mitad de compás no salta (los tiempos de la cola siguen creciendo de forma monótona y el paso actual no cambia); el MIDI lleva el tempo del slider y las mismas notas; permalink `bpm`.
- Escenas: existen las 9 y dibujan en claro y en oscuro; la escena sigue al estilo que suena y cambia en A/B entre familias de grupos distintos; sin reproducción sigue al filtro; con `prefers-reduced-motion` emulado se dibuja una vez y no hay más fotogramas; con la pestaña oculta no se dibuja; el bucle no pasa de 30 fps de fondo; ningún fotograma cambia el brillo medio de la pantalla de forma brusca en el ritmo (medido en Hardcore a 200 BPM).
- A mano: mirar las 9 escenas y ajustarlas.
