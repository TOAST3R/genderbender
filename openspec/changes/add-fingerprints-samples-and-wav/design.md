## Context

- Las voces de los kits (`KITS[id].v[vi](t)`), los ladrillos (`tone`, `noise`, `metal`…), las salidas con efecto (`fx()`), el bus maestro con distortion, delay y reverb (`bus()`, `FXB`) y el buffer de ruido (`noiseBuf`) usan todos un `AudioContext` global, `ac`. Las pruebas han hecho renders offline cambiando esos globales, que funciona pero es frágil.
- El planificador decide qué suena con `getBar(n)` (patrón, secuencia, A/B, pad), Density, mute/solo y `stepTime` (swing por voz); el MIDI exportado ya recorre esa misma lógica sin tiempo real.
- El arrastre del MIDI usa `DownloadURL` en `dragstart`, que necesita los datos de forma síncrona.
- La spec pide una página de un solo archivo sin recursos externos.

## Goals / Non-Goals

**Goals:**
- Sustituir cualquier voz por un sample propio, recordado entre visitas.
- Exportar a WAV exactamente lo que se oye, con loops que empalman.
- Arrastrar el WAV de una parte al DAW como ya se hace con el MIDI.

**Non-Goals:**
- Stems, captura en directo (con el pad), afinación y recorte de samples: más adelante.
- Subir samples o compartirlos por el permalink.
- Otros formatos (24 bits, 48 kHz, MP3, FLAC).

## Decisions

### Audio independiente del contexto

- **Cambio respecto a la propuesta inicial** (`engine(ctx)`): en lugar de reescribir todas las voces de los kits, `inContext(ctx, fn)` cambia los globales del audio (`ac`, `noiseBuf`, `FXB`, `FX`, `choke`) solo mientras `fn` programa las notas del render offline, y los restaura en un `finally`. Programar las notas es síncrono, así que el planificador en directo no puede ejecutarse en medio. El directo no cambia ni una línea, y el test nulo deja de hacer falta.
- En un contexto offline, `applyFx` fija los parámetros de los efectos sin rampa, para que el primer golpe ya lleve su delay y su reverb.
- El choke de hats pasa a ser uno solo (`choke.hh`), para que un hhc corte al hho aunque uno venga de un kit y el otro de un sample.

### Samples

- **Carga**: `<input type="file" accept="audio/*">` y soltar un archivo sobre el nombre de la voz; `decodeAudioData` → `AudioBuffer`. Un archivo que no se puede decodificar muestra un aviso y no cambia nada.
- **Uso**: si la voz tiene sample, el golpe crea un `AudioBufferSourceNode` → ganancia (ganancia del sample × velocity) → bus del motor; si no, la voz del kit. Velocity = valor del paso / 255. El hhc para la fuente del hho como hoy (`choke`).
- **Interfaz** (vista ampliada, junto a mute/solo): por voz, nombre del archivo o del kit, ⇪ cargar, ✕ volver al kit, y ganancia (−24 a +6 dB). Un aviso "samples propios" en la cabecera cuando hay alguno.
- **IndexedDB**: base `gb-samples`, almacén `voices`, clave = índice de voz, valor `{name, bytes: ArrayBuffer, gainDb}`. Se guarda el archivo original (no el decodificado): ocupa menos y se decodifica al cargar la página. Un sample mayor de 10 MB se rechaza con aviso (`shortcut`: límite fijo, subirlo si alguien lo necesita).

### Exportar WAV

- **Render**: `OfflineAudioContext(2, frames, 44100)` con un motor propio; se programan los pasos con la misma lógica que `tick` (getBar, Density, mute/solo, swing por voz, BPM efectivo, kit o samples, efectos), pero sin tiempo real.
- **Colas envueltas** (por defecto): se renderiza un compás más y la parte que sobra (cola de reverb y delay) se suma al principio, para que el loop empalme. Sin la opción, se corta al final del último compás.
- **WAV**: PCM 16 bits, 44,1 kHz, estéreo, con *dither* triangular; cabecera RIFF de 44 bytes.
- **Qué se exporta**:
  - Por parte (p0–p8): el patrón repetido N compases (1, 2, 4 u 8).
  - Secuencia: las partes no vacías en el orden de ▶ secuencia, una vez.
  - Todas las partes: un ZIP sin compresión (*store*, con CRC32) con `ESTILO pN PARTE.wav` por cada parte no vacía.
- **Nombres**: `ESTILO pN PARTE.wav`, con ` NNN BPM` si el BPM no es el del estilo.
- **Arrastre**: `DownloadURL` necesita los datos en `dragstart`, y el render es asíncrono. Por eso, al abrir la vista ampliada y 300 ms después de cualquier cambio que afecte al sonido, se renderiza en segundo plano el WAV de cada parte y se guarda en caché con una clave de los ajustes. `dragstart` usa una URL `data:` (base64) preparada en la caché: es la forma que ya funciona con el MIDI, sin depender de que Chrome acepte `blob:` en `DownloadURL`. La descarga con ⬇ usa el `Blob`. Mientras no está listo, el asa muestra "…" y no se arrastra.

## Risks / Trade-offs

- [Refactor] Tocar toda la síntesis puede cambiar el sonido sin querer. → Test nulo antes de quitar el camino antiguo.
- [Memoria] Nueve WAV en caché de un estilo lento a 8 compases pueden ser ~20 MB. → La caché solo guarda el estilo abierto y se libera (`URL.revokeObjectURL`) al cerrarlo o al cambiar ajustes.
- [CPU] Re-renderizar 9 partes en cada cambio. → Espera de 300 ms y render de una parte cada vez; un render de 2 compases tarda decenas de ms.
- [IndexedDB] Puede no estar disponible (modo privado). → Los samples funcionan en la sesión y se avisa de que no se guardarán.
- [Permalink] Un enlace con samples propios no suena igual en otro navegador. → Aviso "samples propios".

## Verificación

No toca el plugin. En un navegador (Playwright):
- Cargar un WAV generado en la prueba en la voz kick: suena en el preview (energía en el analizador), sobrevive a una recarga (IndexedDB), ✕ vuelve al kit; un archivo no decodificable da aviso.
- El WAV exportado tiene cabecera RIFF válida, 16 bits, 44 100 Hz, 2 canales y la duración exacta de N compases al BPM efectivo; con colas envueltas, el final y el principio empalman (sin salto de nivel); los golpes caen en las muestras esperadas según `stepTime`.
- El ZIP se abre (`unzip -t` sobre el archivo descargado) y contiene una entrada por parte no vacía.
- El asa ⠿ WAV pasa de "…" a lista tras el render y `dragstart` pone `DownloadURL`.
- A mano: arrastrar un WAV a REAPER y cargar samples reales.
