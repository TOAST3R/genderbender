## 1. Generador

- [x] 1.1 Crear `tools/view_styles.py` con `render()` que lea `drum_styles_v/*.txt` con `from_txt` (orden alfabético) y devuelva el HTML como cadena, y un `main` que lo escriba en `docs/fingerprints.html`
- [x] 1.2 Parsear la tabla "Included styles" del README y asignar familias (nombre exacto o nombre + " bpm"; el resto a "Other")
- [x] 1.3 Plantilla HTML autocontenida: datos JSON incrustados, una tira de 9 canvas por estilo agrupada por familia, marca de FILL vacío, temas claro/oscuro
- [x] 1.4 Slider de Density (0–260, inicial 50) que atenúa los pasos con `256 − v ≥ Density`
- [x] 1.5 Vista ampliada al hacer clic o Enter: 9 patrones grandes, nombres de voz, marca cada 8 pasos; cierre con Escape o clic fuera

## 2. Comprobación

- [x] 2.1 Añadir a `tools/check_styles.py` la comparación de `render()` con `docs/fingerprints.html` (error si falta o está desfasado)
- [x] 2.2 Generar `docs/fingerprints.html` y ejecutar `python3 tools/check_styles.py` (debe imprimir `ok`); añadir un `.txt` de prueba temporal y comprobar que falla

## 3. Verificación de la página

- [x] 3.1 Abrir la página en un navegador: 31 tiras, familias del README, p8 vacío marcado en ZZZZ BLACK, ESTAIL, GQOM y TEST2
- [x] 3.2 Probar el slider en 50 y 260, la vista ampliada (clic, Enter, Escape) y una anchura de móvil sin scroll horizontal

## 4. Documentación

- [x] 4.1 README: `tools/view_styles.py` y `docs/` en la tabla de layout, cómo regenerar la página y el enlace a GitHub Pages
- [x] 4.2 Recordar al usuario activar Pages (Settings → Pages → `main`, `/docs`) y hacer push; no hacer push sin su permiso
