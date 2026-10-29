## 1. Preparación

- [x] 1.1 Leer `styles_src/cumbia_villera_98.style` y `styles_src/jungle_165.style` como modelo de cabecera, bloques y receta de groove
- [x] 1.2 Comprobar que ningún otro cambio de estilos está a medio aplicar (todos editan la tabla del README y `docs/fingerprints.html`)
- [x] 1.3 Consultar referencias escritas de SKWEEE, DECONSTRUCTED CLUB, SINGELI, NORTEC, BAKALAO, HARDGROOVE, FUNK DE RAIZ, MOTORIK y los tres phonk, y anotarlas en la cabecera de su fuente

## 2. Estilos

- [x] 2.1 Con un script de un solo uso (fuera de `tools/`), comparar la rejilla `X` de cada BASE prevista en `design.md` con p4/p5 de todos los `drum_styles_v/*.txt`, y ajustar el diseño si alguna coincide en kick, snare y hats
- [x] 2.2 Escribir `styles_src/glitch_hop_110.style` (9 patrones y receta de groove)
- [x] 2.3 Escribir `styles_src/idm_120.style` (9 patrones y receta de groove)
- [x] 2.4 Escribir `styles_src/skweee_100.style` (9 patrones y receta de groove)
- [x] 2.5 Escribir `styles_src/deconstructed_club_130.style` (9 patrones y receta de groove)
- [x] 2.6 Escribir `styles_src/microhouse_124.style` (9 patrones y receta de groove)
- [x] 2.7 Escribir `styles_src/dub_techno_118.style` (9 patrones y receta de groove)
- [x] 2.8 Escribir `styles_src/schranz_150.style` (9 patrones y receta de groove)
- [x] 2.9 Escribir `styles_src/hardgroove_135.style` (9 patrones y receta de groove)
- [x] 2.10 Escribir `styles_src/frenchcore_200.style` (9 patrones y receta de groove)
- [x] 2.11 Escribir `styles_src/industrial_hardcore_150.style` (9 patrones y receta de groove)
- [x] 2.12 Escribir `styles_src/hardstyle_150.style` (9 patrones y receta de groove)
- [x] 2.13 Escribir `styles_src/bakalao_125.style` (9 patrones y receta de groove)
- [x] 2.14 Escribir `styles_src/boogie_110.style` (9 patrones y receta de groove)
- [x] 2.15 Escribir `styles_src/motorik_120.style` (9 patrones y receta de groove)
- [x] 2.16 Escribir `styles_src/future_garage_130.style` (9 patrones y receta de groove)
- [x] 2.17 Escribir `styles_src/psybient_100.style` (9 patrones y receta de groove)
- [x] 2.18 Escribir `styles_src/neurofunk_174.style` (9 patrones y receta de groove)
- [x] 2.19 Escribir `styles_src/liquid_dnb_174.style` (9 patrones y receta de groove)
- [x] 2.20 Escribir `styles_src/riddim_140.style` (9 patrones y receta de groove)
- [x] 2.21 Escribir `styles_src/future_bass_150.style` (9 patrones y receta de groove)
- [x] 2.22 Escribir `styles_src/midtempo_bass_105.style` (9 patrones y receta de groove)
- [x] 2.23 Escribir `styles_src/phonk_130.style` (9 patrones y receta de groove)
- [x] 2.24 Escribir `styles_src/drift_phonk_155.style` (9 patrones y receta de groove)
- [x] 2.25 Escribir `styles_src/brazilian_phonk_130.style` (9 patrones y receta de groove)
- [x] 2.26 Escribir `styles_src/broken_beat_120.style` (9 patrones y receta de groove)
- [x] 2.27 Escribir `styles_src/bossa_nova_chill_100.style` (9 patrones y receta de groove)
- [x] 2.28 Escribir `styles_src/dembow_120.style` (9 patrones y receta de groove)
- [x] 2.29 Escribir `styles_src/funk_de_raiz_130.style` (9 patrones y receta de groove)
- [x] 2.30 Escribir `styles_src/singeli_200.style` (9 patrones y receta de groove)
- [x] 2.31 Escribir `styles_src/nortec_125.style` (9 patrones y receta de groove)
- [x] 2.32 Escribir `styles_src/acid_jazz_105.style` (9 patrones y receta de groove)
- [x] 2.33 Generar los `.txt` con `python3 tools/make_style.py build` y revisar cada base con `decode`

## 3. Documentación

- [x] 3.0 Seguir la skill `adding-styles` (tabla del README en orden alfabético, página de huellas y cruce tabla-carpeta)
- [x] 3.1 Actualizar en `README.md` la tabla "Included styles": cuatro filas nuevas en orden alfabético y los demás estilos en sus filas existentes
- [x] 3.2 Regenerar `docs/fingerprints.html` con `python3 tools/view_styles.py` y comprobar que los estilos nuevos salen en su familia

## 4. Verificación

- [x] 4.1 `python3 tools/check_styles.py` imprime `ok`
- [x] 4.2 `git status` no muestra ningún `.txt` anterior como modificado
- [ ] 4.3 En REAPER (`sh tools/install.sh`), con pad en (0,0), Density y Div por defecto y el swing de la receta, grabar la salida MIDI de cada estilo y comprobar que p4/p5 coinciden con los `X` de la fuente
- [ ] 4.4 En REAPER, subir Density por los escalones 52/103/154/205 y comprobar que cada nivel entra sin quitar golpes
- [ ] 4.5 Escuchar los estilos seguidos y confirmar que se distinguen entre sí y del estilo existente más parecido
