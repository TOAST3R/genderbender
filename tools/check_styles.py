#!/usr/bin/env python3
"""Comprueba que todos los estilos son validos para el plugin.

  python3 tools/check_styles.py

- Cada drum_styles_v/*.txt se decodifica (7 voces x 9 patrones x 32 pasos, 0-255)
  y se vuelve a escribir igual byte a byte, y su BASE (p4 y p5) tiene notas.
- Cada styles_src/*.style genera exactamente su .txt de drum_styles_v/.
- docs/fingerprints.html coincide con lo que genera tools/view_styles.py.
- La tabla "Included styles" del README y drum_styles_v/ coinciden: cada estilo
  tiene su entrada y cada entrada su estilo (misma regla que la pagina de huellas).
Sale con 1 si algo falla.
"""
import glob
import os
import sys

from make_style import ROOT, StyleError, from_txt, parse_style, to_txt
from view_styles import OUT, families, render


def check():
    errors = []
    for path in sorted(glob.glob(os.path.join(ROOT, 'drum_styles_v', '*.txt'))):
        name = os.path.basename(path)
        text = open(path, encoding='utf-8', newline='').read()
        try:
            data = from_txt(text)
            if to_txt(data) != text:
                errors.append(f'{name}: no se reescribe igual (formato inesperado)')
            # p4/p5 es la BASE: lo que suena en el centro del pad y en el preview
            empty = [f'p{p}' for p in (4, 5) if not any(any(voice[p]) for voice in data)]
            if empty:
                errors.append(f'{name}: BASE vacía ({", ".join(empty)} sin notas)')
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
    errors += table_errors()
    try:
        html = render()
    except StyleError:
        html = None  # el estilo corrupto ya tiene su error arriba
    if html is not None and (not os.path.exists(OUT)
                             or open(OUT, encoding='utf-8', newline='').read() != html):
        errors.append('docs/fingerprints.html desfasado (ejecuta tools/view_styles.py)')
    return errors


def table_errors():
    # misma regla que render(): "NOMBRE (bpm)" vale para NOMBRE.txt y NOMBRE bpm.txt
    names = {os.path.basename(p)[:-4] for p in glob.glob(os.path.join(ROOT, 'drum_styles_v', '*.txt'))}
    listed, errors = set(), []
    for family, entries in families():
        for base, bpm in entries:
            match = {n for n in names if n == base or (bpm and n == f'{base} {bpm}')}
            if not match:
                errors.append(f'README: la entrada "{base}" ({family}) no corresponde a ningun estilo')
            listed |= match
    errors += [f'{n}.txt: no esta en la tabla "Included styles" del README' for n in sorted(names - listed)]
    return errors


if __name__ == '__main__':
    errors = check()
    for e in errors:
        print(e, file=sys.stderr)
    print(f'{len(errors)} errores' if errors else 'ok')
    sys.exit(1 if errors else 0)
