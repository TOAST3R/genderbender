## 1. Sincronía

- [x] 1.1 Cola de pasos en `tick` (`{t, canvas, step, voces}`) y bucle `requestAnimationFrame` que solo corre mientras suena y consume la cola con `ac.currentTime`

## 2. Patrón

- [x] 2.1 Cursor (`div` absoluto) sobre el patrón de la vista ampliada con la columna del paso actual; se borra al parar y salta de patrón con el compás (A/B incluido)
- [x] 2.2 `.hit` en el nombre de la voz durante unos 80 ms cuando golpea

## 3. Visualizador

- [x] 3.1 `AnalyserNode` conectado a las salidas del bus maestro
- [x] 3.2 Modos Onda y Espectro (48 barras logarítmicas), alternados con un clic y guardados en `localStorage['gb-vis']`
- [x] 3.3 Canvas en la vista ampliada y barra fija al pie, visible solo mientras suena desde la lista
- [x] 3.4 `prefers-reduced-motion`: sin visualizador ni `.hit`; el cursor se mantiene

## 4. Verificación

- [x] 4.1 Regenerar `docs/fingerprints.html`; `python3 tools/check_styles.py` imprime `ok`; la página no carga recursos externos
- [x] 4.2 En un navegador (Playwright): el cursor recorre los 32 pasos en sincronía con la cola y respeta el swing; `.hit` en las voces; el analizador recibe señal y los dos modos dibujan; barra del pie al tocar desde la lista; movimiento reducido emulado; el bucle se para al parar
- [ ] 4.3 Mirarlo mientras suena y retocar (lo hace el usuario)
