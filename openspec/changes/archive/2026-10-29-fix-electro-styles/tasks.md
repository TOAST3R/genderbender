## 1. Preparación

- [x] 1.1 Leer `styles_src/cumbia_villera_98.style` y `styles_src/jungle_165.style` como modelo de cabecera, bloques y receta de groove
- [x] 1.2 Comprobar que ningún otro cambio de estilos está a medio aplicar (todos editan la tabla del README y `docs/fingerprints.html`)
- [x] 1.3 Consultar referencias escritas de Cybotron, Planet Rock, Model 500 / Drexciya, Miami bass, electroclash, darkwave y outrun, y anotarlas en la cabecera de cada fuente
- [x] 1.4 Añadir a `tools/check_styles.py` la comprobación de BASE no vacía y comprobar que falla con los cuatro estilos rotos

## 2. Estilos

- [x] 2.0 Borrar `ELECTRO CYBOTRON.txt`, `ELECTRO UR 138.txt`, `BASS 101.txt` y `AFRO BEAT.txt` con `git rm`
- [x] 2.1 Derivar VARIACIÓN y FILL de la base de cada estilo y comprobar que ningún p6, p7 ni p8 repite el de otro estilo
- [x] 2.1b Con un script de un solo uso (fuera de `tools/`), comparar la rejilla `X` de cada BASE prevista en `design.md` con p4/p5 de todos los `drum_styles_v/*.txt`, y ajustar el diseño si alguna coincide en kick, snare y hats
- [x] 2.2 Escribir `styles_src/cybotron_electro_125.style` (9 patrones y receta de groove)
- [x] 2.3 Escribir `styles_src/electro_funk_127.style` (9 patrones y receta de groove)
- [x] 2.4 Escribir `styles_src/darkwave_120.style` (9 patrones y receta de groove)
- [x] 2.5 Escribir `styles_src/electro_bass_130.style` (9 patrones y receta de groove)
- [x] 2.6 Escribir `styles_src/detroit_electro_130.style` (9 patrones y receta de groove)
- [x] 2.7 Escribir `styles_src/electroclash_125.style` (9 patrones y receta de groove)
- [x] 2.8 Escribir `styles_src/electro_house_128.style` (9 patrones y receta de groove)
- [x] 2.9 Escribir `styles_src/outrun_118.style` (9 patrones y receta de groove)
- [x] 2.10 Escribir `styles_src/industrial_electro_130.style` (9 patrones y receta de groove)
- [x] 2.11 Generar los `.txt` con `python3 tools/make_style.py build` y revisar cada base con `decode`

## 3. Documentación

- [x] 3.0 Seguir la skill `adding-styles` (tabla del README en orden alfabético, página de huellas y cruce tabla-carpeta)
- [x] 3.1 Actualizar en `README.md` la tabla "Included styles": fila "Electro" nueva en orden cronológico, quitar los cuatro estilos borrados y mover SYNTHWAVE, DARK ELECTRO y GHETTOTECH
- [x] 3.2 Regenerar `docs/fingerprints.html` con `python3 tools/view_styles.py` y comprobar que los estilos nuevos salen en su familia

## 4. Verificación

- [x] 4.1 `python3 tools/check_styles.py` imprime `ok`
- [x] 4.2 `git status` muestra solo los cuatro `.txt` borrados y ningún otro `.txt` anterior modificado
- [ ] 4.3 En REAPER (`sh tools/install.sh`), con pad en (0,0), Density y Div por defecto y el swing de la receta, grabar la salida MIDI de cada estilo y comprobar que p4/p5 coinciden con los `X` de la fuente
- [ ] 4.4 En REAPER, subir Density por los escalones 52/103/154/205 y comprobar que cada nivel entra sin quitar golpes
- [ ] 4.5 Escuchar los estilos seguidos y confirmar que se distinguen entre sí y del estilo existente más parecido
