## 1. Herramienta

- [x] 1.1 Crear `tools/make_style.py` con el parser `.style` (bloques, alias, escala, `[n]`, 16/32) y su validación con número de línea
- [x] 1.2 Implementar `build`, que escribe el `.txt` con el formato exacto (orden de voces, tabuladores, `/` y tabulador final)
- [x] 1.3 Implementar `decode`, que convierte `.txt` en `.style`
- [x] 1.4 Verificar el round-trip byte a byte con todos los `.txt` de `drum_styles_v/` y los errores de validación

## 2. Estilos

- [x] 2.1 Escribir `styles_src/cumbia_colombiana_95.style` (9 patrones y receta de groove)
- [x] 2.2 Escribir `styles_src/cumbia_sonidera_92.style`
- [x] 2.3 Escribir `styles_src/cumbia_villera_98.style`
- [x] 2.4 Escribir `styles_src/cumbia_digital_100.style`
- [x] 2.5 Escribir `styles_src/cumbia_rebajada_72.style`
- [x] 2.6 Generar los cinco `.txt` en `drum_styles_v/`

## 3. Verificación

- [x] 3.1 En una instancia aislada de REAPER, cargar cada estilo con el pad en (0,0) y comprobar que los golpes de p4/p5 coinciden con la fuente
