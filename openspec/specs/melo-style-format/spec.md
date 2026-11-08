# melo-style-format Specification

## Purpose
Define cómo se escribe, compila y valida un estilo melódico de GenderBender Melo, para que un estilo mal formado se detecte antes de llegar al plugin en lugar de silenciarlo.

## Requirements

### Requirement: Fuente legible por estilo
Cada estilo melódico SHALL escribirse como un archivo de texto `styles_melo_src/<nombre>.mstyle` con cabecera (nombre, BPM, compás, escala), sección de armonía (banco de progresiones, tabla de Markov, sustituciones, forma de frase) y patrones de las tres voces.

#### Scenario: Estilo mínimo completo
- **WHEN** un `.mstyle` declara cabecera, al menos una progresión en el banco y los carriles de las tres voces
- **THEN** el compilador lo acepta y genera el archivo compilado en `melo_styles/`

### Requirement: Rejilla de 9 patrones × 32 pasos por voz
Cada voz SHALL tener 9 patrones (p0–p8) de 32 pasos. Cada paso SHALL tener un valor de ritmo de 0 a 255, una altura y una articulación. Los grupos de patrones (`[p0 p1]`) y los niveles de ritmo (`X x o - , .` y `[n]`) SHALL funcionar como en los `.style` de batería.

#### Scenario: Patrón de 16 caracteres
- **WHEN** un carril tiene 16 caracteres de ritmo
- **THEN** se interpreta como semicorcheas y se expande a 32 pasos

#### Scenario: Patrones sin declarar
- **WHEN** un estilo no declara alguno de los 9 patrones de una voz
- **THEN** el compilador falla con un mensaje que indica la voz y el patrón que faltan

### Requirement: Alfabeto de altura por voz
El bajo SHALL escribir su altura como grado relativo al acorde (`R 3 5 7 8` y `a` para aproximación cromática). Los acordes SHALL escribir el tipo de voicing (triada, 7ª, 9ª, sus, power, shell). La melodía SHALL escribir contorno (`+` sube grado, `-` baja, `=` repite, `^` salto a nota del acorde).

#### Scenario: Símbolo no válido
- **WHEN** un carril de altura del bajo contiene un símbolo que no está en su alfabeto
- **THEN** el compilador falla e indica el archivo, el carril y la posición

### Requirement: Articulación por paso
Cada paso con nota SHALL poder marcarse como corta, ligada (sin NoteOff hasta la siguiente nota) o con slide (ligada y con portamento).

#### Scenario: Paso ligado
- **WHEN** un paso del bajo está marcado como ligado y el siguiente paso suena
- **THEN** el estilo compilado conserva esa marca para que el plugin emita la nota siguiente antes del NoteOff de la anterior

### Requirement: Compás declarado
El estilo SHALL declarar su compás (binario o ternario). Un estilo ternario SHALL sonar correctamente sin que el usuario cambie el swing global.

#### Scenario: Estilo ternario con swing neutro
- **WHEN** se carga BULERIA con el swing global a 50
- **THEN** los pasos caen en la subdivisión ternaria del estilo

### Requirement: Escala y armonía válidas
Las escalas SHALL tomarse de una lista conocida (mayor, menor natural, menor armónica, dórica, frigia, frigia dominante, mixolidia, pentatónicas). Las progresiones SHALL escribirse en números romanos: sin alteración, el número es el grado de la escala del estilo; con `b` o `#`, es el grado de la escala mayor alterado (`bII` = 1 semitono). Mayúscula es acorde mayor y minúscula menor, con sufijos `7 maj7 9 m9 maj9 6 add9 sus2 sus4 ° ø +`. Las filas de la tabla de Markov SHALL sumar más de 0.

#### Scenario: Grado inexistente
- **WHEN** una progresión usa un número romano que el compilador no reconoce
- **THEN** el compilador falla con un mensaje que nombra el acorde

### Requirement: Validador de estilos melódicos
`python3 tools/check_melo_styles.py` SHALL recompilar cada `.mstyle`, compararlo con su archivo de `melo_styles/` y comprobar la estructura de cada compilado. SHALL imprimir `ok` solo si todos son válidos y están al día.

#### Scenario: Compilado desactualizado
- **WHEN** se edita un `.mstyle` sin volver a compilarlo
- **THEN** el validador lo nombra como desactualizado y no imprime `ok`

#### Scenario: Todo correcto
- **WHEN** todos los estilos compilan y coinciden con sus compilados
- **THEN** el validador imprime `ok`

### Requirement: Decodificación inversa
`tools/make_melo_style.py decode <archivo>` SHALL imprimir un estilo compilado en formato legible equivalente al `.mstyle`.

#### Scenario: Ida y vuelta
- **WHEN** se compila un `.mstyle`, se decodifica y se vuelve a compilar
- **THEN** el segundo compilado es idéntico al primero
