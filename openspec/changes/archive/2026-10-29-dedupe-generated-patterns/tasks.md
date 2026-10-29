## 1. Patrones

- [x] 1.1 Con un script de un solo uso, regenerar las 73 fuentes con p6, p7 y p8 vacíos cuando repetirían los de otro estilo generado (se conservan en el primero por orden alfabético)
- [x] 1.2 Regenerar los `.txt` con `python3 tools/make_style.py build`
- [x] 1.3 Comprobar que ningún p6, p7 ni p8 no vacío se repite entre los 73 estilos y que p0–p5 no han cambiado

## 2. ESTAIL

- [x] 2.1 Borrar `drum_styles_v/ESTAIL.txt` y su entrada en la fila "Other" del README

## 3. Documentación y verificación

- [x] 3.1 Seguir la skill `adding-styles`: regenerar `docs/fingerprints.html` y cruzar tabla y carpeta
- [x] 3.2 `python3 tools/check_styles.py` imprime `ok`
