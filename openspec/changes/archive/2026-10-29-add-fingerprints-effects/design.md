## Context

- Cada golpe del preview se conecta directamente a `ac.destination`, o a una salida con efecto del kit (`fx('lofi' | 'chip' | 'drive')`) que también acaba en `ac.destination`. Hay 9 conexiones a `ac.destination` en la plantilla.
- El planificador (`tick`) conoce el BPM del compás que suena (`P.bpm`), también en A/B, donde cambia con el estilo.
- Los controles de la cabecera (Density, Swing, Kit) tienen copia sincronizada en la vista ampliada y se guardan en el permalink cuando no están en su valor por defecto.
- La spec exige que la página sea un solo archivo sin recursos externos.

## Goals / Non-Goals

**Goals:**
- Distortion, delay y reverb globales, ajustables mientras suena.
- Que con los tres a 0 el sonido sea idéntico al de hoy.

**Non-Goals:**
- Envíos por voz o efectos por kit en Auto: más adelante, junto con el kit por voz.
- Respuestas de impulso cargadas de fuera (rompen la regla de recursos externos).
- Afectar al MIDI exportado o al plugin.

## Decisions

- **Cadena**, creada una vez por contexto de audio:

  ```
  voces / fx del kit ─▶ master ─▶ DIST ─┬─────────────────────────────▶ destination
                                        ├─▶ envío DELAY ─▶ delay ⟲ fb ─▶ destination
                                        └─▶ envío REVERB ─▶ convolver ─▶ destination
  ```

  Las 9 conexiones a `ac.destination` pasan a `master`. El delay y la reverb van en paralelo (envíos); la señal seca no se toca.
- **Distortion**: `WaveShaper` con curva `tanh(k·x)/tanh(k)`, con `k` de 1 a 20 según el knob, y ganancia de compensación para que el nivel no suba. Con el knob a 0 la curva es lineal (sin efecto). `oversample = '2x'`.
- **Delay**: `DelayNode` con tiempo de corchea con puntillo (`0,75 · 60 / BPM`), actualizado con `setTargetAtTime` cuando cambia el BPM (A/B); realimentación fija de 0,35 con paso bajo a 3 kHz dentro del bucle. El knob controla la ganancia del envío.
- **Reverb**: `ConvolverNode` con una respuesta de impulso estéreo de 2 s generada una vez (ruido con caída exponencial). El knob controla la ganancia del envío.
- **Knobs**: cada uno es un `<input type="range">` de 0 a 100, que conserva el teclado, la rueda y la accesibilidad, presentado como un disco con `conic-gradient` que se gira arrastrando en vertical. Si el disco da guerra, se queda como slider: el valor y el comportamiento no cambian.
- **Sincronización y persistencia**: el mismo patrón que Kit: cabecera y vista ampliada sincronizadas, `localStorage['gb-fx']` y los parámetros `dist`, `dly` y `rev` del permalink, que solo se escriben si no son 0. El permalink manda al cargar.
- **Cambios mientras suena**: los knobs mueven parámetros de audio (`setTargetAtTime`, unos 20 ms) en lugar de reconstruir nodos, para que no haya clics.

## Risks / Trade-offs

- [Volumen] Distortion alta junto con el kit Hardcore (que ya distorsiona) puede saturar. → La curva `tanh` acota la salida y la ganancia de compensación baja el nivel. Sin limitador al final: cambiaría el sonido con los knobs a 0.
- [Realimentación] Un delay con realimentación alta puede crecer sin fin. → Realimentación fija por debajo de 0,5, no expuesta en un knob.
- [Stop] Al parar, la cola del delay y la reverb sigue sonando unos segundos. → Es lo esperable en un efecto; no se corta.

## Verificación

No toca el plugin. En un navegador (Playwright): con los tres knobs a 0, el render offline de un compás es idéntico al de hoy; cada knob cambia la señal (más energía tras el golpe en delay y reverb, más armónicos en distortion); el tiempo del delay sigue al BPM en A/B; mover un knob mientras suena no para la reproducción; cabecera y vista ampliada sincronizadas; `localStorage` y permalink; el MIDI no cambia. A mano: escuchar los efectos.
