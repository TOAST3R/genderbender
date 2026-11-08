# Tasks

## 1. Captura del MIDI

- [x] 1.1 Crear `tools/reaper_test/gbtest_log.jsfx` (namespace `gbtestlog`, slider de id, registra también tras el stop) a partir del logger de esta sesión. Verificar en REAPER que con Melo en modo buses y tres receptoras de id 1–3 el volcado distingue bus y logger, y que los NoteOff del stop aparecen.
- [x] 1.2 Documentar la tabla de posiciones de `gmem` (logger y GUI) en `tools/reaper_test/README.md`, la referencia que usan el generador y la biblioteca. Verificar que cada índice usado en el código aparece en la tabla.

## 2. Copia de prueba de la GUI

- [x] 2.1 Crear `tools/reaper_test/make_test_jsfx.py` (anclas únicas, namespace `gbtestgui`, ratón y menús simulados, exportación del estado dibujado) con salida a una ruta dada. Verificar con `diff` que solo cambian las líneas inyectadas y el nombre, y que al cambiar a propósito un ancla en una copia temporal del JSFX el generador falla nombrando esa línea.

## 3. Biblioteca, escenarios y lanzador

- [x] 3.1 Crear `tools/reaper_test/lib.lua` sin rutas fijas (carpeta propia por `debug.getinfo`, `out/`, sliders, secuencias de reproducción, volcado, parada por ExtState, reapertura con `noprompt:`, espera de fotogramas que falla si la GUI no dibuja). Verificar en REAPER que una secuencia de dos tomas termina sola y que, con la ventana cerrada, una acción de GUI da `FAIL` en vez de quedarse esperando.
- [x] 3.2 Crear el lanzador por escenario y `stop.lua`. Verificar con el MCP que `script_run` de un lanzador devuelve el resultado en `reaper_mcp_script_result` y que `stop.lua` corta un escenario reproduciendo sin abrir el diálogo de script en marcha al relanzar.
- [x] 3.3 Escribir los escenarios de Melo en `tools/reaper_test/scenarios/`:
  - `harmony`: fija, ciclo, ½ compás, sustituciones, Markov, modulación, maestra y progresión en el límite del ciclo, tónica;
  - `voices`: BASE, pad, quinta sobre iv, voice leading, strum, swing;
  - `output`: slide y CC 65, canal y bus a receptoras, acordes partidos, stop, seek, loop, cambio de destino;
  - `persistence`: lock y dados al reabrir, recarga del plugin, semilla, proyecto en formato anterior;
  - `gui`: aviso, indicador, pad, deslizadores, botones, menús, reescalado y dados.

  Verificar que cada escenario se ejecuta de principio a fin en REAPER y deja sus tomas y su registro en `out/`.

## 4. Analizador

- [x] 4.1 Crear `tools/reaper_test/analyze.py` (lee tomas y registros, comprobaciones de MIDI por escenario con las expectativas leídas del estilo compilado, total y código de salida, `SKIP` para lo no disponible). Verificar que con la versión actual de Melo los cinco escenarios salen sin `FAIL`.
- [x] 4.2 Verificar que el banco detecta los errores que encontró: con el reinicio de deslizadores antiguo (3/100/20) aplicado a una copia del JSFX, el escenario `gui` da `FAIL` con ambos valores y `analyze.py` termina con código 1.

## 5. Instalación y documentación

- [x] 5.1 Añadir `--test` a `tools/install.sh` (genera la copia, crea los lanzadores y copia todo a `Effects/GenderBenderTest/` y `Scripts/GenderBenderTest/`). Verificar que sin `--test` el resultado de la instalación es idéntico al de antes (listado de archivos y `cmp`) y que con `--test` los cinco escenarios se lanzan desde el MCP.
- [x] 5.2 Documentar el banco en `AGENTS.md` (sección Checks) y en `tools/reaper_test/README.md`: uso desde el MCP y trampas de REAPER (medida −2 y `beat_position`, no relanzar un script vivo, `noprompt:`, `file_avail` en `@serialize`, grabar abre diálogos, dispositivo de audio). Añadir una línea en la sección de contribución del `README.md`. Verificar que los pasos de `tools/reaper_test/README.md` funcionan tras borrar las carpetas `GenderBenderTest` e instalar con `--test`.
- [x] 5.3 Borrar de REAPER las copias hechas a mano en la sesión anterior (`gbmelo_log.jsfx`, `genderbender_melo_test.jsfx`, `gbmelo_*.lua`). Verificar que solo queda lo instalado con `--test`.

## Workflow follow-up

- Archivar con `/opsx:archive` cuando las tareas estén hechas.
- No hacer push sin el visto bueno del usuario.
