# style-fingerprints Specification

## Purpose
TBD - created by archiving change add-style-fingerprints. Update Purpose after archive.
## Requirements
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

### Requirement: Filtro por familia con recuentos
La cabecera de la página SHALL tener un selector de familia con la opción "Todos" seguida de una opción por familia, en el orden de la tabla "Included styles" y con el número de estilos de cada una entre paréntesis. Junto al selector, la página SHALL mostrar el recuento de estilos visibles y el total. Los recuentos SHALL calcularse a partir de los estilos de la página.

#### Scenario: Valor inicial
- **WHEN** se abre la página
- **THEN** el selector está en "Todos (N)", con N el número total de estilos, se ven todas las familias y el recuento dice `N estilos`

#### Scenario: Elegir una familia
- **WHEN** se elige la opción `Cumbia (6)`
- **THEN** solo se ven el encabezado y las 6 tiras de Cumbia, y el recuento dice `6 de N estilos`

#### Scenario: Volver a todos
- **WHEN** se elige "Todos" después de una familia
- **THEN** vuelven a verse todas las familias y el recuento dice `N estilos`

### Requirement: Preview de audio por estilo
Cada estilo de la página SHALL tener un botón Play. Al pulsarlo, la página SHALL tocar en bucle su p4 y su p5, alternando a cada compás, con sonidos sintetizados en el navegador y sin cargar recursos externos, y el botón SHALL pasar a Stop. Solo SHALL sonar un estilo o patrón a la vez. Cada paso SHALL sonar solo si `256 − v < Density`, con el valor actual del slider de Density.

#### Scenario: Play y Stop
- **WHEN** se pulsa Play en un estilo y después Stop
- **THEN** suena su base en bucle hasta pulsar Stop, y el botón vuelve a mostrar Play

#### Scenario: Uno a la vez
- **WHEN** suena un estilo y se pulsa Play en otro
- **THEN** el primero se para, su botón vuelve a Play y suena solo el segundo

#### Scenario: Esc
- **WHEN** suena un estilo, la vista ampliada está cerrada y se pulsa Esc
- **THEN** la reproducción se para

#### Scenario: Density
- **WHEN** suena un estilo y se sube Density de 50 a 255
- **THEN** a partir del paso siguiente suenan también los pasos con valores menores de 255

#### Scenario: Patrón vacío
- **WHEN** se pulsa el ▶ de un patrón vacío en la vista ampliada
- **THEN** no suena ninguna nota

### Requirement: Preview por patrón
La vista ampliada SHALL tener un ▶ por cada patrón p0–p8 que toque ese patrón en bucle, con las mismas reglas de reproducción única, Density y tempo.

#### Scenario: Escuchar el FILL
- **WHEN** se pulsa el ▶ de p8 en la vista ampliada de un estilo
- **THEN** suena en bucle solo p8 de ese estilo

### Requirement: Tempo de cada estilo
La reproducción SHALL usar el BPM del nombre del estilo (su número final de 2 o 3 cifras entre 60 y 220). Si el nombre no lo lleva, SHALL usar el `(bpm)` de su entrada en la tabla "Included styles" del README, y si tampoco, 120. El paso SHALL durar `60 / BPM / 8` segundos, y la página SHALL mostrar el BPM junto al botón Play.

#### Scenario: BPM en el nombre
- **WHEN** se pulsa Play en `DETROIT TECHNO 128`
- **THEN** suena a 128 BPM

#### Scenario: BPM en el README
- **WHEN** el nombre es `101 JUKE` y su entrada en el README es `101 JUKE (160)`
- **THEN** suena a 160 BPM

#### Scenario: Sin BPM
- **WHEN** un estilo no tiene BPM ni en el nombre ni en el README
- **THEN** suena a 120 BPM

### Requirement: Swing del preview
La cabecera SHALL tener un slider de swing de 50 a 75 % que SHALL mover el tiempo de cada paso con la misma deformación por corchea que el plugin (`groove-swing`). Al pulsar Play, el slider SHALL pasar al swing de la receta del estilo (cabecera de su `styles_src/*.style`), y cada voz SHALL usar `S_voz = 50 + (S − 50) × amount / 100` con el amount de la receta (100 % si no lo indica). Los estilos sin fuente SHALL sonar con swing 50.

