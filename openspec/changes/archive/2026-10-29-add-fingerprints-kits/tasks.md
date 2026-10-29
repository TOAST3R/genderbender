## 1. Kits

- [x] 1.1 Ladrillos de síntesis: `metal()`, `click()` y salidas por kit con `crush`, `drive` y `gate`, además de los `tone()` y `noise()` actuales
- [x] 1.2 Los 9 kits (`KITS[nombre]` = 7 funciones de voz) con las recetas de `design.md`, ajustando de oído y con ganancia de salida por kit
- [x] 1.3 Tabla familia → kit para Auto

## 2. Selector y reproducción

- [x] 2.1 Selector de kit en la cabecera y en la vista ampliada, sincronizados, mostrando "Auto (<kit>)"
- [x] 2.2 El planificador elige el kit en cada golpe según el selector o la familia del estilo del compás (A/B incluido)
- [x] 2.3 Guardar el kit en `localStorage` y en el permalink (`kit`), con prioridad del permalink al cargar

## 3. Verificación

- [x] 3.1 Regenerar `docs/fingerprints.html`; `python3 tools/check_styles.py` imprime `ok`; la página no carga recursos externos
- [x] 3.2 En un navegador (Playwright): los 9 kits programan nodos en las 7 voces; Auto elige 909 en Techno y Percusión en Latin / Caribbean; A/B cambia de kit con el estilo; cambiar el kit mientras suena no para la reproducción; `localStorage` y permalink; el MIDI no cambia con el kit
- [x] 3.3 Medir que el kit 808 con hats en semicorcheas a 200 BPM no se atasca
- [ ] 3.4 Escuchar los 9 kits y retocar las recetas de oído (lo hace el usuario)
