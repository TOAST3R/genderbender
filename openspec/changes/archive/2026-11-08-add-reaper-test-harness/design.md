# Design

## Context

El banco nace de la verificación de GenderBender Melo (ver proposal.md, Why). Lo que se sabe de REAPER y que condiciona el diseño:

- **Grabar la salida MIDI no sirve para automatizar**: al empezar y al parar la grabación REAPER abre diálogos modales que bloquean el script y hacen caer el MCP.
- El MCP de REAPER no puede hacer clic dentro de una ventana JSFX ni capturar la pantalla. Solo lanza ReaScripts y lee `reaper_mcp_script_result`.
- **Relanzar un script con un bucle `defer` vivo abre el diálogo «script en marcha»**, que también bloquea REAPER.
- El proyecto por defecto del usuario empieza en la medida −2. `beat_position` cuenta desde el compás 1 y no desde el tiempo 0 del proyecto.
- **`gmem` se comparte entre instancias y sobrevive al cambiar de proyecto**: un valor viejo puede pasar por uno nuevo.
- **Al leer, `file_avail` en `@serialize` devuelve > 0 si quedan datos, no cuántos.**

## Goals / Non-Goals

**Goals:**
- Reproducir en otra sesión, con un solo comando por escenario, las pruebas hechas a mano en esta.
- Que cada comprobación diga qué esperaba y qué vio.

**Non-Goals:**
- Pruebas de píxeles o capturas de la GUI. Se comprueba el estado que la GUI dibuja, no su aspecto.
- Escenarios para el plugin de batería en esta versión. El logger y el lanzador sirven igual, pero los escenarios son de Melo.
- Integración continua: REAPER no corre en CI.

## Decisions

### D1. Logger con `gmem` en lugar de grabar ítems
El logger escribe en `gmem` (namespace `gbtestlog`): el contador en `gmem[0]` y 5 valores por evento (beat, estado, d1, d2, `midi_bus + 100·id`). Lua lo vuelca a un archivo de texto. Sin ítems no hay diálogos, se ve el bus (la grabación lo pierde) y la posición es exacta. Alternativa descartada: grabar con «Record: output (MIDI)», por los diálogos y la pérdida del bus.

### D2. Copia de prueba generada por inyección de texto
`make_test_jsfx.py` copia el JSFX y le inyecta líneas en puntos ancla. Cada ancla debe aparecer exactamente una vez; si no, el generador falla. Las inyecciones son:
- nombre `… TEST` y `options:gmem=gbtestgui`;
- `gfx_showmenu` → función que devuelve `gmem[4]`;
- tras calcular `ox/oy`, `mouse_x/y/cap` desde una cola de pasos en `gmem` (x, y, botones, fotogramas) mientras queden pasos. Un clic o un arrastre se escribe entero antes de empezar, porque un fotograma con el ratón real en medio soltaría el arrastre;
- exportaciones en el aviso de estilo, el panel de progresión y el final de `@gfx`.

El índice de cada posición de `gmem` se documenta en un único sitio, compartido por el generador y la biblioteca Lua.

Alternativa descartada: un slider o un hook de pruebas en el plugin publicado, porque añadiría superficie pública y sliders que no se pueden quitar después.

### D3. Rutas resueltas desde el script instalado
El lanzador busca su propia carpeta (`debug.getinfo(1, "S").source`) y carga `lib.lua` y los escenarios desde ahí. Los resultados se escriben en `Scripts/GenderBenderTest/out/`. El nombre del escenario a ejecutar llega en un ExtState (`gbtest`/`scenario`), que el MCP no puede escribir directamente. Por eso hay un lanzador fijo por escenario (`run_<escenario>.lua`), generado por `install.sh --test`, para que `script_run` lo invoque por ruta.

### D4. Escenarios como datos más comprobaciones
Cada escenario es un archivo Lua que devuelve una lista de pasos de reproducción o de GUI. Las comprobaciones que dependen del estado vivo (sliders, `gmem` de la GUI) se hacen en Lua y se escriben como líneas `PASS`/`FAIL`/`SKIP`. Las que dependen del MIDI se hacen en `analyze.py` sobre las tomas, porque comparar notas, acordes y escalas es mucho más claro en Python. El analizador junta ambas y da el total y el código de salida.

### D5. Defensas contra los diálogos y el estado viejo
- Cada escenario termina su bucle `defer` y el script de parada pone un ExtState que todos los bucles consultan.
- Reabrir proyectos con `Main_openProject("noprompt:…")`.
- Antes de comprobar, se ponen a −1 las posiciones de `gmem` que se van a leer, y la espera de fotogramas exige que avance el contador de fotogramas. Si no avanza en 5 s, la acción falla.
- Antes de cada escenario se para el transporte y se restaura el proyecto de prueba. Los escenarios trabajan en un proyecto propio (`out/test_project.rpp`), nunca en el del usuario.

### D6. Instalación con `--test`
`install.sh --test`:
1. hace la instalación normal;
2. genera la copia de prueba con `make_test_jsfx.py`;
3. copia el logger y la copia a `Effects/GenderBenderTest/`;
4. copia la biblioteca, los escenarios y los lanzadores a `Scripts/GenderBenderTest/`.

Sin la opción, el script sigue igual línea a línea en lo que instala.

## Risks / Trade-offs

- [El plugin cambia y una ancla de inyección desaparece] → El generador falla con el nombre del ancla. Se actualiza el ancla en el mismo cambio que toca la GUI.
- [Escenarios que dependen de los estilos actuales (BULERIA iv–bIII–bII–I)] → Las expectativas se leen del estilo compilado cuando es posible (raíces, escala) en lugar de fijarlas a mano.
- [REAPER sin dispositivo de audio no mueve el transporte] → El lanzador comprueba que el transporte avanza y, si no, falla con «abre el dispositivo de audio».
- [El reescalado necesita `js_ReaScriptAPI`] → Sin él, esas comprobaciones salen como `SKIP`.
- [`gmem` compartido entre el logger y la GUI] → Namespaces distintos (`gbtestlog` y `gbtestgui`), y la biblioteca vuelve a enlazar el correcto antes de cada lectura.

## Migration Plan

Primero se instala con `--test`. Después se borran las copias hechas a mano en esta sesión (`Effects/GenderBenderTest/gbmelo_log.jsfx`, `genderbender_melo_test.jsfx`, `Scripts/GenderBenderTest/gbmelo_*.lua`), que usan nombres y rutas del scratchpad. Para quitar el banco basta con borrar las dos carpetas `GenderBenderTest`.
