#!/usr/bin/env python3
"""Comprueba que todos los estilos son validos para el plugin.

  python3 tools/check_styles.py

- Cada drum_styles_v/*.txt se decodifica (7 voces x 9 patrones x 32 pasos, 0-255)
  y se vuelve a escribir igual byte a byte.
- Cada styles_src/*.style genera exactamente su .txt de drum_styles_v/.
Sale con 1 si algo falla.
"""
import glob
import os
import sys

from make_style import ROOT, StyleError, from_txt, parse_style, to_txt


def check():
    errors = []
    for path in sorted(glob.glob(os.path.join(ROOT, 'drum_styles_v', '*.txt'))):
        name = os.path.basename(path)
        text = open(path, encoding='utf-8', newline='').read()
        try:
            if to_txt(from_txt(text)) != text:
                errors.append(f'{name}: no se reescribe igual (formato inesperado)')
        except StyleError as e:
            errors.append(f'{name}: {e}')
    for path in sorted(glob.glob(os.path.join(ROOT, 'styles_src', '*.style'))):
        src = os.path.basename(path)
        try:
            name, data = parse_style(open(path, encoding='utf-8').read())
        except StyleError as e:
            errors.append(f'{src}: {e}')
            continue
        txt = os.path.join(ROOT, 'drum_styles_v', f'{name}.txt')
        if not os.path.exists(txt):
            errors.append(f'{src}: falta drum_styles_v/{name}.txt')
        elif open(txt, encoding='utf-8', newline='').read() != to_txt(data):
            errors.append(f'{src}: no coincide con drum_styles_v/{name}.txt (vuelve a ejecutar build)')
    return errors


if __name__ == '__main__':
    errors = check()
    for e in errors:
        print(e, file=sys.stderr)
    print(f'{len(errors)} errores' if errors else 'ok')
    sys.exit(1 if errors else 0)
