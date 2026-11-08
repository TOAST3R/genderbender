#!/usr/bin/env python3
"""Genera y decodifica estilos melodicos de GenderBender Melo (melo_styles/*.txt).

  python3 tools/make_melo_style.py build styles_melo_src/cumbia_colombiana.mstyle [salida.txt]
      (sin salida explicita tambien actualiza melo_index/estilos.txt, la lista que lee el plugin)
  python3 tools/make_melo_style.py decode "melo_styles/CUMBIA COLOMBIANA.txt" [salida.mstyle]

Formato .mstyle (# comentario, tambien al final de linea):
  name: CUMBIA COLOMBIANA          nombre del .txt de salida (el de bateria sin BPM)
  bpm: 95
  meter: 4/4                        4/4 -> 32 pasos por compas; 12/8 -> 24 (tresillos)
  key: A                            tonica por defecto
  scale: harmonic_minor             ver melo_theory.SCALES
  chord_bars: 1                     compases por acorde: 0.5, 1 o 2
  cycle: 4                          compases del ciclo de progresion: 2, 4 u 8
  form.bass: A A A A                forma de frase por voz (A, A', B), 4 motivos de 2 compases
  prog: i iv V7 i                   banco de progresiones (la primera es la de por defecto)
  chords: i iv V7                   opcional: orden de la tabla de acordes (decode lo escribe)
  markov: i > iv 3, V7 2            sucesores de un acorde y su peso (1-255)
  sub: V7 > bII7                    sustitucion posible de un acorde (control de tension)

  [p4 p5]                           las lineas siguientes se aplican a esos patrones
  bass.rhy   X... .... X... ....    ritmo: X=255 x=204 o=153 -=102 ,=51 .=0 o [n]
  bass.deg   R... .... 5... ....    altura del bajo: R 3 5 7 8 a(aproximacion)
  bass.art   .... .... ~... ....    articulacion: . corta  ~ ligada  / slide
  chord.voi  t 7 9 s p h            triada, 7a, 9a, sus, power, shell
  mel.cnt    = + - ^                repite, sube, baja, salta a nota del acorde

  Cada carril tiene 16 o 32 caracteres (4/4) o 12 o 24 (12/8); espacios ignorados.
  En altura y articulacion '.' es el valor por defecto (R, triada, =, corta).
  Cada voz necesita su carril .rhy en los 9 patrones; altura y articulacion son opcionales.
"""
import itertools
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from melo_theory import (ART, FORM, NOTES, PITCH_LANE, ROMAN_DEGREE, SCALES,  # noqa: E402
                         SUFFIXES, VOICES, TheoryError, mask_to_list, parse_chord, parse_key,
                         scale_mask)

MAGIC = 7714
VERSION = 1
PATTERNS = 9
SLOTS = 32
LEVELS = {'X': 255, 'x': 204, 'o': 153, '-': 102, ',': 51, '.': 0}
LEVEL_SYM = {v: k for k, v in LEVELS.items()}
METERS = {'4/4': 32, '12/8': 24}
MAX_CHORDS, MAX_PROGS, MAX_PROG_LEN, MAX_SUBS = 16, 8, 16, 16
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
OUT_DIR = os.path.join(ROOT, 'melo_styles')
INDEX = os.path.join(ROOT, 'melo_index', 'estilos.txt')


def index_text():
    """Nombres de melo_styles/ en el orden de la lista del slider de archivo de REAPER (alfabetico).
    El plugin lo usa para pasar del valor del slider al archivo sin depender de strcpy_fromslider."""
    names = sorted(os.path.basename(p)[:-4] for p in os.listdir(OUT_DIR) if p.endswith('.txt'))
    return ''.join(n + '\n' for n in names)


def write_index():
    os.makedirs(os.path.dirname(INDEX), exist_ok=True)
    with open(INDEX, 'w', encoding='utf-8', newline='') as f:
        f.write(index_text())


class StyleError(Exception):
    pass


def err(where, msg):
    return StyleError(f'{where}: {msg}')


def parse_rhy(text, where):
    vals, i = [], 0
    text = text.replace(' ', '').replace('\t', '')
    while i < len(text):
        c = text[i]
        if c == '[':
            end = text.find(']', i)
            if end < 0:
                raise err(where, 'falta "]"')
            try:
                v = int(text[i + 1:end])
            except ValueError:
                raise err(where, f'valor no numerico "{text[i:end + 1]}" en la posicion {len(vals) + 1}')
            if not 0 <= v <= 255:
                raise err(where, f'valor fuera de 0-255 en la posicion {len(vals) + 1}: {v}')
            vals.append(v)
            i = end + 1
        elif c in LEVELS:
            vals.append(LEVELS[c])
            i += 1
        else:
            raise err(where, f'simbolo de ritmo no valido "{c}" en la posicion {len(vals) + 1}')
    return vals


