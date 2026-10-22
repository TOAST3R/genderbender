## ADDED Requirements

### Requirement: Escala de cinco niveles
El formato `.style` SHALL usar la escala `X=255`, `x=204`, `o=153`, `-=102`, `,=51` y `.=0`, y SHALL seguir aceptando `[n]` para cualquier valor exacto entre 0 y 255.

#### Scenario: Símbolos de la escala
- **WHEN** se construye una cuadrícula `Xxo-,...` de 16 pasos
- **THEN** los pasos pares 0–10 del `.txt` valen 255, 204, 153, 102, 51 y 0

#### Scenario: Valor exacto
- **WHEN** una cuadrícula contiene `[170]`
- **THEN** ese paso vale 170 en el `.txt`

## MODIFIED Requirements

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
