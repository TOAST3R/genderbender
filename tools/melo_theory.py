"""Teoria musical comun a make_melo_style.py y check_melo_styles.py.

Escalas como mascara de 12 bits (bit n = n semitonos sobre la tonica),
numeros romanos -> (raiz en semitonos, mascara de intervalos del acorde)
y los alfabetos de altura y articulacion de cada voz.
"""

NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
FLATS = {'DB': 1, 'EB': 3, 'GB': 6, 'AB': 8, 'BB': 10}

SCALES = {
    'major':              [0, 2, 4, 5, 7, 9, 11],
    'minor':              [0, 2, 3, 5, 7, 8, 10],
    'harmonic_minor':     [0, 2, 3, 5, 7, 8, 11],
    'dorian':             [0, 2, 3, 5, 7, 9, 10],
    'phrygian':           [0, 1, 3, 5, 7, 8, 10],
    'phrygian_dominant':  [0, 1, 4, 5, 7, 8, 10],
    'mixolydian':         [0, 2, 4, 5, 7, 9, 10],
    'major_pentatonic':   [0, 2, 4, 7, 9],
    'minor_pentatonic':   [0, 3, 5, 7, 10],
}
MAJOR = SCALES['major']
ROMANS = ['VII', 'III', 'VI', 'IV', 'II', 'V', 'I']  # los largos primero para el prefijo
ROMAN_DEGREE = {'I': 0, 'II': 1, 'III': 2, 'IV': 3, 'V': 4, 'VI': 5, 'VII': 6}

# sufijo -> (intervalos a anadir, intervalos a quitar); el triada base sale de la mayuscula
SUFFIXES = {
    '':     ((), ()),
    '7':    (('7',), ()),        # 7 de dominante en mayuscula, menor en minuscula
    'maj7': ((11,), ()),
    '9':    (('7', 2), ()),
    'm9':   ((10, 2), ()),
    'maj9': ((11, 2), ()),
    '6':    ((9,), ()),
    'add9': ((2,), ()),
    'sus2': ((2,), ('third',)),
    'sus4': ((5,), ('third',)),
}

# alfabetos de altura (simbolo -> codigo del compilado); '.' = el primero (valor por defecto)
BASS_DEG = {'R': 0, '3': 1, '5': 2, '7': 3, '8': 4, 'a': 5}
CHORD_VOI = {'t': 0, '7': 1, '9': 2, 's': 3, 'p': 4, 'h': 5}   # triada, 7a, 9a, sus, power, shell
MEL_CNT = {'=': 0, '+': 1, '-': 2, '^': 3}
ART = {'.': 0, '~': 1, '/': 2}                                 # corta, ligada, slide
VOICES = ['bass', 'chord', 'mel']
PITCH_LANE = {'bass': ('deg', BASS_DEG), 'chord': ('voi', CHORD_VOI), 'mel': ('cnt', MEL_CNT)}
FORM = {'A': 0, "A'": 1, 'B': 2}


class TheoryError(Exception):
    pass


def scale_mask(name):
    if name not in SCALES:
        raise TheoryError(f'escala desconocida "{name}" (validas: {", ".join(SCALES)})')
    return sum(1 << s for s in SCALES[name])


def mask_to_list(mask):
    return [i for i in range(12) if mask >> i & 1]


def parse_key(text):
    t = text.strip().upper()
    if t in NOTES:
        return NOTES.index(t)
    if t in FLATS:
        return FLATS[t]
    raise TheoryError(f'tonica desconocida "{text}"')


def parse_chord(symbol, scale):
    """'bII7' -> (raiz, mascara). Sin alteracion el numero es grado de la escala del estilo;
    con b/# es el grado de la escala mayor alterado. Mayuscula = mayor, minuscula = menor."""
    s = symbol
    acc = 0
    while s[:1] in ('b', '#'):
        acc += -1 if s[0] == 'b' else 1
        s = s[1:]
    up = s.upper()
    roman = next((r for r in ROMANS if up.startswith(r)), None)
    if roman is None:
        raise TheoryError(f'acorde desconocido "{symbol}"')
    head, rest = s[:len(roman)], s[len(roman):]
    if head not in (roman, roman.lower()):
        raise TheoryError(f'acorde desconocido "{symbol}" (mezcla de mayusculas y minusculas)')
    major = head == roman
    deg = ROMAN_DEGREE[roman]
    steps = SCALES[scale] if scale in SCALES else None
    if steps is None:
        raise TheoryError(f'escala desconocida "{scale}"')
    if acc:
        root = (MAJOR[deg] + acc) % 12
    else:
        if deg >= len(steps):
            raise TheoryError(f'acorde "{symbol}": la escala {scale} solo tiene {len(steps)} grados')
        root = steps[deg]
    quality = None
    if rest[:1] in ('°', '+') or rest[:1] == 'ø':
        quality, rest = rest[0], rest[1:]
    if rest not in SUFFIXES:
        raise TheoryError(f'acorde "{symbol}": sufijo desconocido "{rest}"')
    if quality == '°':
        ints = {0, 3, 6}
    elif quality == 'ø':
        ints = {0, 3, 6, 10}
    elif quality == '+':
        ints = {0, 4, 8}
    else:
        ints = {0, 4, 7} if major else {0, 3, 7}
    add, remove = SUFFIXES[rest]
    if 'third' in remove:
        ints -= {3, 4}
    for a in add:
        if a == '7':
            ints.add(10 if quality != '°' else 9)
        else:
            ints.add(a)
    return root, sum(1 << i for i in ints)


def chord_name(root, mask, key=0):
    """Nombre legible para depurar: raiz absoluta + intervalos."""
    return f'{NOTES[(root + key) % 12]}{{{",".join(str(i) for i in mask_to_list(mask))}}}'
