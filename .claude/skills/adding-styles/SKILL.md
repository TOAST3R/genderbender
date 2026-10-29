---
name: adding-styles
description: Use when adding, renaming or deleting a GenderBender style (drum_styles_v/*.txt or styles_src/*.style), or when a style shows up under "Other" on the fingerprints page by mistake.
---

# Añadir estilos

## Principio

Un estilo no está terminado hasta que tiene fila en la tabla "Included styles" del `README.md` y sale en `docs/fingerprints.html`. La página saca las familias de esa tabla: un estilo que no aparece en ella cae en "Other" sin ningún aviso, y `check_styles.py` no lo detecta.

## Pasos

1. Escribir la fuente en `styles_src/<nombre>.style` y generarla con `python3 tools/make_style.py build styles_src/<nombre>.style`. Nunca editar un `.txt` a mano.
2. En la tabla "Included styles" del `README.md`, añadir el estilo a la fila de su familia, o abrir una fila nueva `| Familia | ... |`.
   - Entrada `NOMBRE (bpm)`: vale para los archivos `NOMBRE.txt` y `NOMBRE bpm.txt`.
   - Entrada sin `(bpm)`: el nombre del archivo tal cual, sin `.txt`.
   - Si no tiene familia, ponerlo por su nombre en la fila `Other`.
   - Si se borra o se renombra un estilo, quitar o corregir su entrada.
3. `python3 tools/view_styles.py` para regenerar la página.
4. Cruzar tabla y carpeta. No debe imprimir nada:
   ```bash
   cd tools && python3 -c "
   import glob, os, view_styles as v
   files = {os.path.basename(p)[:-4] for p in glob.glob('../drum_styles_v/*.txt')}
   listed = set()
   for fam, entries in v.families():
       for base, bpm in entries:
           m = {n for n in files if n == base or (bpm and n == f'{base} {bpm}')}
           listed |= m
           if not m: print('en la tabla sin archivo:', fam, '/', base)
   for n in sorted(files - listed): print('sin fila en la tabla:', n)
   "
   ```
5. `python3 tools/check_styles.py` debe imprimir `ok`.

## Errores habituales

| Error | Qué pasa |
|---|---|
| Añadir el `.txt` sin tocar el README | El estilo cae en "Other" y `check_styles.py` sigue diciendo `ok` |
| Tocar el README y no regenerar la página | `check_styles.py` falla: `docs/fingerprints.html desfasado` |
| Dejar en la tabla un estilo que ya no existe | La tabla miente. El paso 4 lo muestra como "en la tabla sin archivo" |
