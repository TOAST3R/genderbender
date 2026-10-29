## 1. Audio

- [x] 1.1 Bus maestro: las conexiones a `ac.destination` de voces y salidas de kit pasan a `master`
- [x] 1.2 Cadena de efectos: distortion (`WaveShaper` con compensación), envío de delay (corchea con puntillo, realimentación 0,35 con paso bajo) y envío de reverb (respuesta de impulso generada)
- [x] 1.3 El tiempo del delay sigue a `P.bpm` en el planificador (A/B incluido)

## 2. Knobs

- [x] 2.1 Knob = `<input type="range">` 0–100 presentado como disco (`conic-gradient`, arrastre vertical); Distortion, Delay y Reverb en la cabecera y en la vista ampliada, sincronizados
- [x] 2.2 Los knobs mueven parámetros de audio con `setTargetAtTime`, sin reconstruir nodos
- [x] 2.3 `localStorage['gb-fx']` y parámetros `dist`, `dly` y `rev` del permalink (solo si no son 0), con prioridad del permalink al cargar

## 3. Verificación

- [x] 3.1 Regenerar `docs/fingerprints.html`; `python3 tools/check_styles.py` imprime `ok`; la página no carga recursos externos
- [x] 3.2 En un navegador (Playwright): con los knobs a 0 el render offline es idéntico al de hoy; cada knob cambia la señal; el delay sigue al BPM en A/B; mover un knob mientras suena no para nada; sincronización, `localStorage` y permalink; el MIDI no cambia
- [ ] 3.3 Escuchar los efectos con varios kits y retocar de oído (lo hace el usuario)