#### Scenario: Swing del estilo
- **WHEN** se pulsa Play en DEEP HOUSE 122, cuya receta es `swing 56 · amount: hhc 100, resto 0`
- **THEN** el slider pasa a 56, el hhc suena con swing 56 y el resto de voces recto

#### Scenario: Estilo sin fuente
- **WHEN** se pulsa Play en un estilo sin `.style` en `styles_src/`
- **THEN** el slider pasa a 50 y todo suena recto

#### Scenario: Ajuste a mano
- **WHEN** suena un estilo y se mueve el slider de swing
- **THEN** los pasos siguientes usan el valor nuevo, con el mismo amount por voz

#### Scenario: Swing por defecto
- **WHEN** el swing está en 50
- **THEN** todos los pasos caen en la rejilla recta

#### Scenario: Swing a 66
- **WHEN** el swing está en 66
- **THEN** la segunda semicorchea de cada corchea suena a 0,33 negras del inicio de la corchea

### Requirement: Tabla del README al día con los estilos
`python3 tools/check_styles.py` SHALL fallar si algún `drum_styles_v/*.txt` no corresponde a ninguna entrada de la tabla "Included styles" del README, y SHALL fallar si alguna entrada de la tabla no corresponde a ningún `.txt`. La correspondencia SHALL usar la misma regla que la página de huellas: una entrada `NOMBRE (bpm)` corresponde a `NOMBRE.txt` y a `NOMBRE bpm.txt`, y una entrada sin `(bpm)` al nombre tal cual. Cada error SHALL nombrar el estilo o la entrada.

#### Scenario: Tabla y carpeta coinciden
- **WHEN** cada `.txt` tiene su entrada en la tabla y cada entrada su `.txt`
- **THEN** `check_styles.py` no informa de ningún error de la tabla

#### Scenario: Estilo sin entrada
- **WHEN** existe `drum_styles_v/NUEVO 120.txt` y la tabla no lo lista
- **THEN** `check_styles.py` sale con error y nombra `NUEVO 120.txt`

#### Scenario: Entrada sin estilo
- **WHEN** la tabla lista `TEST2` y no existe ningún `.txt` que le corresponda
- **THEN** `check_styles.py` sale con error y nombra la entrada `TEST2` y su familia

### Requirement: Render perezoso
La página SHALL crear y pintar los canvas de cada tira solo cuando la tira está en pantalla o a menos de 400 px de ella. El cambio de Density y de tema SHALL repintar solo los canvas ya creados. La vista ampliada SHALL pintarse entera al abrirse.

#### Scenario: Carga
- **WHEN** se abre la página con la ventana arriba del todo
- **THEN** solo existen los canvas de las tiras visibles o cercanas, muchos menos que 9 por estilo

#### Scenario: Scroll
- **WHEN** se baja hasta una familia que no se veía
- **THEN** sus tiras aparecen pintadas con la Density actual

### Requirement: Exportar MIDI
La vista ampliada SHALL tener un botón que descargue `<NOMBRE>.mid`: un MIDI tipo 0 con el tempo del estilo y dos compases de lo que se está oyendo (p4/p5 si es la BASE, o el patrón elegido repetido), con Density y swing aplicados y una nota de 1/32 por paso que suena. Las notas SHALL ser por defecto las del plugin (36 + voz) y, con el interruptor "GM", las de General MIDI (36, 38, 39, 42, 46, 50 y 45). En los navegadores con `DownloadURL`, un asa SHALL permitir arrastrar el mismo archivo fuera de la página.

#### Scenario: Descargar la base
- **WHEN** en la vista ampliada de TRAIN BEAT 110, con Density por defecto, se pulsa ⬇ .mid
- **THEN** se descarga `TRAIN BEAT 110.mid`, a 110 BPM, con 32 notas 37 (snare) y 4 notas 36 (kick) en dos compases

#### Scenario: General MIDI
- **WHEN** se activa "GM" y se descarga el mismo estilo
- **THEN** el snare sale en la nota 38 en lugar de la 37

#### Scenario: Arrastrar
- **WHEN** en Chrome se arrastra el asa ⠿ fuera del navegador
- **THEN** el arrastre lleva `DownloadURL` con tipo `audio/midi` y el nombre `<NOMBRE>.mid`

### Requirement: Enlaces a las fuentes
La vista ampliada SHALL enlazar al `.txt` del estilo en el repositorio de GitHub y, si el estilo tiene fuente en `styles_src/`, a su `.style`.

