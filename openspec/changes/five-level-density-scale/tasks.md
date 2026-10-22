## 1. Preparación

- [ ] 1.1 Archivar `add-cumbia-styles` para que `style-authoring` exista en `openspec/specs/`
- [ ] 1.2 Guardar los `.txt` actuales de las cinco cumbias para compararlos después

## 2. Herramienta

- [ ] 2.1 Cambiar `SCALE` en `tools/make_style.py` a `X=255 x=204 o=153 -=102 ,=51 .=0` y actualizar el docstring
- [ ] 2.2 Hacer que `to_style` ajuste cada valor con `round(v / 51) * 51` y emita su símbolo, sin `[n]`
- [ ] 2.3 Comprobar los escenarios del spec: la cuadrícula `Xxo-,...`, `[170]`, el ajuste de 255/170/85/128/20, el round-trip de valores en escala y el estilo corrupto

## 3. Migrar las cumbias

- [ ] 3.1 En `styles_src/*.style`, reescribir `x/o/-` como `[170]/[120]/[60]` y actualizar el comentario de escala de la cabecera
- [ ] 3.2 Reconstruir las cinco cumbias y verificar que los `.txt` son idénticos byte a byte a los guardados en 1.2
- [ ] 3.3 Verificar que ningún otro `.txt` de `drum_styles_v/` ha cambiado
