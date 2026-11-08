# Tasks

## 1. Formato y herramientas de estilos melódicos

- [x] 1.1 Crear el módulo común de teoría (escalas como máscara de 12 bits, grados romanos → raíz y máscara de intervalos según la escala, alfabetos de altura por voz). Verificar con pruebas en `tools/` que `V7` en A menor armónica da raíz 7 y la máscara {0,4,7,10}, y que `bII` en frigia dominante da raíz 1.
- [x] 1.2 Implementar `tools/make_melo_style.py build` (cabecera, armonía, carriles `rhy/deg/voi/cnt/art`, grupos `[p0 p1]`, 16 → 32 pasos, 24 pasos en ternario) que escribe el compilado numérico de design D2 con `MAGIC` al inicio y al final. Verificar que un `.mstyle` de prueba compila y que los errores de símbolo, patrón que falta o grado desconocido nombran el archivo, el carril y la posición.
- [x] 1.3 Implementar `tools/make_melo_style.py decode`. Verificar la ida y vuelta: build → decode → build da un compilado idéntico.
- [x] 1.4 Implementar `tools/check_melo_styles.py` (recompila y compara, comprueba conteos, rangos, filas de Markov > 0 y `MAGIC`). Verificar que imprime `ok` con estilos correctos y nombra un estilo desactualizado tras editar su fuente.
- [x] 1.5 Documentar el formato `.mstyle` en `README.md` (sección GenderBender Melo) y las reglas nuevas en `AGENTS.md` (no editar `melo_styles/*.txt` a mano, ejecutar `check_melo_styles.py`). Verificar que el ejemplo del README compila con el comando documentado.

## 2. Estilos de la v1

- [x] 2.1 Escribir `styles_melo_src/cumbia_colombiana.mstyle` según la spec `melo-styles` (bajo R/5 en 1 y 3, acordes a contratiempo, ≥3 progresiones, Markov y una sustitución). Verificar con `check_melo_styles.py` → `ok` y con `decode` que la BASE (p4/p5) cumple el escenario del bajo.
- [x] 2.2 Escribir ROOTS REGGAE (one drop, skank en 2 y 4). Verificar con `check_melo_styles.py` y `decode`.
- [x] 2.3 Escribir ACID HOUSE (semicorcheas con ≥2 slides en la BASE, stabs m7). Verificar con `check_melo_styles.py` y `decode`.
- [x] 2.4 Escribir BULERIA (24 pasos, frigia dominante con tónica E, cadencia andaluza iv–bIII–bII–I como primera progresión). Verificar con `check_melo_styles.py` y `decode`.
- [x] 2.5 Escribir LIQUID DNB (maj7/m9, ii–V–I, bajo ligado). Verificar con `check_melo_styles.py` y `decode`.
- [x] 2.6 Escribir SON (tumbao sin el tiempo 1, montuno). Verificar con `check_melo_styles.py` y `decode`.
- [x] 2.7 Añadir al validador la comprobación de que los nombres coinciden con estilos de batería y que los BPM son los mismos. Verificar que imprime `ok`.

## 3. Esqueleto del plugin y carga de estilos

- [x] 3.1 Crear `GenderBenderMelo/genderbender_melo.jsfx` con el mapa de sliders de design D9, `ext_midi_bus = 1` y un `@serialize` vacío preparado. Verificar en REAPER que compila sin errores y que los 53 sliders aparecen y se pueden automatizar.
- [x] 3.2 Cargar el estilo de cada voz con `file_var` y comprobar `MAGIC` y `VERSION`. Si no son válidos, marcar la voz como inválida y mostrarlo en la GUI. Verificar en REAPER con un compilado truncado a propósito (en el scratchpad, no en `melo_styles/`).
- [x] 3.3 Ampliar `tools/install.sh` para copiar `GenderBenderMelo/` y `melo_styles/`. Verificar con `sh tools/install.sh` que el plugin aparece en REAPER como MIDI GenderBender Melo.

## 4. Director armónico

- [x] 4.1 Implementar el PRNG por claves de design D5. Verificar que las mismas claves dan el mismo resultado tras recargar el plugin: misma semilla y ajustes, mismo MIDI antes y después de quitar y volver a poner el plugin (comprobado con un registro MIDI en REAPER en lugar de una función de depuración en la GUI).
- [x] 4.2 Implementar la voz maestra, la tónica, el ritmo armónico, la longitud de ciclo y el modo fija/ciclo/aleatoria. Verificar en REAPER grabando la salida de la voz de acordes con BULERIA en modo fija (iv–bIII–bII–I sobre la tónica elegida).
- [x] 4.3 Implementar las sustituciones con tensión y el modo Markov con resolución a la tónica al cerrar el ciclo. Verificar que con tensión 0 la grabación es igual a la de modo fija y que en Markov el último acorde del ciclo es i.
- [x] 4.4 Aplicar los cambios en el límite del ciclo, la modulación cada N ciclos y el indicador de progresión con acorde actual y cambio pendiente. Verificar en REAPER pulsando cambios a mitad de ciclo.

