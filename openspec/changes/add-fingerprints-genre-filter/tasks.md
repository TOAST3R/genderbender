## 1. Página

- [x] 1.1 En la plantilla de `tools/view_styles.py`, añadir a la cabecera el selector de familia y el recuento
- [x] 1.2 Agrupar cada familia en un `<section>` y filtrar con `hidden` al cambiar el selector
- [x] 1.3 Regenerar `docs/fingerprints.html` con `python3 tools/view_styles.py`

## 2. Verificación

- [x] 2.1 `python3 tools/check_styles.py` imprime `ok`
- [x] 2.2 Abrir la página en un navegador: "Todos" muestra todos los estilos con el total, una familia muestra solo sus tiras y su recuento, y volver a "Todos" lo restaura
