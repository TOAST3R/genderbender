# Proposal

## Why

GenderBender genera baterías, pero en el proyecto no hay nada para bajo, acordes ni melodía. Un plugin hermano, con la misma forma de trabajar (estilos por género, pad XY que mezcla 9 patrones, densidad, botones de azar) y los mismos nombres de géneros, completaría la "banda" generativa. Sería un producto aparte que vive en el mismo repo y comparte herramientas y convenciones.

## What Changes

- Nuevo plugin JSFX **GenderBender Melo** (`GenderBenderMelo/genderbender_melo.jsfx`), independiente de `genderbender.jsfx`. No modifica el plugin de batería ni sus sliders.
- Tres voces en un mismo plugin: **bajo**, **acordes** y **melodía**. Cada una puede tener su propio género, y los tres comparten un **pad XY global**. Cada voz tiene un **peso de pad** (0 = ignora el pad).
- **Director armónico**: la tónica, la escala y la progresión salen del estilo de la **voz maestra**, que se elige entre bajo, acordes o melodía. La progresión se elige de un banco del género o se randomiza en cuatro niveles: ciclo del banco, aleatoria del banco, sustituciones según un control de **tensión** y cadena de Markov del género. Ofrece ritmo armónico configurable y cambio de tónica opcional.
- **Altura relativa**: el bajo se escribe en grados relativos al acorde, los acordes como ritmo más tipo de voicing, y la melodía como contorno sobre la escala, con gravedad hacia notas del acorde en los tiempos fuertes.
- **Generación por frases**: cada voz genera motivos que se recuerdan, varían y responden según la forma de frase del estilo (AA'AB…). Un control de **evolución** decide cuánto muta el motivo en cada frase. Hay **lock** por voz para congelar lo generado y una **semilla** que se guarda en el preset.
- **Azar con alcance definido**: ALL RND, EACH RND y dados de progresión, de motivo por voz y de tónica.
- **Salidas MIDI independientes** por canal MIDI o por bus MIDI de REAPER (seleccionable). Los acordes salen polifónicos en un canal o **partidos**, con cada nota del acorde en su propio canal o bus.
- **Nuevo formato de estilo melódico** con fuente legible (`styles_melo_src/*.mstyle`), un compilador (`tools/make_melo_style.py`) y un validador (`tools/check_melo_styles.py`). Los estilos compilados van en `melo_styles/`. El estilo declara su compás, y así los ternarios ya no dependen de ajustar el swing a mano.
- **v1 con 6 estilos** muy distintos entre sí, con nombres tomados de gb_18: CUMBIA COLOMBIANA, ROOTS REGGAE, ACID HOUSE, BULERIA, LIQUID DNB y SON.
- `tools/install.sh` también instala el plugin melódico y sus estilos.

## Capabilities

### New Capabilities
- `melo-style-format`: formato fuente y compilado de los estilos melódicos, compilador y validador.
- `melo-harmony`: director armónico (tónica, escala, banco de progresiones, sustituciones con tensión, Markov, voz maestra, ritmo armónico, cambio de tónica).
- `melo-voices`: comportamiento de bajo, acordes y melodía. Cubre ritmo por densidad, altura relativa, pad XY global con peso por voz, articulación, octava y duración.
- `melo-phrase-generation`: motivos, forma de frase, variación, evolución, lock y semilla.
- `melo-randomization`: alcance de ALL RND, EACH RND y de cada dado.
- `melo-midi-output`: salida por canal o bus, acordes polifónicos o partidos, emisión sample-accurate, legato y manejo de transporte sin notas colgadas.
- `melo-styles`: los 6 estilos de la v1 y su carácter musical (escala, progresiones, rol rítmico de cada voz).

### Modified Capabilities
<!-- Ninguna: el plugin de batería y sus specs no cambian. -->

## Impact

- **Código nuevo**: `GenderBenderMelo/` (plugin y fondo), `styles_melo_src/`, `melo_styles/`, `tools/make_melo_style.py`, `tools/check_melo_styles.py`.
- **Modificado**: `tools/install.sh` (copia también el plugin melódico y `melo_styles/`), `README.md` y `AGENTS.md` (sección del plugin melódico y reglas de su formato).
- **Sin cambios**: `genderbender.jsfx`, `drum_styles_v/`, sus sliders y presets.
- **Dependencias**: ninguna nueva. Los buses MIDI solo funcionan en REAPER. Con ysfx en otros DAWs se usan los canales MIDI.
- **Verificación**: el validador en Python para los estilos y la prueba en REAPER para el plugin (grabar las salidas MIDI y comprobar tonalidad, canales y que no haya notas colgadas).
