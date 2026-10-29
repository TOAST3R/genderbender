## Why

Los 73 estilos de `add-techno-house-hardcore-rave-styles` y `add-pulseroots-styles` tienen bases (p4/p5) distintas, pero sus patrones VARIACIÓN y FILL salen de las mismas reglas: solo hay 3 FILL (p8) distintos entre los 73, y uno lo comparten 54 estilos. En la página de huellas se ven iguales. Además, ESTAIL y GQOM son idénticos en los 9 patrones. Antes que tener patrones repetidos, se prefiere quitarlos.

## What Changes

- En los 73 estilos generados, cada p6, p7 y p8 que se repita en otro estilo generado se queda solo en uno (el primero por orden alfabético) y se vacía en los demás: el FILL queda vacío en 70 estilos y la VARIACIÓN (p6/p7) en GABBER 180 y GABBER ROLL 180, que repetían la de FULL-ON 145.
- Se borra `ESTAIL` (idéntico a `GQOM`): su `.txt` y su entrada en la fila "Other" del README.
- `docs/fingerprints.html` regenerado.
- Sin cambios en el plugin ni en `tools/`. Los estilos anteriores a hoy no se tocan, salvo ESTAIL.

## Capabilities

### New Capabilities

### Modified Capabilities
- `techno-house-hardcore-rave-styles`: p6, p7 y p8 pueden quedar vacíos cuando repetirían los de otro estilo.
- `pulseroots-styles`: lo mismo.

## Impact

- `styles_src/` (los 73 `.style` generados) y sus `.txt`; `drum_styles_v/ESTAIL.txt` borrado; `README.md`; `docs/fingerprints.html`.
- Con el pad en la zona de FILL, los 70 estilos sin p8 no tocan nada; GABBER 180 y GABBER ROLL 180 tampoco tocan en la zona de VARIACIÓN.
