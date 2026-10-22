## ADDED Requirements

### Requirement: Generación de la página de huellas
`python3 tools/view_styles.py` SHALL leer todos los `drum_styles_v/*.txt` y escribir `docs/fingerprints.html`, un único archivo autocontenido que no cargue recursos externos (sin CDN, fuentes ni imágenes remotas). Para los mismos estilos SHALL producir siempre el mismo archivo byte a byte.

#### Scenario: Regenerar sin cambios
- **WHEN** se ejecuta `view_styles.py` dos veces sin tocar los estilos
- **THEN** `docs/fingerprints.html` es idéntico tras ambas ejecuciones

#### Scenario: Página sin red
- **WHEN** se abre `docs/fingerprints.html` desde el disco sin conexión
- **THEN** se ven todos los estilos y el slider funciona

#### Scenario: Estilo corrupto
- **WHEN** un `.txt` de `drum_styles_v/` no se puede decodificar
- **THEN** el comando falla con el mensaje de `StyleError` que nombra el archivo y no escribe la página

### Requirement: Tira de 9 patrones por estilo
Cada estilo SHALL mostrarse como una tira con sus 9 patrones (p0–p8) en orden. Cada patrón SHALL mostrar las 7 voces (filas, en el orden `bdrum, sdrum, clap, hhclosed, hhopen, hitom, lotom`) por 32 pasos (columnas), con un color cuya intensidad crece con el valor 0–255 y fondo para 0. Si el p8 tiene todas sus voces a 0, la tira SHALL marcarlo como FILL vacío.

#### Scenario: p8 vacío
- **WHEN** se genera la página con `GQOM`, cuyo p8 está vacío
- **THEN** la tira de GQOM marca su p8 como FILL vacío

#### Scenario: Recuento
- **WHEN** hay 31 estilos en `drum_styles_v/`
- **THEN** la página muestra 31 tiras de 9 patrones cada una

### Requirement: Agrupación por familia
Los estilos SHALL agruparse bajo las familias de la tabla "Included styles" del README, en el orden de la tabla. Un estilo pertenece a una entrada de la tabla si su nombre es igual al de la entrada sin el `(bpm)` final, o a ese nombre seguido de un espacio y el bpm. Los estilos que no correspondan a ninguna entrada SHALL ir a la familia "Other".

#### Scenario: Nombre con bpm en el archivo
- **WHEN** el README lista `CUMBIA COLOMBIANA (95)` en Cumbia y existe `CUMBIA COLOMBIANA 95.txt`
- **THEN** ese estilo aparece en la familia Cumbia

#### Scenario: Estilo no listado
- **WHEN** existe un `.txt` cuyo nombre no aparece en la tabla
- **THEN** aparece en la familia "Other"

### Requirement: Filtro de Density
La página SHALL tener un slider de Density de 0 a 260 con valor inicial 50. Un paso con valor v SHALL mostrarse a intensidad plena si `256 − v < Density` y atenuado en otro caso, en todas las tiras y en la vista ampliada.

#### Scenario: Density por defecto
- **WHEN** el slider está en 50
- **THEN** solo los pasos con v ≥ 207 se ven a intensidad plena

#### Scenario: Density al máximo
- **WHEN** el slider está en 260
- **THEN** todos los pasos con v > 0 se ven a intensidad plena

### Requirement: Vista ampliada
Al hacer clic en una tira, o pulsar Enter con ella enfocada, la página SHALL mostrar ese estilo con sus 9 patrones a mayor tamaño, con los nombres de las voces y una marca cada 8 pasos. Escape o un clic fuera del panel SHALL cerrarla.

#### Scenario: Abrir y cerrar
- **WHEN** se hace clic en la tira de `TekkThump` y luego se pulsa Escape
- **THEN** se abre la vista ampliada de TekkThump y después se cierra

### Requirement: Página al día con los estilos
`tools/check_styles.py` SHALL fallar con un error si `docs/fingerprints.html` no existe o no coincide con lo que generaría `view_styles.py` con los estilos actuales.

#### Scenario: Estilo nuevo sin regenerar
- **WHEN** se añade un `.txt` a `drum_styles_v/` sin ejecutar `view_styles.py`
- **THEN** `check_styles.py` informa que `docs/fingerprints.html` está desfasado y sale con código 1

#### Scenario: Página al día
- **WHEN** se ejecuta `view_styles.py` y luego `check_styles.py`
- **THEN** `check_styles.py` imprime `ok`
