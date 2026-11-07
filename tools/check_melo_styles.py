#!/usr/bin/env python3
"""Comprueba que todos los estilos melodicos son validos para GenderBender Melo.

  python3 tools/check_melo_styles.py

- Cada melo_styles/*.txt se lee entero (MAGIC, rangos, conteos, markov) y se reescribe igual.
- Cada styles_melo_src/*.mstyle compila exactamente a su .txt, y cada .txt tiene su fuente.
- Cada estilo cumple lo minimo de la v1: >= 3 progresiones, tabla markov que cubre el banco,
  >= 1 sustitucion y BASE (p4/p5) con notas en las tres voces.
- melo_index/estilos.txt (la lista que lee el plugin) esta al dia.
- Cada nombre es el de un estilo de bateria (sin el BPM) con el mismo BPM (tabla del README).
Sale con 1 si algo falla.
"""
import glob
import os
import sys

from make_melo_style import INDEX, OUT_DIR, ROOT, VOICES, StyleError, from_txt, index_text, parse_style, to_txt

SRC_DIR = os.path.join(ROOT, 'styles_melo_src')


def drum_bpms():
    """{nombre sin BPM: bpm} de la tabla "Included styles" del README."""
    from view_styles import families
    out = {}
    for _, entries in families():
        for base, bpm in entries:
            if bpm:
                name = base[:-len(str(bpm)) - 1] if base.endswith(f' {bpm}') else base
                out[name] = int(bpm)
    return out


def style_errors(name, s):
    errors = []
    if len(s['progs']) < 3:
        errors.append(f'{name}: {len(s["progs"])} progresiones (minimo 3)')
    bank = {i for p in s['progs'] for i in p}
    if not all(any(s['markov'][i]) for i in bank):
        errors.append(f'{name}: la tabla markov no cubre todos los acordes del banco')
    if not s['subs']:
        errors.append(f'{name}: sin sustituciones')
    for vi, v in enumerate(VOICES):
        for p in (4, 5):
            if not any(s['voices'][vi][p][0]):
                errors.append(f'{name}: BASE vacia ({v} p{p} sin notas)')
    return errors


def check():
    errors = []
    compiled = {}
    for path in sorted(glob.glob(os.path.join(OUT_DIR, '*.txt'))):
        name = os.path.basename(path)[:-4]
        text = open(path, encoding='utf-8', newline='').read()
        try:
            s = from_txt(text)
        except StyleError as e:
            errors.append(f'{name}.txt: {e}')
            continue
        compiled[name] = (text, s)
        errors += style_errors(name, s)
    sources = set()
    for path in sorted(glob.glob(os.path.join(SRC_DIR, '*.mstyle'))):
        src = os.path.basename(path)
        try:
            s = parse_style(open(path, encoding='utf-8').read(), src)
        except StyleError as e:
            errors.append(str(e))
            continue
        sources.add(s['name'])
        if s['name'] not in compiled:
            if not os.path.exists(os.path.join(OUT_DIR, s['name'] + '.txt')):
                errors.append(f'{src}: falta melo_styles/{s["name"]}.txt')
        elif compiled[s['name']][0] != to_txt(s):
            errors.append(f'{src}: desactualizado, no coincide con melo_styles/{s["name"]}.txt '
                          '(vuelve a ejecutar build)')
    errors += [f'{n}.txt: no tiene fuente en styles_melo_src/' for n in sorted(set(compiled) - sources)]
    if not os.path.exists(INDEX) or open(INDEX, encoding='utf-8', newline='').read() != index_text():
        errors.append('melo_index/estilos.txt desfasado (vuelve a ejecutar build)')
    for name in compiled:
        if not all(c.isupper() or c.isdigit() or c in ' -&' for c in name):
            errors.append(f'{name}.txt: usa solo mayusculas, digitos, espacios, - y & '
                          '(el orden del indice debe coincidir con el de REAPER)')
    bpms = drum_bpms()
    for name, (_, s) in sorted(compiled.items()):
        if name not in bpms:
            errors.append(f'{name}.txt: no hay estilo de bateria con ese nombre en el README')
        elif bpms[name] != s['bpm']:
            errors.append(f'{name}.txt: BPM {s["bpm"]}, el de bateria es {bpms[name]}')
    return errors


if __name__ == '__main__':
    errors = check()
    for e in errors:
        print(e, file=sys.stderr)
    print(f'{len(errors)} errores' if errors else 'ok')
    sys.exit(1 if errors else 0)
