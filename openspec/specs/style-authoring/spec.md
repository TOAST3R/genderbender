# style-authoring Specification

## Purpose
TBD - created by archiving change add-cumbia-styles. Update Purpose after archive.
## Requirements
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
`tools/make_style.py decode <estilo.txt>` SHALL emitir una fuente `.style` para cualquier estilo bien formado (32 enteros por patrón). Cada valor SHALL ajustarse al nivel más cercano de la escala (`round(v / 51) * 51`) y escribirse con su símbolo, sin `[n]`. Un estilo corrupto SHALL rechazarse con un error que identifique el patrón afectado.

#### Scenario: Ajuste al nivel más cercano
- **WHEN** se decodifica un patrón con los valores 255, 170, 85, 128 y 20
- **THEN** se emiten `X`, `o`, `-`, `o` y `.`

#### Scenario: Round-trip de valores en escala
- **WHEN** se decodifica y se reconstruye un `.txt` cuyos valores son todos 0, 51, 102, 153, 204 o 255
- **THEN** el resultado es idéntico al original

#### Scenario: Estilo corrupto
- **WHEN** se decodifica un `.txt` con un patrón que no son 32 enteros (por ejemplo `bdrum1|i`)
- **THEN** el comando falla indicando ese patrón, sin traceback

### Requirement: Escala de cinco niveles
El formato `.style` SHALL usar la escala `X=255`, `x=204`, `o=153`, `-=102`, `,=51` y `.=0`, y SHALL seguir aceptando `[n]` para cualquier valor exacto entre 0 y 255.

#### Scenario: Símbolos de la escala
- **WHEN** se construye una cuadrícula `Xxo-,...` de 16 pasos
- **THEN** los pasos pares 0–10 del `.txt` valen 255, 204, 153, 102, 51 y 0

#### Scenario: Valor exacto
- **WHEN** una cuadrícula contiene `[170]`
- **THEN** ese paso vale 170 en el `.txt`

### Requirement: Base no vacía
`python3 tools/check_styles.py` SHALL fallar, nombrando el estilo, si algún `drum_styles_v/*.txt` tiene el patrón p4 o el p5 sin ninguna nota.

#### Scenario: Base vacía
- **WHEN** un estilo tiene p4 o p5 a 0 en todas las voces
- **THEN** `check_styles.py` sale con error y nombra ese estilo

#### Scenario: Todos con base
- **WHEN** todos los estilos tienen notas en p4 y p5
- **THEN** `check_styles.py` imprime `ok`

