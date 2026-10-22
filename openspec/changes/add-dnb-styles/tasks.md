## 1. Preparación

- [ ] 1.1 Confirmar que `five-level-density-scale` está aplicado: `make_style.py` acepta `,` y `x` vale 204
- [ ] 1.2 Leer `styles_src/cumbia_villera_98.style` como modelo de cabecera, bloques y receta de groove

## 2. Estilos

- [ ] 2.1 Escribir `styles_src/jungle_165.style` (9 patrones y receta de groove)
- [ ] 2.2 Escribir `styles_src/ragga_jungle_165.style`
- [ ] 2.3 Escribir `styles_src/hardstep_172.style`
- [ ] 2.4 Escribir `styles_src/jump_up_174.style`
- [ ] 2.5 Escribir `styles_src/dancefloor_dnb_174.style`
- [ ] 2.6 Escribir `styles_src/techstep_172.style`
- [ ] 2.7 Escribir `styles_src/halftime_174.style`
- [ ] 2.8 Generar los siete `.txt` con `python3 tools/make_style.py build` y revisar cada base con `decode`

## 3. Documentación

- [ ] 3.1 Actualizar en `README.md` la tabla "Included styles" (familia Drum & bass) y el recuento de estilos

## 4. Verificación

- [ ] 4.1 `python3 tools/check_styles.py` imprime `ok`
- [ ] 4.2 `git status` no muestra ningún `.txt` anterior como modificado
- [ ] 4.3 En REAPER (`sh tools/install.sh`), con pad en (0,0) y Density y Div por defecto, grabar la salida MIDI de cada estilo y comprobar que p4/p5 coinciden con los `X` de la fuente
- [ ] 4.4 En REAPER, subir Density por los escalones 52/103/154/205 y comprobar que cada nivel entra sin quitar golpes
- [ ] 4.5 Escuchar los siete estilos seguidos y confirmar que se distinguen
