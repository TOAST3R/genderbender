## 1. Comprobación

- [x] 1.1 En `tools/check_styles.py`, importar `families` de `view_styles` y comprobar que cada `.txt` tiene entrada en la tabla y cada entrada su `.txt`, con la misma regla de emparejado que `render()`
- [x] 1.2 Actualizar el docstring de `check_styles.py` con la comprobación nueva

## 2. Skill

- [x] 2.1 En `.claude/skills/adding-styles/SKILL.md`, sustituir el snippet de cruce del paso 4 por "lo comprueba `check_styles.py`" y quitar el error habitual que decía que `check_styles.py` no lo detectaba

## 3. Verificación

- [x] 3.1 `python3 tools/check_styles.py` imprime `ok` con la tabla actual
- [x] 3.2 Con una copia temporal del README sin una entrada, la comprobación falla nombrando el estilo
- [x] 3.3 Con una copia temporal del README con una entrada inventada, falla nombrando la entrada y su familia