def parse_symbols(text, alphabet, where):
    vals = []
    for c in text.replace(' ', '').replace('\t', ''):
        if c == '.':
            vals.append(0)
        elif c in alphabet:
            vals.append(alphabet[c])
        else:
            raise err(where, f'simbolo no valido "{c}" en la posicion {len(vals) + 1} '
                             f'(validos: . {" ".join(alphabet)})')
    return vals


def expand(vals, steps, where):
    if len(vals) == steps // 2:
        out = [0] * steps
        out[0::2] = vals
    elif len(vals) == steps:
        out = list(vals)
    else:
        raise err(where, f'{len(vals)} pasos (deben ser {steps // 2} o {steps})')
    return out + [0] * (SLOTS - steps)


def parse_style(source, fname='<fuente>'):
    """Devuelve un dict con cabecera, armonia y voces[v][p] = (rhy, pitch, art)."""
    head = {'name': None, 'bpm': None, 'meter': '4/4', 'key': None, 'scale': None,
            'chord_bars': '1', 'cycle': '4'}
    forms = {v: ['A', 'A', 'A', 'A'] for v in VOICES}
    progs, markov, subs, order = [], [], [], []
    lanes = {}           # (voz, carril, patron) -> (texto, donde)
    block = None
    for lineno, raw in enumerate(source.splitlines(), 1):
        where = f'{fname} linea {lineno}'
        line = raw.split('#', 1)[0].strip()
        if not line:
            continue
        if line.startswith('['):
            if not line.endswith(']'):
                raise err(where, 'cabecera de bloque mal cerrada')
            block = []
            for tok in line[1:-1].split():
                if not (tok[:1] == 'p' and tok[1:].isdigit() and int(tok[1:]) < PATTERNS):
                    raise err(where, f'patron desconocido "{tok}" (p0-p8)')
                block.append(int(tok[1:]))
            if not block:
                raise err(where, 'bloque sin patrones')
            continue
        key, sep, val = line.partition(':')
        if sep and ' ' not in key.strip():
            key, val = key.strip(), val.strip()
            if key in head:
                head[key] = val
            elif key.startswith('form.') and key[5:] in VOICES:
                toks = val.split()
                if len(toks) != 4 or any(t not in FORM for t in toks):
                    raise err(where, f'forma "{val}" no valida (4 motivos de A, A\' o B)')
                forms[key[5:]] = toks
            elif key == 'chords':
                order.append((val.split(), where))
            elif key == 'prog':
                progs.append((val.split(), where))
            elif key == 'markov':
                markov.append((val, where))
            elif key == 'sub':
                subs.append((val, where))
            else:
                raise err(where, f'clave desconocida "{key}"')
            continue
        lane, _, grid = line.partition(' ')
        voice, _, kind = lane.partition('.')
        if voice not in VOICES or kind not in ('rhy', 'art', PITCH_LANE.get(voice, ('',))[0]):
            raise err(where, f'carril desconocido "{lane}"')
        if block is None:
            raise err(where, 'carril fuera de un bloque [pN]')
        for p in block:
            lanes[(voice, kind, p)] = (grid, where)

    for k in ('name', 'bpm', 'key', 'scale'):
        if not head[k]:
            raise err(fname, f'falta "{k}:"')
    try:
        bpm = int(head['bpm'])
        key = parse_key(head['key'])
        smask = scale_mask(head['scale'])
    except (ValueError, TheoryError) as e:
        raise err(fname, str(e))
    if head['meter'] not in METERS:
        raise err(fname, f'compas "{head["meter"]}" no valido ({", ".join(METERS)})')
    steps = METERS[head['meter']]
    cb = {'0.5': 1, '1': 2, '2': 4}.get(head['chord_bars'])
    if cb is None:
        raise err(fname, 'chord_bars debe ser 0.5, 1 o 2')
    if head['cycle'] not in ('2', '4', '8'):
        raise err(fname, 'cycle debe ser 2, 4 u 8')
    if not progs:
        raise err(fname, 'falta al menos una linea "prog:"')

    chords, index = [], {}

    def chord(sym, where):
        if sym not in index:
            try:
                rm = parse_chord(sym, head['scale'])
            except TheoryError as e:
                raise err(where, str(e))
            index[sym] = len(chords)
            chords.append((sym, rm))
        return index[sym]

    for toks, where in order:
        for t in toks:
            chord(t, where)
    prog_idx = []
    for toks, where in progs:
        if not 1 <= len(toks) <= MAX_PROG_LEN:
            raise err(where, f'la progresion debe tener de 1 a {MAX_PROG_LEN} acordes')
        prog_idx.append([chord(t, where) for t in toks])
    sub_pairs = []
    for val, where in subs:
        a, sep, b = val.partition('>')
        if not sep or not a.strip() or not b.strip():
            raise err(where, 'formato "sub: ACORDE > SUSTITUTO"')
        sub_pairs.append((chord(a.strip(), where), chord(b.strip(), where)))
    edges = []
    for val, where in markov:
        a, sep, rest = val.partition('>')
        if not sep:
            raise err(where, 'formato "markov: ACORDE > SUCESOR peso, SUCESOR peso"')
        src = chord(a.strip(), where)
        for item in rest.split(','):
            toks = item.split()
            if len(toks) != 2 or not toks[1].isdigit() or not 1 <= int(toks[1]) <= 255:
                raise err(where, f'sucesor "{item.strip()}" no valido (ACORDE peso 1-255)')
            edges.append((src, chord(toks[0], where), int(toks[1])))
    if len(chords) > MAX_CHORDS:
        raise err(fname, f'{len(chords)} acordes distintos (maximo {MAX_CHORDS})')
    if len(prog_idx) > MAX_PROGS:
        raise err(fname, f'{len(prog_idx)} progresiones (maximo {MAX_PROGS})')
    if len(sub_pairs) > MAX_SUBS:
        raise err(fname, f'{len(sub_pairs)} sustituciones (maximo {MAX_SUBS})')
    n = len(chords)
    table = [[0] * n for _ in range(n)]
    for a, b, w in edges:
        table[a][b] = w
    needed = {i for p in prog_idx for i in p} | {b for _, b, _ in edges}
    if edges:
        for i in sorted(needed):
            if not any(table[i]):
                raise err(fname, f'markov: el acorde "{chords[i][0]}" no tiene sucesores')
    tonic = next((i for i, (_, (r, _)) in enumerate(chords) if r == 0), prog_idx[0][0])

    voices = []
    for v in VOICES:
        pats = []
        pkind, alphabet = PITCH_LANE[v]
        for p in range(PATTERNS):
            if (v, 'rhy', p) not in lanes:
                raise err(fname, f'falta {v}.rhy en el patron p{p}')
            grid, where = lanes[(v, 'rhy', p)]
            rhy = expand(parse_rhy(grid, where), steps, where)
            res = [rhy]
            for kind, alpha in ((pkind, alphabet), ('art', ART)):
                if (v, kind, p) in lanes:
                    grid, where = lanes[(v, kind, p)]
                    res.append(expand(parse_symbols(grid, alpha, where), steps, where))
                else:
                    res.append([0] * SLOTS)
            pats.append(tuple(res))
        voices.append(pats)

    return {'name': head['name'], 'bpm': bpm, 'steps': steps, 'key': key, 'scale': head['scale'],
            'smask': smask, 'chord_bars2': cb, 'cycle': int(head['cycle']),
            'forms': [[FORM[t] for t in forms[v]] for v in VOICES],
            'chords': [rm for _, rm in chords], 'tonic': tonic, 'progs': prog_idx,
            'markov': table, 'subs': sub_pairs, 'voices': voices}


