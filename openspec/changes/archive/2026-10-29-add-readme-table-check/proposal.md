## Why

La página de huellas saca las familias de la tabla "Included styles" del README. Si un estilo no aparece en la tabla cae en "Other" sin aviso, y si la tabla nombra un estilo que ya no existe nadie se entera. Ya pasó: el commit `7db9261` añadió 23 estilos sin tocar la tabla, y en ella seguían `TEST2` y `ZZZZ BLACK`, que no existían. Hoy solo lo evita la skill `adding-styles`, que es un recordatorio: un agente que no la cargue (o una persona) puede saltárselo y `check_styles.py` sigue diciendo `ok`.

## What Changes

- `tools/check_styles.py` falla si algún `drum_styles_v/*.txt` no tiene entrada en la tabla "Included styles" del README (ni en una familia ni por su nombre en "Other").
- También falla si una entrada de la tabla no corresponde a ningún `.txt`.
- La comprobación usa la misma regla de emparejado que la página (`view_styles.families()`): una entrada `NOMBRE (bpm)` vale para `NOMBRE.txt` y `NOMBRE bpm.txt`; sin `(bpm)`, el nombre tal cual.
- La skill `adding-styles` deja de pedir el cruce a mano: lo hace `check_styles.py`.

## Capabilities

### New Capabilities

### Modified Capabilities
- `style-fingerprints`: `check_styles.py` exige que la tabla del README y la carpeta de estilos coincidan.

## Impact

- `tools/check_styles.py` y `.claude/skills/adding-styles/SKILL.md`.
- Hoy la tabla y la carpeta coinciden (193 estilos), así que el cambio no rompe nada. `add-world-folk-styles`, que sigue abierto, tendrá que añadir sus filas para que `check_styles.py` pase, que es justo lo que se quiere.
