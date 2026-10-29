## 1. BPM

- [x] 1.1 Slider 40–240 con salida y ↺ en la cabecera y en la vista ampliada, sincronizados; `bpmOverride` y BPM efectivo; `start()` lo vuelve al del estilo
- [x] 1.2 Planificador: BPM efectivo en A/B y recálculo de `P.barStart` al cambiar a mitad de compás; el delay lo sigue
- [x] 1.3 MIDI con el BPM efectivo y permalink `bpm`

## 2. Escenas: base

- [x] 2.1 Canvas de fondo fijo (también dentro del `<dialog>`), dimensionado con `devicePixelRatio` ≤ 2; cabecera, secciones y diálogo sobre tarjetas sólidas
- [x] 2.2 Estado por fotograma `{t, beat, bar, hits, bands, bpm, w, h, dark}` desde la cola de pasos y el analizador; dibujo a ≤ 30 fps en el bucle `rAF`; nada con la pestaña oculta
- [x] 2.3 Elección de escena (estilo que suena → filtro → Otros) con fundido de 400 ms; `still` sin reproducción, al cambiar de filtro o de tema, y con `prefers-reduced-motion`

## 3. Escenas: las nueve

- [x] 3.1 909 y 808
- [x] 3.2 Acústico y Lo-fi
- [x] 3.3 Hardcore y 80s
- [x] 3.4 Percusión, Chiptune y Otros

## 4. Verificación

- [x] 4.1 Regenerar `docs/fingerprints.html`; `python3 tools/check_styles.py` imprime `ok`; la página no carga recursos externos
- [x] 4.2 En un navegador (Playwright): las comprobaciones de BPM y de escenas de `design.md`, incluido el brillo medio en Hardcore a 200 BPM y los fps de fondo
- [ ] 4.3 Mirar las 9 escenas en claro y en oscuro y ajustarlas (lo hace el usuario)