def to_txt(s):
    """Compilado: solo numeros separados por comas, una seccion por linea, MAGIC al principio y al final.
    (El modo texto de JSFX separa valores con comas o saltos de linea; un espacio corta la linea.)"""
    def row(vals):
        return ','.join(str(x) for x in vals)
    lines = [row([MAGIC, VERSION]),
             row([s['bpm'], s['steps'], s['key'], s['smask'], s['chord_bars2'], s['cycle'], s['tonic']]),
             row([x for f in s['forms'] for x in f]),
             row([len(s['chords'])] + [x for rm in s['chords'] for x in rm]),
             row([len(s['progs'])] + [x for p in s['progs'] for x in [len(p)] + p]),
             row([w for r in s['markov'] for w in r]),
             row([len(s['subs'])] + [x for ab in s['subs'] for x in ab])]
    for pats in s['voices']:
        for rhy, pitch, art in pats:
            lines.append(row([x for i in range(SLOTS) for x in (rhy[i], pitch[i], art[i])]))
    lines.append(str(MAGIC))
    return '\n'.join(lines) + '\n'


def from_txt(text):
    """Lee y valida un compilado. Lanza StyleError con la seccion que falla."""
    try:
        nums = [int(t) for t in re.split(r'[,\s]+', text.strip())]
    except ValueError:
        raise StyleError('el compilado contiene algo que no es un numero entero')
    pos = 0

    def take(k=1, what='dato'):
        nonlocal pos
        if pos + k > len(nums):
            raise StyleError(f'archivo truncado leyendo {what}')
        out = nums[pos:pos + k]
        pos += k
        return out if k > 1 else out[0]

    def rng(x, lo, hi, what):
        if not lo <= x <= hi:
            raise StyleError(f'{what} fuera de rango: {x} ({lo}-{hi})')
        return x

    if take(what='MAGIC') != MAGIC:
        raise StyleError('falta el MAGIC inicial (no es un estilo melodico)')
    if take(what='version') != VERSION:
        raise StyleError('version de formato desconocida')
    bpm, steps, key, smask, cb, cycle, tonic = take(7, 'cabecera')
    if steps not in METERS.values():
        raise StyleError(f'pasos por compas no validos: {steps}')
    rng(key, 0, 11, 'tonica')
    if not 0 < smask < 4096 or not smask & 1:
        raise StyleError(f'mascara de escala no valida: {smask}')
    if cb not in (1, 2, 4) or cycle not in (2, 4, 8):
        raise StyleError('ritmo armonico o ciclo no validos')
    forms = take(12, 'forma de frase')
    forms = [[rng(x, 0, 2, 'forma') for x in forms[i * 4:i * 4 + 4]] for i in range(3)]
    n = rng(take(what='n acordes'), 1, MAX_CHORDS, 'n acordes')
    chords = []
    for _ in range(n):
        r, m = take(2, 'acorde')
        rng(r, 0, 11, 'raiz')
        if not 0 < m < 4096 or not m & 1:
            raise StyleError(f'mascara de acorde no valida: {m}')
        chords.append((r, m))
    rng(tonic, 0, n - 1, 'acorde de tonica')
    np_ = rng(take(what='n progresiones'), 1, MAX_PROGS, 'n progresiones')
    progs = []
    for _ in range(np_):
        ln = rng(take(what='longitud'), 1, MAX_PROG_LEN, 'longitud de progresion')
        p = take(ln, 'progresion')
        p = [p] if ln == 1 else p
        progs.append([rng(i, 0, n - 1, 'acorde de progresion') for i in p])
    flat = take(n * n, 'tabla markov')
    flat = [flat] if n == 1 else flat
    markov = [[rng(w, 0, 255, 'peso markov') for w in flat[i * n:i * n + n]] for i in range(n)]
    if any(any(r) for r in markov):
        for i in {i for p in progs for i in p}:
            if not any(markov[i]):
                raise StyleError(f'markov: el acorde {i} no tiene sucesores')
    ns = rng(take(what='n sustituciones'), 0, MAX_SUBS, 'n sustituciones')
    subs = []
    for _ in range(ns):
        a, b = take(2, 'sustitucion')
        subs.append((rng(a, 0, n - 1, 'sustitucion'), rng(b, 0, n - 1, 'sustitucion')))
    voices = []
    maxp = [5, 5, 3]
    for vi in range(3):
        pats = []
        for p in range(PATTERNS):
            raw = take(SLOTS * 3, f'voz {VOICES[vi]} p{p}')
            rhy = [rng(x, 0, 255, 'ritmo') for x in raw[0::3]]
            pitch = [rng(x, 0, maxp[vi], 'altura') for x in raw[1::3]]
            art = [rng(x, 0, 2, 'articulacion') for x in raw[2::3]]
            if any(rhy[steps:]):
                raise StyleError(f'voz {VOICES[vi]} p{p}: notas fuera del compas de {steps} pasos')
            pats.append((rhy, pitch, art))
        voices.append(pats)
    if take(what='MAGIC final') != MAGIC:
        raise StyleError('falta el MAGIC final')
    if pos != len(nums):
        raise StyleError('datos sobrantes despues del MAGIC final')
    return {'bpm': bpm, 'steps': steps, 'key': key, 'smask': smask, 'chord_bars2': cb,
            'cycle': cycle, 'tonic': tonic, 'forms': forms, 'chords': chords, 'progs': progs,
            'markov': markov, 'subs': subs, 'voices': voices}


