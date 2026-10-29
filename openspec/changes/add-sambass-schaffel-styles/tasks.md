## 1. Preparación

- [ ] 1.1 Leer `styles_src/cumbia_villera_98.style` y `styles_src/jungle_165.style` como modelo de cabecera, bloques y receta de groove
- [ ] 1.2 Comprobar que ningún otro cambio de estilos está a medio aplicar (todos editan la tabla del README y `docs/fingerprints.html`)

## 2. Estilos

- [ ] 2.1 Con un script de un solo uso (fuera de `tools/`), comparar la rejilla `X` de cada BASE prevista en `design.md` con p4/p5 de todos los `drum_styles_v/*.txt`, y ajustar el diseño si alguna coincide en kick, snare y hats
- [ ] 2.2 Escribir `styles_src/sambass_172.style` (9 patrones y receta de groove)
- [ ] 2.3 Escribir `styles_src/schaffel_125.style` (9 patrones y receta de groove)
- [ ] 2.4 Generar los `.txt` con `python3 tools/make_style.py build` y revisar cada base con `decode`

## 3. Documentación

- [ ] 3.1 Actualizar en `README.md` la tabla "Included styles": SAMBASS 172 en "Drum & bass" y SCHAFFEL 125 en "Techno"
- [ ] 3.2 Regenerar `docs/fingerprints.html` con `python3 tools/view_styles.py` y comprobar que los estilos nuevos salen en su familia

## 4. Verificación

- [ ] 4.1 `python3 tools/check_styles.py` imprime `ok`
- [ ] 4.2 `git status` no muestra ningún `.txt` anterior como modificado
- [ ] 4.3 En REAPER (`sh tools/install.sh`), con pad en (0,0), Density y Div por defecto y el swing de la receta, grabar la salida MIDI de cada estilo y comprobar que p4/p5 coinciden con los `X` de la fuente
- [ ] 4.4 En REAPER, subir Density por los escalones 52/103/154/205 y comprobar que cada nivel entra sin quitar golpes
- [ ] 4.5 Escuchar los estilos seguidos y confirmar que se distinguen entre sí y del estilo existente más parecido