#### Scenario: Estilo con fuente
- **WHEN** se abre la vista ampliada de SALSA 180
- **THEN** hay enlaces a `drum_styles_v/SALSA 180.txt` y a `styles_src/salsa_180.style`

#### Scenario: Estilo sin fuente
- **WHEN** se abre la vista ampliada de GQOM
- **THEN** solo hay enlace al `.txt`

### Requirement: Permalink
El hash de la URL SHALL guardar el estilo abierto, la Density y el género elegido. Al cargar la página con un hash, la página SHALL aplicar el género, la Density y abrir la vista ampliada del estilo; los valores que no existan SHALL ignorarse.

#### Scenario: Abrir un enlace
- **WHEN** se carga `fingerprints.html#style=SALSA 180&density=120&fam=Latin / Caribbean`
- **THEN** se ve solo la familia Latin / Caribbean, Density está en 120 y la vista ampliada de SALSA 180 está abierta

#### Scenario: Estilo inexistente
- **WHEN** el hash nombra un estilo que no existe
- **THEN** la página carga normal, sin vista ampliada

### Requirement: Density y swing en la vista ampliada
La vista ampliada SHALL tener sus propios controles de Density (0–260) y de swing (50–75), sincronizados con los de la cabecera: moverlos SHALL cambiar lo que suena, lo que se pinta y el MIDI exportado igual que los de la cabecera, y al pulsar Play el control de swing SHALL mostrar el swing de la receta del estilo. El contenido de la página SHALL ir centrado.

#### Scenario: Density desde la vista ampliada
- **WHEN** con la vista ampliada abierta se sube su Density a 200
- **THEN** la Density de la cabecera también vale 200 y las tiras y los patrones ampliados se repintan con ella

#### Scenario: Swing al pulsar Play
- **WHEN** en la vista ampliada de DEEP HOUSE 122 se pulsa el ▶ de un patrón
- **THEN** el swing de la vista ampliada muestra 56

### Requirement: Pad XY del plugin
La vista ampliada SHALL tener un pad de −100 a 100 en cada eje que mezcle los patrones con la misma fórmula que el plugin: el sector se elige con las condiciones `x<0 y<0` → 1, `x<0 y>0` → 2, `x≥0 y≥0` → 3, `x≥0 y≤0` → 4, en ese orden y ganando la última que se cumple; cada voz interpola los valores de cuatro patrones con `X = |x|/100` e `Y = |y|/100` según la fórmula de su sector; y el valor resultante suena si `256 − v < Density`. El pad SHALL poder moverse mientras suena.

#### Scenario: Centro
- **WHEN** el pad está en (0, 0)
- **THEN** suenan las mismas notas que p4 en el compás 1 y p5 en el 2

#### Scenario: Bordes
- **WHEN** el pad está en (100, 0), en (0, −100) o en (100, −100)
- **THEN** suenan p2/p3, p0/p1 o p8, respectivamente

#### Scenario: Discontinuidad del centro
- **WHEN** el pad está en (0, 1)
- **THEN** la mezcla es la del sector 3, igual que en el plugin

### Requirement: Secuencia del estilo
La vista ampliada SHALL tener un botón que toque en bucle INTRO (p0/p1), BASE (p4/p5), ENERGÍA (p2/p3), VARIACIÓN (p6/p7) y FILL (p8, dos veces), saltando las partes vacías y marcando el patrón que suena.

#### Scenario: Estilo con FILL vacío
- **WHEN** se toca la secuencia de un estilo con p8 vacío
- **THEN** después de la VARIACIÓN vuelve a la INTRO sin compases en silencio

### Requirement: Mute y solo por voz
La vista ampliada SHALL tener un control de mute y otro de solo por cada una de las 7 voces. Con algún solo activo SHALL sonar solo las voces en solo. Mute y solo SHALL aplicarse al preview y al MIDI exportado.

#### Scenario: Solo de kick
- **WHEN** se activa el solo del kick y se exporta el MIDI
- **THEN** el archivo solo tiene notas de kick

### Requirement: Comparar dos estilos
La vista ampliada SHALL permitir elegir un segundo estilo y alternar la BASE de los dos cada dos compases, cada uno con su BPM y su swing.

#### Scenario: A/B
- **WHEN** en la vista ampliada de SALSA 180 se elige MAMBO 190 y se activa A/B
- **THEN** suenan dos compases de SALSA 180 a 180 BPM y dos de MAMBO 190 a 190 BPM, en bucle

