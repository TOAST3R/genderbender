---
name: adding-styles
description: Use when adding, renaming or deleting a GenderBender style (drum_styles_v/*.txt or styles_src/*.style), or when a style shows up under "Other" on the fingerprints page by mistake.
---

# Añadir estilos

## Principio

Un estilo no está terminado hasta que tiene fila en la tabla "Included styles" del `README.md` y sale en `docs/fingerprints.html`. La página saca las familias de esa tabla: un estilo que no aparece en ella cae en "Other". `check_styles.py` falla si la tabla y la carpeta no coinciden.

## Pasos

1. Escribir la fuente en `styles_src/<nombre>.style` y generarla con `python3 tools/make_style.py build styles_src/<nombre>.style`. Nunca editar un `.txt` a mano.
2. En la tabla "Included styles" del `README.md`, añadir el estilo a la fila de su familia, o abrir una fila nueva `| Familia | ... |`.
   - Entrada `NOMBRE (bpm)`: vale para los archivos `NOMBRE.txt` y `NOMBRE bpm.txt`.
   - Entrada sin `(bpm)`: el nombre del archivo tal cual, sin `.txt`.
   - Si no tiene familia, ponerlo por su nombre en la fila `Other`.
   - Si se borra o se renombra un estilo, quitar o corregir su entrada.
3. `python3 tools/view_styles.py` para regenerar la página.
4. `python3 tools/check_styles.py` debe imprimir `ok`. Falla si un estilo no tiene entrada en la tabla, si una entrada no tiene estilo, si la BASE (p4/p5) está vacía o si la página está desfasada.

## Errores habituales

| Error | Qué pasa |
|---|---|
| Añadir el `.txt` sin tocar el README | `check_styles.py` falla: "no esta en la tabla" |
| Tocar el README y no regenerar la página | `check_styles.py` falla: `docs/fingerprints.html desfasado` |
| Dejar en la tabla un estilo que ya no existe | `check_styles.py` falla: "no corresponde a ningun estilo" |
