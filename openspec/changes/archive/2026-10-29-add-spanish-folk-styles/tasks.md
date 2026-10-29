## 1. Preparación

- [x] 1.1 Leer `styles_src/cumbia_villera_98.style` y `styles_src/jungle_165.style` como modelo de cabecera, bloques y receta de groove
- [x] 1.2 Comprobar que ningún otro cambio de estilos está a medio aplicar (todos editan la tabla del README y `docs/fingerprints.html`)
- [x] 1.3 Consultar referencias escritas de la percusión de cada uno de los 16 estilos (palos flamencos, muiñeira, jota, sardana, arin-arin, tajaraste…) y anotarlas en la cabecera de su fuente
- [x] 1.4 Comprobar con la fórmula de `groove-swing` que, con swing 67, los pasos 0, 2 y 5 de cada negra caen a menos de 3 ms del tresillo exacto al tempo de cada estilo

## 2. Estilos

- [x] 2.0 Escribir los ternarios con la rejilla de tresillos (paso = `(j // 3) × 8 + (0, 2, 5)[j % 3]`), y derivar VARIACIÓN y FILL sin salirse de ella; comprobar que ningún p6, p7 ni p8 repite el de otro estilo
- [x] 2.1 Con un script de un solo uso (fuera de `tools/`), comparar la rejilla `X` de cada BASE prevista en `design.md` con p4/p5 de todos los `drum_styles_v/*.txt`, y ajustar el diseño si alguna coincide en kick, snare y hats
- [x] 2.2 Escribir `styles_src/muineira_120.style` (9 patrones y receta de groove)
- [x] 2.3 Escribir `styles_src/pasacorredoira_110.style` (9 patrones y receta de groove)
- [x] 2.4 Escribir `styles_src/marcha_procesional_70.style` (9 patrones y receta de groove)
- [x] 2.5 Escribir `styles_src/arin_arin_130.style` (9 patrones y receta de groove)
- [x] 2.6 Escribir `styles_src/biribilketa_110.style` (9 patrones y receta de groove)
- [x] 2.7 Escribir `styles_src/jota_aragonesa_60.style` (9 patrones y receta de groove)
- [x] 2.8 Escribir `styles_src/sardana_100.style` (9 patrones y receta de groove)
- [x] 2.9 Escribir `styles_src/ball_de_bastons_110.style` (9 patrones y receta de groove)
- [x] 2.10 Escribir `styles_src/tangos_100.style` (9 patrones y receta de groove)
- [x] 2.11 Escribir `styles_src/tientos_75.style` (9 patrones y receta de groove)
- [x] 2.12 Escribir `styles_src/buleria_80.style` (9 patrones y receta de groove)
- [x] 2.13 Escribir `styles_src/solea_50.style` (9 patrones y receta de groove)
- [x] 2.14 Escribir `styles_src/seguiriya_45.style` (9 patrones y receta de groove)
- [x] 2.15 Escribir `styles_src/sevillana_65.style` (9 patrones y receta de groove)
- [x] 2.16 Escribir `styles_src/fandango_de_huelva_60.style` (9 patrones y receta de groove)
- [x] 2.17 Escribir `styles_src/tajaraste_110.style` (9 patrones y receta de groove)
- [x] 2.18 Generar los `.txt` con `python3 tools/make_style.py build` y revisar cada base con `decode`

## 3. Documentación

- [x] 3.0 Seguir la skill `adding-styles` (tabla del README en orden alfabético, página de huellas y cruce tabla-carpeta)
- [x] 3.0b Añadir al README una nota: los estilos ternarios piden swing global 67
- [x] 3.1 Actualizar en `README.md` la tabla "Included styles": filas nuevas "Flamenco" y "Folk ibérico" en orden alfabético de familias
- [x] 3.2 Regenerar `docs/fingerprints.html` con `python3 tools/view_styles.py` y comprobar que los estilos nuevos salen en su familia

## 4. Verificación

- [x] 4.1 `python3 tools/check_styles.py` imprime `ok`
- [x] 4.2 `git status` no muestra ningún `.txt` anterior como modificado
- [ ] 4.3 En REAPER (`sh tools/install.sh`), con pad en (0,0), Density y Div por defecto y el swing de la receta (67 en los ternarios), grabar la salida MIDI de cada estilo y comprobar que p4/p5 coinciden con los `X` de la fuente
- [ ] 4.4 En REAPER, subir Density por los escalones 52/103/154/205 y comprobar que cada nivel entra sin quitar golpes
- [ ] 4.5 Escuchar los estilos seguidos y confirmar que se distinguen entre sí y del estilo existente más parecido