## 5. Voces y pad

- [x] 5.1 Implementar los pesos bilineales del pad como tabla de cuadrantes (misma geometría que gb_18), el peso por voz y el ritmo por densidad. Verificar que con peso 0 el bajo toca siempre su BASE (p4/p5) aunque se mueva el pad.
- [x] 5.2 Implementar el sorteo ponderado de altura y articulación entre esquinas. Verificar que con el pad en una esquina la altura grabada coincide siempre con la del patrón (`decode`).
- [x] 5.3 Implementar el bajo (grados sobre el acorde, aproximación, octava). Verificar la quinta sobre iv en A menor (A) y el tumbao de SON en la grabación.
- [x] 5.4 Implementar los acordes (voicings, voice leading de mínimo movimiento, registro y strum). Verificar en la grabación que Am → Dm elige la inversión de menor movimiento y que el strum a 20 ms separa las notas 10 ms.
- [x] 5.5 Implementar la melodía (contorno sobre la escala, gravedad en tiempos fuertes, salto máximo y registro con salto de octava). Verificar en la grabación que las notas de los tiempos fuertes pertenecen al acorde.
- [x] 5.6 Implementar los controles por voz (duración, velocidad, swing y slide reutilizando las reglas de `groove-swing` y `voice-slide`) y la rejilla de 24 pasos. Verificar que BULERIA con swing 50 cae en tresillos.

## 6. Salida MIDI

- [x] 6.1 Implementar la cola de 256 eventos con nota, canal y bus, emisión sample-accurate y prioridad de NoteOff. Verificar con la grabación que las notas caen en su sample de rejilla con swing 50.
- [x] 6.2 Implementar el modo canal/bus, el destino por voz y los acordes partidos (base + n, con tope en 16). Verificar en REAPER con tres pistas receptoras por bus y por canal.
- [x] 6.3 Implementar el legato (NoteOn antes del NoteOff) y el slide con CC 65. Verificar en la grabación de ACID HOUSE el orden de eventos y el CC.
- [x] 6.4 Implementar la tabla de notas activas por destino y el todo NoteOff en stop, seek, vuelta de loop y cambio de destino. Verificar en REAPER que no quedan notas colgadas en ningún caso, incluidos acordes partidos.

## 7. Generación por frases

- [x] 7.1 Implementar el motivo por frase calculado desde el índice de frase (design D6) y la forma de frase (A, A', B). Verificar con AAAA y evolución 0 que los cuatro compases grabados son iguales y que B termina en nota del acorde.
- [x] 7.2 Implementar las variaciones (≤ ⅓ de las notas, tiempos fuertes conservados) y la re-armonización del motivo al cambiar de acorde. Verificar en la grabación.
- [x] 7.3 Implementar la evolución y el recálculo tras un seek. Verificar que dos reproducciones desde el mismo punto (una tras un seek) dan el mismo MIDI.
- [x] 7.4 Implementar el lock por voz con el buffer en `@serialize`. Verificar que una voz bloqueada ignora el pad y la densidad y que se conserva al reabrir el proyecto.

## 8. Azar

- [x] 8.1 Implementar ALL RND, EACH RND, el dado de progresión, el dado de motivo por voz y el dado de tónica según la spec `melo-randomization`, respetando los locks y guardando el resultado como estado. Verificar en REAPER cada escenario y que el resultado se conserva al reabrir el proyecto.

## 9. Interfaz

- [x] 9.1 Dibujar la GUI con `gfx_*`: selectores de estilo por voz, pad XY, panel de progresión, controles globales y una fila de controles por voz con lock y dado. Verificar en REAPER que todos los controles responden y que la ventana se reescala.
- [x] 9.2 Documentar el uso en `README.md` (instalación, enrutado por canal o bus, acordes partidos, lock y semilla). Verificar que los pasos del README funcionan en una instalación limpia.

## 10. Integración

- [x] 10.1 Prueba completa en REAPER: los 6 estilos como maestro, cruces con EACH RND, modo bus con acordes partidos, transporte con loops y seeks. Grabar el MIDI de las tres salidas y comprobar tonalidad común, ausencia de notas colgadas y reproducibilidad con la misma semilla. Verificar también que `python3 tools/check_styles.py` y `python3 tools/check_melo_styles.py` imprimen `ok` y que gb_18 sigue funcionando igual.

## Workflow follow-up

- Archivar el cambio con `/opsx:archive` cuando la prueba en REAPER esté completa.
- No hacer push sin el visto bueno del usuario.
