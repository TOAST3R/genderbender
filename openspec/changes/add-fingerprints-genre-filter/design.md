## Context

`tools/view_styles.py` genera `docs/fingerprints.html` con los datos de todos los estilos en JSON (`DATA.groups`, una entrada por familia en el orden de la tabla del README) y un script que pinta las tiras. La cabecera es fija (`position: sticky`) y ya tiene el slider de Density.

## Goals / Non-Goals

**Goals:**
- Ver de un vistazo cuántos estilos tiene cada familia y cuántos hay en total.
- Filtrar la página por una familia sin recargar.

**Non-Goals:**
- Buscar por nombre, filtrar por BPM o guardar el filtro en la URL.

## Decisions

- **Un `<select>` nativo** en la cabecera, con las opciones generadas en el navegador desde `DATA.groups`: "Todos (N)" y luego `Familia (n)` en el orden de la tabla. Es accesible con teclado sin código extra.
- **Cada familia en un `<section>`** con su `h2` y sus estilos. Filtrar es poner `hidden` a las secciones que no coinciden. Las tiras ya están pintadas, así que no hay que redibujar.
- **Recuento en un `<output>`** junto al selector: `N estilos` o `n de N estilos`.
- Los totales salen de los datos de la página, no se escriben a mano: no pueden desfasarse.

## Risks / Trade-offs

- [Página regenerada] `check_styles.py` compara el HTML con lo que genera `view_styles.py`. → Se regenera la página en el mismo cambio.

## Verificación

No toca el plugin, así que no hace falta REAPER. Se abre `docs/fingerprints.html` en un navegador, se elige una familia y se comprueba que solo se ve esa, que el recuento coincide con el número de tiras y que "Todos" vuelve a mostrar las 80.
