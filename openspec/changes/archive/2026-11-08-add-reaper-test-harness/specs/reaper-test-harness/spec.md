# Spec Delta

## Purpose

Banco de pruebas que verifica los plugins JSFX dentro de REAPER sin mirar a mano: captura el MIDI de salida, maneja la GUI de una copia de prueba, ejecuta escenarios lanzados desde el MCP de REAPER e informa PASS/FAIL.

## ADDED Requirements

### Requirement: Captura del MIDI de salida
Un logger JSFX colocado detrás del plugin SHALL dejar pasar todo el MIDI sin cambios y registrar cada evento con su posición exacta en negras (`beat_position` más el desplazamiento dentro del bloque), estado, datos, bus MIDI e identificador de logger. Los eventos que el plugin emite al parar el transporte también SHALL registrarse. La captura SHALL funcionar reproduciendo, sin grabar ítems ni abrir diálogos.

#### Scenario: Bus e identificador
- **WHEN** el plugin está en modo buses y tres pistas receptoras con loggers de id 1, 2 y 3 reciben un envío filtrado por bus
- **THEN** el registro distingue el bus de cada evento y qué logger lo recibió

#### Scenario: NoteOff al parar
- **WHEN** se para el transporte con notas sonando
- **THEN** sus NoteOff aparecen en el registro aunque el transporte ya no esté en marcha

### Requirement: Estado dibujado de la copia de prueba
La copia de prueba SHALL exportar en cada fotograma el estado que dibuja la GUI: aviso de estilo inválido por voz, acorde marcado, aviso de cambio pendiente, escala y tamaño de la ventana, contadores de los dados y un contador de fotogramas.

#### Scenario: Aviso de estilo inválido
- **WHEN** el bajo usa un estilo con el archivo truncado
- **THEN** el estado exportado marca el aviso solo en la voz del bajo

### Requirement: Copia de prueba de la GUI
Un generador SHALL crear, a partir del JSFX publicado, una copia instalable con otro nombre en la que el ratón y la respuesta de los menús los fija el script de prueba. Fuera de las líneas inyectadas, el código SHALL ser idéntico al publicado. El JSFX publicado no SHALL modificarse.

#### Scenario: Punto de inyección perdido
- **WHEN** el plugin cambia y una de las líneas donde se inyecta ya no existe o aparece más de una vez
- **THEN** el generador falla con un mensaje que nombra esa línea y no escribe la copia

#### Scenario: Diferencias acotadas
- **WHEN** se compara la copia generada con el JSFX publicado
- **THEN** las únicas diferencias son las líneas inyectadas y el nombre del plugin

### Requirement: Conductor de la GUI
La biblioteca de pruebas SHALL ofrecer clic, clic derecho, arrastre y elección de menú en coordenadas de la GUI (900×540), independientes del tamaño de la ventana. Cada acción SHALL esperar a que el plugin dibuje los fotogramas necesarios. Si la ventana no dibuja, la acción SHALL fallar en lugar de seguir con datos viejos.

#### Scenario: Ventana reescalada
- **WHEN** la ventana mide 1500×760 y se hace clic en el botón `>` del panel de progresión
- **THEN** la progresión avanza igual que con la ventana a su tamaño original

#### Scenario: Ventana cerrada
- **WHEN** se lanza una acción de GUI con la ventana del plugin cerrada
- **THEN** la comprobación termina con `FAIL` y un mensaje que dice que la GUI no dibuja

### Requirement: Escenarios lanzados desde el MCP
Un lanzador instalado en `Scripts/` de REAPER SHALL ejecutar un escenario por su nombre y devolver un resultado legible por el MCP de REAPER (`reaper_mcp_script_result`). Los escenarios SHALL terminar solos. Un script de parada SHALL cortar cualquier escenario en marcha. Ninguna ruta de la biblioteca ni de los escenarios SHALL depender de la máquina ni de la sesión: SHALL resolverse desde la carpeta instalada o desde el repo.

#### Scenario: Escenario de persistencia
- **WHEN** se lanza el escenario de persistencia con un proyecto guardado
- **THEN** el escenario guarda, reabre el proyecto sin diálogo de guardado, compara estilos, sliders y estado serializado, y repite una toma que debe salir idéntica

#### Scenario: Parada
- **WHEN** se lanza el script de parada con un escenario reproduciendo
- **THEN** el transporte se para, el escenario termina y un nuevo lanzamiento no abre el diálogo de script en marcha

### Requirement: Informe PASS/FAIL
Un analizador en Python SHALL leer las tomas y el registro de la GUI de un escenario e imprimir una línea `PASS`, `FAIL` o `SKIP` por comprobación, con los valores observados, y un total. SHALL salir con código distinto de 0 si hay algún `FAIL`. Una comprobación que depende de algo no instalado (por ejemplo, el reescalado sin `js_ReaScriptAPI`) SHALL salir como `SKIP`.

#### Scenario: Fallo con valores
- **WHEN** el clic derecho en la evolución del bajo deja el slider en 20 y el valor por defecto es 10
- **THEN** el analizador imprime `FAIL`, el nombre de la comprobación y ambos valores, y termina con código 1

#### Scenario: Sin js_ReaScriptAPI
- **WHEN** falta `js_ReaScriptAPI`
- **THEN** las comprobaciones de reescalado salen como `SKIP` y el resto del escenario se ejecuta

### Requirement: Instalación opcional
`tools/install.sh --test` SHALL copiar el logger, la copia de prueba generada, la biblioteca, los escenarios y el lanzador a `Effects/GenderBenderTest/` y `Scripts/GenderBenderTest/` de REAPER, además de la instalación normal. Sin `--test`, `install.sh` SHALL instalar exactamente lo mismo que antes.

#### Scenario: Instalación normal
- **WHEN** se ejecuta `sh tools/install.sh` sin opciones
- **THEN** no se crea ni modifica nada en `Effects/GenderBenderTest/` ni en `Scripts/GenderBenderTest/`
