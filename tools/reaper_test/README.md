# Banco de pruebas en REAPER

Verifica GenderBender Melo dentro de REAPER sin mirar a mano. Un logger JSFX captura el MIDI de salida y una copia de prueba del plugin deja que un script maneje la GUI. Los escenarios se lanzan desde el MCP de REAPER, y `analyze.py` da `PASS`/`FAIL`/`SKIP` por comprobación.

| Archivo | Qué es |
|---|---|
| `gbtest_log.jsfx` | Logger: deja pasar el MIDI y anota cada evento en `gmem` `gbtestlog`. |
| `make_test_jsfx.py` | Genera la copia de prueba de Melo (`genderbender_melo_test.jsfx`) inyectando líneas en anclas. |
| `lib.lua` | Biblioteca: proyecto de prueba, sliders, tomas, ratón y menús simulados, registro. |
| `run.lua` | Lanzador. `install.sh --test` lo copia como `run_<escenario>.lua` por cada escenario. |
| `stop.lua` | Para el escenario en marcha y restaura los estilos truncados. |
| `scenarios/*.lua` | `harmony`, `voices`, `output`, `persistence`, `gui`. |
| `analyze.py` | Lee el registro y las tomas de un escenario e imprime el informe. Código 1 si hay algún `FAIL`. |

## Uso

1. Instalar: `sh tools/install.sh --test`. Copia el logger y la copia de prueba a `Effects/GenderBenderTest/`, y la biblioteca, los escenarios y los lanzadores a `Scripts/GenderBenderTest/`.
2. En REAPER: abrir el dispositivo de audio (sin él el transporte no se mueve) y arrancar el servidor del MCP.
3. Lanzar un escenario desde el MCP: `script_run("GenderBenderTest/run_harmony.lua")`. Devuelve `started harmony -> …/out/harmony.log` y el escenario sigue solo en segundo plano. Trabaja en un proyecto propio en otra pestaña (`out/test_project.rpp`) y no toca el del usuario.
4. Esperar a que termine: la última línea de `out/<escenario>.log` empieza por `DONE`. Hasta entonces no lanzar otro escenario. Para cortarlo: `script_run("GenderBenderTest/stop.lua")`.
5. Analizar: `python3 tools/reaper_test/analyze.py harmony` (varios escenarios a la vez también). Con otra carpeta de REAPER: `REAPER_DIR=…` o `--out DIR`.

El escenario `gui` necesita la ventana flotante del plugin abierta y visible (la abre él). Las comprobaciones de reescalado necesitan la extensión `js_ReaScriptAPI`; sin ella salen como `SKIP`.

Para quitar el banco basta con borrar las dos carpetas `GenderBenderTest`.

## Resultados (`Scripts/GenderBenderTest/out/`)

- `<escenario>.log`: líneas `PASS`/`FAIL`/`SKIP` de las comprobaciones hechas en Lua, `TAKE <nombre> <n> eventos` por toma y `DONE …` al final. Un `DONE` con paréntesis (`(parado)`, `(sin GUI)`, `(transporte parado)`) indica que el escenario se cortó.
- `<toma>.txt`: un evento por línea, `beat tipo canal d1 d2 bus+100·id`. `beat` es `beat_position` (0 = compás 1 de la regla). `tipo` es 1 NoteOn, 0 NoteOff, 2 CC. Primero van los eventos del logger 0, luego los del 1, etc., cada uno en su orden de emisión.
- `g_ind.csv`: muestras del indicador de progresión durante la toma `g_ind` (columnas: beat y `gmem` 50–57).

## Tabla de `gmem`

Es la única referencia de los índices. El generador (`make_test_jsfx.py`), la biblioteca y los escenarios usan estos.

### Logger, namespace `gbtestlog`

Cada logger escribe en su zona, `base = id * 200000` (`id` = slider 1 del logger, 0–9). Las pistas se procesan en hilos distintos y un contador compartido perdería eventos.

| Índice | Contenido |
|---|---|
| `base` | Número de eventos. Lua lo pone a 0 antes de cada toma. |
| `base + 1 + 5i` | beat del evento `i` (`beat_position` + desplazamiento dentro del bloque) |
| `base + 2 + 5i` | byte de estado |
| `base + 3 + 5i` | dato 1 |
| `base + 4 + 5i` | dato 2 |
| `base + 5 + 5i` | `midi_bus + 100 * id` |

