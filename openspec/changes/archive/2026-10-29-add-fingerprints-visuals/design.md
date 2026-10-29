## Context

- El planificador (`tick`) programa cada paso por adelantado (unos 100 ms) con `ac.currentTime`; hoy solo marca el patrón del compás con un `setTimeout`.
- Toda la salida pasa por el bus maestro (`bus()`): la señal seca, el envío de delay y el de reverb van a `ac.destination`.
- La vista ampliada dibuja cada patrón en un `canvas` (`draw([c, hex, s])`, 32 pasos × 7 voces, celdas de `s` px) con los nombres de las voces a la izquierda (`.voices`).
- La vista ampliada es un `<dialog>` modal: un elemento fijo de la página no se ve por encima de él.

## Goals / Non-Goals

**Goals:**
- Ver qué paso suena y qué voces golpean, sincronizado con el audio.
- Ver la onda o el espectro de lo que sale por los altavoces.
- Coste bajo: animar solo mientras suena.

**Non-Goals:**
- Visuales "de VJ" (partículas, 3D, shaders): más adelante si gusta.
- Cursor en las tiras pequeñas de la lista: ya se marca el patrón del compás y no hay sitio.
- Grabar o exportar el visualizador.

## Decisions

- **Cola de pasos**: `tick` mete en una cola `{t, step, bar, voces}` cada paso que programa. Un bucle `requestAnimationFrame`, activo solo mientras `play` existe, saca de la cola los pasos con `t <= ac.currentTime` (más `ac.outputLatency` si existe) y pinta el último. Así el cursor sigue al audio aunque el planificador vaya adelantado, y respeta el swing porque `t` ya lo incluye.
- **Cursor**: un `div` con posición absoluta encima del patrón que suena en la vista ampliada, del ancho de un paso, en `var(--ink)` semitransparente. No hace falta otro canvas. No se redibuja la huella.
- **Golpe por voz**: la clase `.hit` en el nombre de la voz durante unos 80 ms (transición CSS de opacidad).
- **Visualizador**: un `AnalyserNode` (`fftSize` 2048) al que se conectan las tres salidas del bus, además de a `ac.destination`. **Onda** usa `getFloatTimeDomainData` (una línea); **Espectro** usa `getByteFrequencyData` en unas 48 barras en escala logarítmica de 30 Hz a 16 kHz. Un clic en el visualizador cambia de modo; el modo se guarda en `localStorage['gb-vis']`.
- **Dónde**: un `canvas` en la vista ampliada, debajo de las herramientas, y otro en una barra fija al pie de la página que solo se muestra mientras suena algo desde la lista. El bucle dibuja en el que esté visible.
- **Movimiento reducido**: con `prefers-reduced-motion: reduce` no se dibuja el visualizador y no hay `.hit`; el cursor de paso se mantiene.

## Risks / Trade-offs

- [Sincronía] `setTimeout` y `rAF` no son exactos. → La cola con tiempos de audio corrige la deriva; un desfase de un fotograma (unos 16 ms) es aceptable.
- [CPU] Dibujar a 60 fps. → Solo mientras suena, un único `rAF` y canvas pequeños; se mide en el navegador.
- [A/B] Con A/B, el patrón que suena cambia de canvas cada compás. → El elemento de la cola guarda qué canvas es; el cursor salta con él.

## Verificación

No toca el plugin. En un navegador (Playwright): mientras suena, el cursor avanza por los 32 pasos y se reinicia en cada compás, coincide con el paso de la cola cuyo tiempo ya pasó y, con swing, los pasos impares se retrasan; los nombres de las voces reciben `.hit` cuando golpean; el analizador recibe señal (energía mayor que 0) y los dos modos dibujan; la barra del pie aparece al pulsar Play en la lista y desaparece al parar; con `prefers-reduced-motion` emulado no se dibuja el visualizador; el bucle `rAF` se detiene al parar. A mano: mirarlo mientras suena.
