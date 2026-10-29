## 1. Preparación

- [x] 1.1 Leer `styles_src/cumbia_villera_98.style` y `styles_src/jungle_165.style` como modelo de cabecera, bloques y receta de groove
- [x] 1.2 Comprobar que ningún otro cambio de estilos está a medio aplicar (todos editan la tabla del README y `docs/fingerprints.html`)
- [x] 1.3 Consultar referencias escritas de cada estilo (claves cubanas, surdo y tamborim, train beat, bodhrán, dhol, keherwa…) y anotarlas en la cabecera de su fuente

## 2. Estilos

- [x] 2.0 Escribir los ternarios en la rejilla de tresillos y derivar VARIACIÓN y FILL sin salirse de ella; comprobar que ningún p6, p7 ni p8 repite el de otro estilo
- [x] 2.1 Con un script de un solo uso (fuera de `tools/`), comparar la rejilla `X` de cada BASE prevista en `design.md` con p4/p5 de todos los `drum_styles_v/*.txt`, y ajustar el diseño si alguna coincide en kick, snare y hats
- [x] 2.2 Escribir `styles_src/blues_shuffle_100.style` (9 patrones y receta de groove)
- [x] 2.3 Escribir `styles_src/western_swing_170.style` (9 patrones y receta de groove)
- [x] 2.4 Escribir `styles_src/bluegrass_120.style` (9 patrones y receta de groove)
- [x] 2.5 Escribir `styles_src/country_shuffle_120.style` (9 patrones y receta de groove)
- [x] 2.6 Escribir `styles_src/train_beat_110.style` (9 patrones y receta de groove)
- [x] 2.7 Escribir `styles_src/rockabilly_180.style` (9 patrones y receta de groove)
- [x] 2.8 Escribir `styles_src/zydeco_120.style` (9 patrones y receta de groove)
- [x] 2.9 Escribir `styles_src/two_step_140.style` (9 patrones y receta de groove)
- [x] 2.10 Escribir `styles_src/reel_110.style` (9 patrones y receta de groove)
- [x] 2.11 Escribir `styles_src/jig_115.style` (9 patrones y receta de groove)
- [x] 2.12 Escribir `styles_src/strathspey_120.style` (9 patrones y receta de groove)
- [x] 2.13 Escribir `styles_src/irish_polka_140.style` (9 patrones y receta de groove)
- [x] 2.14 Escribir `styles_src/son_95.style` (9 patrones y receta de groove)
- [x] 2.15 Escribir `styles_src/rumba_guaguanco_100.style` (9 patrones y receta de groove)
- [x] 2.16 Escribir `styles_src/bolero_80.style` (9 patrones y receta de groove)
- [x] 2.17 Escribir `styles_src/merengue_130.style` (9 patrones y receta de groove)
- [x] 2.18 Escribir `styles_src/mambo_190.style` (9 patrones y receta de groove)
- [x] 2.19 Escribir `styles_src/cha_cha_cha_120.style` (9 patrones y receta de groove)
- [x] 2.20 Escribir `styles_src/kompa_120.style` (9 patrones y receta de groove)
- [x] 2.21 Escribir `styles_src/salsa_180.style` (9 patrones y receta de groove)
- [x] 2.22 Escribir `styles_src/bachata_130.style` (9 patrones y receta de groove)
- [x] 2.23 Escribir `styles_src/maracatu_90.style` (9 patrones y receta de groove)
- [x] 2.24 Escribir `styles_src/frevo_140.style` (9 patrones y receta de groove)
- [x] 2.25 Escribir `styles_src/samba_100.style` (9 patrones y receta de groove)
- [x] 2.26 Escribir `styles_src/baiao_100.style` (9 patrones y receta de groove)
- [x] 2.27 Escribir `styles_src/axe_130.style` (9 patrones y receta de groove)
- [x] 2.28 Escribir `styles_src/candombe_110.style` (9 patrones y receta de groove)
- [x] 2.29 Escribir `styles_src/tango_64.style` (9 patrones y receta de groove)
- [x] 2.30 Escribir `styles_src/milonga_90.style` (9 patrones y receta de groove)
- [x] 2.31 Escribir `styles_src/chacarera_70.style` (9 patrones y receta de groove)
- [x] 2.32 Escribir `styles_src/huayno_90.style` (9 patrones y receta de groove)
- [x] 2.33 Escribir `styles_src/huapango_110.style` (9 patrones y receta de groove)
- [x] 2.34 Escribir `styles_src/son_jarocho_120.style` (9 patrones y receta de groove)
- [x] 2.35 Escribir `styles_src/freylekhs_130.style` (9 patrones y receta de groove)
- [x] 2.36 Escribir `styles_src/bhangra_95.style` (9 patrones y receta de groove)
- [x] 2.37 Escribir `styles_src/keherwa_100.style` (9 patrones y receta de groove)
- [x] 2.38 Generar los `.txt` con `python3 tools/make_style.py build` y revisar cada base con `decode`

## 3. Documentación

- [x] 3.0 Seguir la skill `adding-styles` (tabla del README en orden alfabético, página de huellas y cruce tabla-carpeta)
- [x] 3.1 Actualizar en `README.md` la tabla "Included styles": seis filas nuevas en orden alfabético de familias, y los ternarios en la nota del swing 67
- [x] 3.2 Regenerar `docs/fingerprints.html` con `python3 tools/view_styles.py` y comprobar que los estilos nuevos salen en su familia

## 4. Verificación

- [x] 4.1 `python3 tools/check_styles.py` imprime `ok`
- [x] 4.2 `git status` no muestra ningún `.txt` anterior como modificado
- [ ] 4.3 En REAPER (`sh tools/install.sh`), con pad en (0,0), Density y Div por defecto y el swing de la receta (67 en los ternarios), grabar la salida MIDI de cada estilo y comprobar que p4/p5 coinciden con los `X` de la fuente
- [ ] 4.4 En REAPER, subir Density por los escalones 52/103/154/205 y comprobar que cada nivel entra sin quitar golpes
- [ ] 4.5 Escuchar los estilos seguidos y confirmar que se distinguen entre sí y del estilo existente más parecido
