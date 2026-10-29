## 1. Preparación

- [x] 1.1 Leer `styles_src/cumbia_villera_98.style` y `styles_src/jungle_165.style` como modelo de cabecera, bloques y receta de groove
- [x] 1.2 Comprobar que ningún otro cambio de estilos está a medio aplicar (todos editan la tabla del README y `docs/fingerprints.html`); si `add-fingerprints-audio-preview` sigue abierto, aplicar este encima conservando los `(bpm)`
- [x] 1.3 Consultar referencias escritas de BREAKSTEP, WONKY, BLEEP TECHNO, HYPNOTIC TECHNO, ROCKERS, STEPPERS, DIGITAL DANCEHALL y TWO TONE, y anotarlas en la cabecera de su fuente

## 2. Estilos

- [x] 2.0 Derivar VARIACIÓN y FILL de la base de cada estilo y comprobar que ningún p6, p7 ni p8 repite el de otro estilo generado (si coincide, dejarlo vacío)
- [x] 2.1 Con un script de un solo uso (fuera de `tools/`), comparar la rejilla `X` de cada BASE prevista en `design.md` con p4/p5 de todos los `drum_styles_v/*.txt`, y ajustar el diseño si alguna coincide en kick, snare y hats
- [x] 2.2 Escribir `styles_src/speed_garage_135.style` (9 patrones y receta de groove)
- [x] 2.3 Escribir `styles_src/bassline_138.style` (9 patrones y receta de groove)
- [x] 2.4 Escribir `styles_src/breakstep_140.style` (9 patrones y receta de groove)
- [x] 2.5 Escribir `styles_src/wonky_140.style` (9 patrones y receta de groove)
- [x] 2.6 Escribir `styles_src/bleep_techno_122.style` (9 patrones y receta de groove)
- [x] 2.7 Escribir `styles_src/ambient_techno_120.style` (9 patrones y receta de groove)
- [x] 2.8 Escribir `styles_src/tribal_techno_130.style` (9 patrones y receta de groove)
- [x] 2.9 Escribir `styles_src/deep_techno_124.style` (9 patrones y receta de groove)
- [x] 2.10 Escribir `styles_src/hypnotic_techno_130.style` (9 patrones y receta de groove)
- [x] 2.11 Escribir `styles_src/peak_time_techno_132.style` (9 patrones y receta de groove)
- [x] 2.12 Escribir `styles_src/industrial_techno_140.style` (9 patrones y receta de groove)
- [x] 2.13 Escribir `styles_src/ska_120.style` (9 patrones y receta de groove)
- [x] 2.14 Escribir `styles_src/rocksteady_80.style` (9 patrones y receta de groove)
- [x] 2.15 Escribir `styles_src/roots_reggae_75.style` (9 patrones y receta de groove)
- [x] 2.16 Escribir `styles_src/dub_70.style` (9 patrones y receta de groove)
- [x] 2.17 Escribir `styles_src/rockers_80.style` (9 patrones y receta de groove)
- [x] 2.18 Escribir `styles_src/steppers_75.style` (9 patrones y receta de groove)
- [x] 2.19 Escribir `styles_src/two_tone_160.style` (9 patrones y receta de groove)
- [x] 2.20 Escribir `styles_src/digital_dancehall_95.style` (9 patrones y receta de groove)
- [x] 2.21 Escribir `styles_src/modern_dancehall_100.style` (9 patrones y receta de groove)
- [x] 2.22 Generar los `.txt` con `python3 tools/make_style.py build` y revisar cada base con `decode`

## 3. Documentación

- [x] 3.0 Seguir la skill `adding-styles` (tabla del README en orden alfabético, página de huellas y cruce tabla-carpeta)
- [x] 3.1 Actualizar en `README.md` la tabla "Included styles": filas UK garage (con grime y dubstep), Techno en orden cronológico, Reggae / dancehall nueva y Reggaeton / funk carioca
- [x] 3.2 Regenerar `docs/fingerprints.html` con `python3 tools/view_styles.py` y comprobar que los estilos nuevos salen en su familia

## 4. Verificación

- [x] 4.1 `python3 tools/check_styles.py` imprime `ok`
- [x] 4.2 `git status` no muestra ningún `.txt` anterior como modificado
- [ ] 4.3 En REAPER (`sh tools/install.sh`), con pad en (0,0), Density y Div por defecto y el swing de la receta, grabar la salida MIDI de cada estilo y comprobar que p4/p5 coinciden con los `X` de la fuente
- [ ] 4.4 En REAPER, subir Density por los escalones 52/103/154/205 y comprobar que cada nivel entra sin quitar golpes
- [ ] 4.5 Escuchar los estilos seguidos y confirmar que se distinguen entre sí y del estilo existente más parecido
