## ADDED Requirements

### Requirement: Generación de estilos desde fuente legible
`tools/make_style.py build <fuente.style> [destino]` SHALL generar un `.txt` con el formato exacto del editor: 7 voces en el orden `bdrum, sdrum, clap, hhclosed, hhopen, hitom, lotom` separadas por `/`, 9 patrones por voz separados por tabulador con el formato `<voz><i>|v0,…,v31`, y un tabulador final sin salto de línea. Los patrones y voces que no se especifiquen SHALL quedar a 0.

#### Scenario: Semicorcheas expandidas
- **WHEN** una línea de voz tiene 16 caracteres de cuadrícula
- **THEN** el carácter i se escribe en el paso 2i y los pasos impares quedan a 0

#### Scenario: Bloque multi-patrón con sobrescritura
- **WHEN** un bloque `[p4 p5]` define el kick y un bloque posterior `[p5]` lo redefine
- **THEN** p4 conserva el kick del primer bloque y p5 usa el del segundo

### Requirement: Validación de la fuente
La herramienta SHALL rechazar con un error, indicando el número de línea, cualquier voz, patrón o carácter desconocido y cualquier longitud distinta de 16 o 32, y en ese caso no SHALL escribir ningún archivo.

#### Scenario: Longitud inválida
- **WHEN** una cuadrícula tiene 15 caracteres
- **THEN** el comando falla con un mensaje que incluye el número de línea y no crea ningún `.txt`

### Requirement: Decodificación de estilos existentes
`tools/make_style.py decode <estilo.txt>` SHALL emitir una fuente `.style` equivalente para cualquier estilo bien formado (32 enteros por patrón), y volver a construirla SHALL producir un archivo idéntico byte a byte. Un estilo corrupto SHALL rechazarse con un error que identifique el patrón afectado.

#### Scenario: Round-trip de los estilos incluidos
- **WHEN** se decodifica y se reconstruye cualquier `.txt` bien formado de `drum_styles_v/`
- **THEN** el resultado es idéntico al original

#### Scenario: Estilo corrupto
- **WHEN** se decodifica un `.txt` con un patrón que no son 32 enteros (por ejemplo `bdrum1|i`)
- **THEN** el comando falla indicando ese patrón, sin traceback
