# Proposal

## Why

Los plugins JSFX solo se pueden verificar en REAPER, y hasta ahora eso era grabar la salida y mirarla a mano. Al probar GenderBender Melo por el MCP de REAPER se montó un banco de pruebas automático (logger MIDI, conductor de la GUI y analizadores). Ese banco encontró tres errores reales que el validador en Python no puede ver: Markov sin cadencia, estilos perdidos al reabrir el proyecto y reinicio de deslizadores. Pero vive en un scratchpad de sesión que desaparece y apunta a rutas fijas. Hay que llevarlo al repo antes de perderlo, para que la próxima prueba en REAPER sea repetible.

## What Changes

- Nueva carpeta `tools/reaper_test/` con el banco de pruebas:
  - **Logger MIDI** (`gbtest_log.jsfx`): se pone detrás del plugin, deja pasar el MIDI y anota en `gmem` cada evento con su `beat_position` exacto, estado, datos, bus e id de logger (para varias pistas receptoras).
  - **Generador de la copia de prueba de la GUI** (`make_test_jsfx.py`): crea a partir de `genderbender_melo.jsfx` una copia con ratón y menús simulados por `gmem` y con el estado dibujado (aviso de estilo, indicador de progresión, escala de la ventana, contadores de los dados) exportado a `gmem`. Así responde el código real de la GUI. Falla con un error claro si el plugin cambia y un punto de inyección deja de existir.
  - **Biblioteca Lua** sin rutas fijas: secuencias de reproducción (poner sliders, reproducir un rango, acciones a mitad, volcado), conductor de la GUI (clic, clic derecho, arrastre, menú, esperar fotogramas, comprobar) y utilidades de proyecto (reabrir sin diálogo).
  - **Lanzador** instalable en `Scripts/` de REAPER que ejecuta un escenario por nombre y deja el resultado donde el MCP lo lee, y un script de parada para cortar un bucle en marcha.
  - **Escenarios** reutilizables para Melo: armonía, voces, salida MIDI, persistencia y GUI. Cada uno escribe sus tomas y sus comprobaciones.
  - **Analizador en Python** (`analyze.py`) que lee las tomas y los registros de la GUI e imprime `PASS`/`FAIL` por comprobación y un total.
- `tools/install.sh --test` copia el banco a `Effects/GenderBenderTest/` y `Scripts/GenderBenderTest/`. Sin la opción, la instalación no cambia.
- `AGENTS.md`: cómo usar el banco y las trampas de REAPER aprendidas (medida inicial −2 y `beat_position`, no relanzar un script con un bucle `defer` vivo, `noprompt:` para reabrir proyectos, `file_avail` en `@serialize`, grabar la salida MIDI abre diálogos).
- El plugin publicado (`GenderBenderMelo/`, `GenderBender/`) y los estilos no cambian.

## Capabilities

### New Capabilities
- `reaper-test-harness`: banco de pruebas de los plugins en REAPER. Cubre la captura del MIDI de salida, el control de la GUI de una copia de prueba, la ejecución de escenarios desde el MCP, el informe PASS/FAIL y su instalación opcional.

### Modified Capabilities
<!-- Ninguna: los plugins y el formato de estilos no cambian. -->

## Impact

- **Código nuevo**: `tools/reaper_test/` (JSFX del logger, generador de la copia de prueba, Lua, escenarios, analizador).
- **Modificado**: `tools/install.sh` (opción `--test`), `AGENTS.md` (sección de pruebas en REAPER), `README.md` (una línea en la sección de contribución).
- **Sin cambios**: los plugins, sus sliders, los estilos y `check_styles.py`/`check_melo_styles.py`.
- **Dependencias**: REAPER con el MCP de REAPER para lanzar escenarios. El reescalado de ventana usa `js_ReaScriptAPI` si está instalado; si no, esa comprobación sale como `SKIP`, no como `FAIL`.
- **Limpieza**: las copias instaladas a mano en esta sesión (`Effects/GenderBenderTest/`, `Scripts/GenderBenderTest/`) se sustituyen por las instaladas con `--test`.
