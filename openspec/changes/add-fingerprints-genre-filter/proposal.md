## Why

La página de huellas tiene ya 80 estilos en 17 familias y solo se puede recorrer haciendo scroll. Para ver los estilos de un género hay que buscar su encabezado, y no se ve cuántos estilos hay en cada familia ni en total.

## What Changes

- En la cabecera fija de `docs/fingerprints.html`, un selector de género con una opción por familia de la tabla "Included styles", cada una con su número de estilos, y una opción "Todos".
- Al elegir una familia, la página muestra solo esa familia.
- Junto al selector, el recuento: `N estilos` con "Todos", o `n de N estilos` con una familia.
- Sin cambios en el plugin ni en los estilos. La página sigue siendo un único archivo sin recursos externos.

## Capabilities

### New Capabilities

### Modified Capabilities
- `style-fingerprints`: se añade el filtro por familia con recuentos en la cabecera.

## Impact

- `tools/view_styles.py` (plantilla HTML y script) y `docs/fingerprints.html` regenerado.