### Copia de prueba, namespace `gbtestgui`

Escritos por Lua, leídos por el plugin:

| Índice | Contenido |
|---|---|
| 0 | Pasos de ratón simulado que quedan en la cola. Mientras sea > 0, el plugin usa la cola en lugar del ratón real. Lua lo escribe el último, cuando la cola ya está completa. |
| 4 | Respuesta de los menús (como `gfx_showmenu`: 1 = primera opción, 0 = cancelar) |
| 100 + 4k … 103 + 4k | Paso `k` de la cola: x, y (unidades de la GUI, 900×540; el plugin aplica su escala y su margen), `mouse_cap` (1 botón izquierdo, 2 derecho) y fotogramas que dura. |

Escritos por el plugin:

| Índice | Contenido |
|---|---|
| 5 | Menús abiertos (contador) |
| 6 | Paso actual de la cola de ratón (Lua lo pone a 0 al escribir una cola) |
| 9 | Fotogramas dibujados (contador). Las esperas de la biblioteca exigen que avance. |
| 20 | Escala `sc` |
| 21, 22 | Margen `ox`, `oy` |
| 23, 24 | `gfx_w`, `gfx_h` |
| 25 | 1 si la GUI escalada cabe en la ventana |
| 30, 31, 32 | Contador de motivos (dado motivo) de bajo, acordes y melodía |
| 33 | `progSalt` (dado prog) |
| 34 | `diceN` (tiradas de dado) |
| 35, 36 | slider 5 y 6 (pad) |
| 37 | `dragId` (control que se arrastra) |
| 40, 41, 42 | 1 si la voz (bajo, acordes, melodía) muestra «estilo invalido» |
| 50 | Hueco del acorde marcado en el ciclo |
| 51 | Raíz absoluta del acorde de ese hueco |
| 52 | 1 si se ve «cambio pendiente» |
| 53 | Progresión del ciclo (−1 = markov) |
| 54 | Número de ciclo |
| 55 | Tónica del ciclo |
| 56 | 1 si hay un acorde marcado (reproduciendo y dentro del ciclo) |
| 57 | Huecos del ciclo |
| 60 … 60 + n − 1 | Raíz de cada hueco |

Las posiciones 40–42 y 50–57 solo se escriben cuando se dibuja esa parte. Antes de comprobarlas, el escenario las pone a −1 para no leer un valor de otra ejecución: `gmem` se comparte entre instancias y sobrevive al cambiar de proyecto.

## Trampas de REAPER

- **No grabar la salida MIDI.** Al empezar y al parar la grabación REAPER abre diálogos modales que bloquean el script y hacen caer el MCP. Por eso el logger escribe en `gmem`.
- **No relanzar un script cuyo bucle `defer` sigue vivo**: REAPER abre el diálogo «script en marcha» y bloquea todo. Los escenarios terminan solos y `stop.lua` los corta por ExtState sin relanzar nada. `run_*.lua` se niega a arrancar si ya hay uno en marcha.
- **Medida inicial distinta de 1.** El proyecto por defecto del usuario empieza en la medida −2. `beat_position` cuenta desde el compás 1 de la regla, no desde el tiempo 0. Analizar con `beat_position` (es lo que guardan las tomas), no con QN del proyecto. `beatTime()` de la biblioteca hace la conversión.
- **Reabrir sin diálogo**: `Main_openProject("noprompt:" .. ruta)`, después de guardar.
- **`file_avail` en `@serialize`** devuelve > 0 si quedan datos al leer, no cuántos.
- **Dispositivo de audio**: sin él el transporte no avanza. La toma falla con «abre el dispositivo de audio de REAPER».
- **JSFX editado en disco**: hay que quitarlo y volver a ponerlo en la cadena para que se recompile. La biblioteca crea el proyecto de prueba desde cero en cada escenario.
- **`EnumerateFiles` guarda el listado en caché**: tras borrar un archivo puede seguir devolviéndolo. Llamar antes con índice −1 para vaciar la caché, reunir los nombres y comprobar que cada archivo existe antes de abrirlo. Un error de Lua dentro de un bucle `defer` abre un diálogo y detiene también el servidor del MCP.
- **Filtro de bus de un envío MIDI**: `I_MIDIFLAGS = bus << 14`. `I_MIDI_SRCBUS` se lee como 0 y no hace nada.
