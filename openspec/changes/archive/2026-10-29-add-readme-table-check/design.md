## Context

- `tools/view_styles.py` tiene `families()`, que lee las filas de la tabla bajo `## Included styles` y devuelve `(familia, [(nombre, bpm), …])`. `render()` empareja cada entrada con los `.txt` (igual al nombre, o al nombre seguido de un espacio y el bpm) y lo que no empareja cae en "Other".
- `tools/check_styles.py` ya importa `render` de `view_styles` para comprobar que la página está al día, y devuelve una lista de errores.
- La skill `adding-styles` tiene en su paso 4 un snippet que hace este mismo cruce a mano.

## Goals / Non-Goals

**Goals:**
- Que añadir, renombrar o borrar un estilo sin tocar la tabla rompa `check_styles.py`.

**Non-Goals:**
- Comprobar que el estilo esté en la familia "correcta" (eso es una decisión musical).
- Comprobar el orden de las filas o de los estilos dentro de una fila.
- Tocar el plugin.

## Decisions

- **Reutilizar `families()`** y la misma regla de emparejado de `render()`, para que la comprobación y la página no puedan discrepar. Se importa `families` junto a `render` en `check_styles.py`.
- **Dos errores con nombre**:
  - `<estilo>.txt: no está en la tabla "Included styles" del README`.
  - `README: la entrada "<nombre>" (<familia>) no corresponde a ningún estilo`.
- **Un estilo emparejado por dos entradas** no es error: la página lo pone en la primera, como hoy.
- **La skill `adding-styles`**: el paso 4 (el snippet de cruce) se sustituye por "lo comprueba `check_styles.py`", y se quita el error habitual "Añadir el `.txt` sin tocar el README… `check_styles.py` sigue diciendo `ok`", que deja de ser cierto.

## Risks / Trade-offs

- [Cambio abierto] `add-world-folk-styles` tiene estilos propuestos sin aplicar; al aplicarlo, `check_styles.py` fallará hasta que añada sus filas. → Es el comportamiento buscado; sus tareas ya incluyen la tabla.

## Verificación

No toca el plugin. Se comprueba con `check_styles.py`:
1. Con la tabla actual imprime `ok`.
2. Quitando una entrada de la tabla (en una copia temporal) falla nombrando ese estilo.
3. Añadiendo una entrada inventada falla nombrando la entrada y su familia.