# ---------- decode ----------

def scale_name(mask):
    for name in SCALES:
        if scale_mask(name) == mask:
            return name
    raise StyleError(f'mascara de escala {mask} sin nombre')


def chord_symbol(root, mask, scale):
    """Primer simbolo romano que vuelve a dar (raiz, mascara)."""
    romans = list(ROMAN_DEGREE)
    for q, acc, rom, suf in itertools.product(('', '°', 'ø', '+'), ('', 'b', '#'), romans, SUFFIXES):
        for low in ((True, False) if q in ('°', 'ø') else (False, True)):
            sym = acc + (rom.lower() if low else rom) + q + suf
            try:
                if parse_chord(sym, scale) == (root, mask):
                    return sym
            except TheoryError:
                pass
    raise StyleError(f'acorde raiz {root} intervalos {mask_to_list(mask)} sin simbolo')


def to_style(name, s):
    from melo_theory import BASS_DEG, CHORD_VOI, MEL_CNT
    scale = scale_name(s['smask'])
    syms = [chord_symbol(r, m, scale) for r, m in s['chords']]
    inv_form = {v: k for k, v in FORM.items()}
    meter = {v: k for k, v in METERS.items()}[s['steps']]
    out = [f'name: {name}', '# decodificado con tools/make_melo_style.py decode',
           f'bpm: {s["bpm"]}', f'meter: {meter}', f'key: {NOTES[s["key"]]}', f'scale: {scale}',
           f'chord_bars: {({1: "0.5", 2: "1", 4: "2"})[s["chord_bars2"]]}', f'cycle: {s["cycle"]}']
    for vi, v in enumerate(VOICES):
        out.append(f'form.{v}: ' + ' '.join(inv_form[x] for x in s['forms'][vi]))
    out.append('chords: ' + ' '.join(syms))
    for p in s['progs']:
        out.append('prog: ' + ' '.join(syms[i] for i in p))
    for a, b in s['subs']:
        out.append(f'sub: {syms[a]} > {syms[b]}')
    for i, row in enumerate(s['markov']):
        succ = [f'{syms[j]} {w}' for j, w in enumerate(row) if w]
        if succ:
            out.append(f'markov: {syms[i]} > ' + ', '.join(succ))
    out.append('')
    alph = [{v: k for k, v in a.items()} for a in (BASS_DEG, CHORD_VOI, MEL_CNT)]
    art_sym = {v: k for k, v in ART.items()}
    for p in range(PATTERNS):
        out.append(f'[p{p}]')
        for vi, v in enumerate(VOICES):
            rhy, pitch, art = s['voices'][vi][p]
            kind = PITCH_LANE[v][0]
            # si el ritmo es de 16 pasos y la altura no, se muestran los 32 en todos
            steps = s['steps']
            half = not any(rhy[1:steps:2]) and not any(pitch[1:steps:2]) and not any(art[1:steps:2])
            def fmt(vals, sym, half=half):
                vv = vals[:steps]
                vv = vv[0::2] if half else vv
                cells = [sym(x) for x in vv]
                g = 4 if steps == 32 else 3          # en 12/8, grupos de 3 tiempos
                return ' '.join(''.join(cells[i:i + g]) for i in range(0, len(cells), g))
            out.append(f'{v}.rhy'.ljust(10) + fmt(rhy, lambda x: LEVEL_SYM.get(x, f'[{x}]')))
            if any(pitch):
                out.append(f'{v}.{kind}'.ljust(10) + fmt(pitch, lambda x, a=alph[vi]: '.' if x == 0 else a[x]))
            if any(art):
                out.append(f'{v}.art'.ljust(10) + fmt(art, lambda x: art_sym[x]))
        out.append('')
    return '\n'.join(out)


def main(argv):
    if len(argv) < 2 or argv[0] not in ('build', 'decode'):
        print(__doc__)
        return 2
    cmd, src = argv[0], argv[1]
    try:
        with open(src, encoding='utf-8') as f:
            text = f.read()
        if cmd == 'build':
            s = parse_style(text, os.path.basename(src))
            dst = argv[2] if len(argv) > 2 else os.path.join(OUT_DIR, s['name'] + '.txt')
            os.makedirs(os.path.dirname(os.path.abspath(dst)), exist_ok=True)
            with open(dst, 'w', encoding='utf-8', newline='') as f:
                f.write(to_txt(s))
            if len(argv) <= 2:
                write_index()
            print(f'ok -> {os.path.normpath(dst)}')
        else:
            name = os.path.splitext(os.path.basename(src))[0]
            style = to_style(name, from_txt(text))
            if len(argv) > 2:
                with open(argv[2], 'w', encoding='utf-8') as f:
                    f.write(style)
            else:
                print(style)
    except StyleError as e:
        print(f'error ({src}): {e}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
