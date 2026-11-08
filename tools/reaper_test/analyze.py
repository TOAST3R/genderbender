#!/usr/bin/env python3
"""Analiza un escenario del banco de pruebas de REAPER e imprime PASS / FAIL / SKIP por comprobacion.

Lee out/<escenario>.log (comprobaciones hechas en Lua) y las tomas out/<toma>.txt (MIDI capturado por el logger),
y anade las comprobaciones de notas. Las expectativas salen de los estilos compilados (melo_styles/).
Termina con codigo 1 si hay algun FAIL.

Uso: python3 tools/reaper_test/analyze.py [--out DIR] escenario [escenario ...]
     (por defecto DIR = Scripts/GenderBenderTest/out de REAPER, o $REAPER_DIR/Scripts/GenderBenderTest/out)
"""
import os
import sys
from collections import Counter, defaultdict
from itertools import permutations

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(REPO, 'tools'))
from make_melo_style import from_txt  # noqa: E402

NN = 'C C# D Eb E F F# G Ab A Bb B'.split()
EPS = 1e-3


def nn(p):
    return f'{NN[p % 12]}{p // 12 - 1}'


# ---------- resultados ----------
class Results:
    def __init__(self):
        self.n = Counter()

    def add(self, tag, name, detail=''):
        self.n[tag] += 1
        print(f'{tag} {name}' + (f'  [{detail}]' if detail else ''))

    def check(self, name, ok, detail=''):
        self.add('PASS' if ok else 'FAIL', name, detail)


R = Results()


# ---------- estilos ----------
def style_names():
    with open(os.path.join(REPO, 'melo_index', 'estilos.txt')) as f:
        return [l.strip() for l in f if l.strip()]


_styles = {}


def style(name):
    if name not in _styles:
        with open(os.path.join(REPO, 'melo_styles', name + '.txt')) as f:
            _styles[name] = from_txt(f.read())
    return _styles[name]


def third(m):
    return 4 if m >> 4 & 1 else 3 if m >> 3 & 1 else 5 if m >> 5 & 1 else 2 if m >> 2 & 1 else 4


def fifth(m):
    return 7 if m >> 7 & 1 else 6 if m >> 6 & 1 else 8 if m >> 8 & 1 else 7


def scale_pcs(s, key=None):
    k = s['key'] if key is None else key
    return {(k + i) % 12 for i in range(12) if s['smask'] >> i & 1}


def chord_at(s, prog, slot, key=None):
    """(raiz absoluta, mascara) del acorde del hueco slot en la progresion prog"""
    r, m = s['chords'][s['progs'][prog][slot % len(s['progs'][prog])]]
    return ((s['key'] if key is None else key) + r) % 12, m


def triad(root, m):
    return {root % 12, (root + third(m)) % 12, (root + fifth(m)) % 12}


# ---------- tomas ----------
class Take:
    """eventos en orden de emision: (beat, tipo 1 on / 0 off / 2 cc, logger id, bus, canal, d1, d2)"""

    def __init__(self, out, name):
        self.name = name
        self.ev = []
        path = os.path.join(out, name + '.txt')
        self.ok = os.path.exists(path)
        if self.ok:
            for l in open(path):
                b, ty, ch, d1, d2, bus = l.split()
                lid, bus = divmod(int(float(bus)), 100)
                self.ev.append((float(b), int(ty), lid, bus, int(ch), int(d1), int(d2)))

    def notes(self, lid=0):
        """notas (inicio, fin, bus, canal, altura, vel) emparejadas en orden de emision, y las que quedan abiertas"""
        open_ = defaultdict(list)
        out = []
        for b, ty, l, bus, ch, d1, d2 in self.ev:
            if l != lid or ty == 2:
                continue
            k = (bus, ch, d1)
            if ty == 1:
                open_[k].append((b, d2))
            elif open_[k]:
                b0, v = open_[k].pop(0)
                out.append((b0, b, bus, ch, d1, v))
        hung = {k: len(v) for k, v in open_.items() if v}
        return sorted(out), hung

    def voice(self, ch, lid=0, lo=-1e9, hi=1e9):
        return [n for n in self.notes(lid)[0] if n[3] == ch and lo <= n[0] < hi]

    def first_hit(self, ch, lo, hi):
        """alturas del primer golpe de la voz en [lo, hi)"""
        ns = self.voice(ch, lo=lo, hi=hi)
        if not ns:
            return []
        t = ns[0][0]
        return [n[4] for n in ns if abs(n[0] - t) < 0.05]


TAKES = {}


def take(out, name):
    if name not in TAKES:
        TAKES[name] = Take(out, name)
        if not TAKES[name].ok:
            R.check(f'{name}: la toma existe', False, 'falta ' + name + '.txt')
    return TAKES[name]


def same_notes(a, b, ch=None, hi=1e9):
    f = lambda t: sorted((round(n[0], 3), n[3], n[4]) for n in t.notes()[0] if (ch is None or n[3] == ch) and n[0] < hi)
    return f(a) == f(b), len(f(a)), len(f(b))


def roots_ok(t, s, slots, slotq, ch=2, name=''):
    """slots: lista de (raiz, mascara) esperados; comprueba la triada del primer golpe de cada hueco"""
    bad = []
    for i, (r, m) in enumerate(slots):
        hit = {p % 12 for p in t.first_hit(ch, i * slotq, (i + 1) * slotq)}
        if not hit or not triad(r, m) <= hit:
            bad.append(f'hueco {i + 1}: esperado {NN[r]} y tiene {sorted(NN[p] for p in hit) or "-"}')
    R.check(f'{t.name}: {name}', not bad, '; '.join(bad[:3]) if bad else f'{len(slots)} acordes')


# ---------- escenarios ----------
def no_hung(t):
    hung = t.notes()[1]
    R.check(f'{t.name}: sin notas colgadas', not hung, str(hung) if hung else f'{len(t.notes()[0])} notas cerradas')


def harmony(out):
    BUL, CUM = style('BULERIA'), style('CUMBIA COLOMBIANA')
    sq = BUL['chord_bars2'] * 2
    t = take(out, 'h_fixed')
    roots_ok(t, BUL, [chord_at(BUL, 0, i) for i in range(16 // sq)], sq, name='modo fija = progresion 1')
    t = take(out, 'h_cycle')
    per = BUL['cycle'] * 4 // sq
    roots_ok(t, BUL, [chord_at(BUL, (i // per) % len(BUL['progs']), i) for i in range(48 // sq)], sq,
             name='modo ciclo = progresiones 1, 2, 3')
    t = take(out, 'h_half')
    roots_ok(t, BUL, [chord_at(BUL, 0, i) for i in range(4)], 2, name='acorde de 1/2 compas')
    ok, a, b = same_notes(take(out, 'h_sub0'), take(out, 'h_fixed'))
    R.check('h_sub0: tension 0 suena igual que fija', ok, f'{a} vs {b} notas')
    t = take(out, 'h_sub100')
    subs = defaultdict(list)
    for x, y in BUL['subs']:
        subs[x].append(y)
    bad = []
    for i in range(16 // sq):
        ci = BUL['progs'][0][i % len(BUL['progs'][0])]
        cands = [BUL['chords'][j] for j in subs.get(ci, [ci])]
        hit = {p % 12 for p in t.first_hit(2, i * sq, (i + 1) * sq)}
        if not any(triad(BUL['key'] + r, m) <= hit for r, m in cands):
            bad.append(f'hueco {i + 1}')
    differs = not same_notes(t, take(out, 'h_fixed'))[0]
    R.check('h_sub100: tension 100 sustituye y cambia la toma', not bad and differs,
            ('sin sustituir: ' + ', '.join(bad)) if bad else 'distinta de fija')
    t = take(out, 'h_markov')
    tr, tm = BUL['chords'][BUL['tonic']]
    per = BUL['cycle'] * 4 // sq
    bad = []
    for c in range(48 // (per * sq)):
        for i in (c * per, c * per + per - 1):
            hit = {p % 12 for p in t.first_hit(2, i * sq, (i + 1) * sq)}
            if not triad(BUL['key'] + tr, tm) <= hit:
                bad.append(f'ciclo {c + 1} hueco {i - c * per + 1}')
    R.check('h_markov: cada ciclo empieza y termina en la tonica', not bad, ', '.join(bad))
    t = take(out, 'h_mod')

    def cycle_key(c):
        """tonica del ciclo c (2 compases, 2 acordes de la progresion 1): la que hace que las triadas
        esperadas esten en el primer golpe de cada acorde. La nota grave no sirve: depende de la inversion."""
        hits = [{p % 12 for p in t.first_hit(2, (c * 2 + s) * 4, (c * 2 + s) * 4 + 4)} for s in range(2)]
        ks = [k for k in range(12) if all(h and triad(*chord_at(BUL, 0, s, key=k)) <= h for s, h in enumerate(hits))]
        return ks[0] if len(ks) == 1 else None
    keys = [cycle_key(c) for c in range(5)]
    R.check('h_mod: modula al empezar los ciclos 3 y 5 (ciclos de 2 compases)',
            None not in keys and keys[0] == keys[1] and keys[2] != keys[1] and keys[2] == keys[3] and keys[4] != keys[3],
            'tonicas de los ciclos 1-5: ' + ' '.join(NN[k] if k is not None else '-' for k in keys))
    a, b = take(out, 'h_cumbia'), take(out, 'h_cumbia_C')
    bass_a, bass_b = a.voice(1, hi=16), b.voice(1, hi=16)
    R.check('h_cumbia_C: el bajo sube 3 semitonos en los mismos pasos',
            len(bass_a) == len(bass_b) > 0 and all(abs(x[0] - y[0]) < EPS and y[4] - x[4] == 3 for x, y in zip(bass_a, bass_b)),
            f'{len(bass_a)} notas')
    roots_ok(b, CUM, [chord_at(CUM, 0, i, key=0) for i in range(4)], CUM['chord_bars2'] * 2,
             name='acordes equivalentes sobre C')
    sc = scale_pcs(CUM, key=0)
    out_ = [nn(n[4]) for n in b.notes()[0] if n[4] % 12 not in sc | {(chord_at(CUM, 0, int(n[0] // 4), key=0)[0] + i) % 12 for i in range(12) if chord_at(CUM, 0, int(n[0] // 4), key=0)[1] >> i & 1}]
    R.check('h_cumbia_C: todas las notas en la escala o el acorde de C', not out_, ', '.join(out_[:5]))
    t = take(out, 'h_master')
    roots_ok(t, BUL, [chord_at(BUL, 0, i) for i in range(4)] + [chord_at(CUM, 0, i) for i in range(4)], 4,
             name='la maestra cambia en el ciclo siguiente (BULERIA -> CUMBIA)')
    t = take(out, 'h_prog')
    roots_ok(t, BUL, [chord_at(BUL, 0, i) for i in range(4)] + [chord_at(BUL, 1, i) for i in range(4)], 4,
             name='la progresion cambia en el ciclo siguiente')
    names = style_names()
    for m in range(len(names)):
        t = take(out, f'h_master{m}')
        s = style(names[m])
        sc = scale_pcs(s)
        ns = t.notes()[0]
        chords = defaultdict(set)
        for n in ns:
            if n[3] == 2:
                chords[int(n[0] // 4)].add(n[4] % 12)
        bad = [nn(n[4]) for n in ns if n[4] % 12 not in sc | chords[int(n[0] // 4)]]
        R.check(f'h_master{m}: maestro {names[m]}, todas las notas en su escala o el acorde', ns and not bad,
                f'{len(ns)} notas' + (', fuera: ' + ', '.join(bad[:5]) if bad else ''))


def base_steps(s, voice, pat, bar_steps):
    return [i for i in range(bar_steps) if s['voices'][voice][pat][0][i] == 255]


def steps_of(notes, bar, steps):
    return sorted({round((n[0] - bar * 4) * steps / 4) for n in notes})


def voices(out):
    ACID, CUM, SON, BUL = style('ACID HOUSE'), style('CUMBIA COLOMBIANA'), style('SON'), style('BULERIA')
    t = take(out, 'v_acid')
    got, want = steps_of(t.voice(1, hi=4), 0, 32), base_steps(ACID, 0, 4, 32)
    R.check('v_acid: el bajo toca su BASE (p4, pasos a 255)', got == want, f'{got} vs {want}')
    bad = []
    for n0 in sorted({round(n[0], 2) for n in t.voice(2)}):
        grp = sorted(n[0] for n in t.voice(2) if abs(n[0] - n0) < 0.1)
        if len(grp) > 1:
            gaps = [round((grp[i + 1] - grp[i]) * 500, 2) for i in range(len(grp) - 1)]
            if any(abs(g - 20 / (len(grp) - 1)) > 0.2 for g in gaps):
                bad.append(f'{n0}: {gaps} ms')
    R.check('v_acid: strum de 20 ms repartido entre las notas del acorde', not bad and t.voice(2), '; '.join(bad[:3]))
    p = take(out, 'v_pad0')
    ok = [(round(n[0], 3), n[4]) for n in p.voice(1, hi=16)] == [(round(n[0], 3), n[4]) for n in t.voice(1, hi=16)]
    R.check('v_pad0: con peso de pad 0 el bajo no cambia', ok)
    got, want = steps_of(p.voice(2, hi=4), 0, 32), base_steps(ACID, 1, 6, 32)
    R.check('v_pad0: los acordes tocan la esquina (p6)', got == want, f'{got} vs {want}')
    c = take(out, 'v_cumbia')
    r, m = chord_at(CUM, 0, 1)
    pcs = {n[4] % 12 for n in c.voice(1, lo=4, hi=8)}
    R.check(f'v_cumbia: el bajo sobre {NN[r]}m toca su fundamental y su quinta', pcs == {r, (r + 7) % 12},
            f'{sorted(NN[x] for x in pcs)}')
    a, b = sorted(c.first_hit(2, 0, 4)), sorted(c.first_hit(2, 4, 8))
    tpcs = sorted({x % 12 for x in b})

    def dist(x, pc):
        """distancia de la nota x a la nota mas cercana de clase pc"""
        d = (pc - x) % 12
        return min(d, 12 - d)
    # minimo sobre todos los repartos de las notas del acorde nuevo entre las voces del anterior
    best = min(sum(dist(x, pc) for x, pc in zip(a, perm))
               for perm in permutations(tpcs)) if len(a) == len(b) == len(tpcs) else None
    moved = sum(abs(x - y) for x, y in zip(a, b)) if len(a) == len(b) else None
    R.check('v_cumbia: voice leading de menor movimiento entre los dos primeros acordes',
            moved is not None and best is not None and moved <= best,
            f'{[nn(x) for x in a]} -> {[nn(x) for x in b]}: {moved} semitonos (minimo {best})')
    s0, s1 = take(out, 'v_son'), take(out, 'v_son_swing')
    R.check('v_son: el tumbao no toca en el tiempo 1', all(round((n[0] % 4) * 8) != 0 for n in s0.voice(1, hi=8)))
    a = sorted((n[0], n[3], n[4]) for n in s0.notes()[0] if n[0] < 8)
    b = sorted((n[0], n[3], n[4]) for n in s1.notes()[0] if n[0] < 8)
    shift = 0.5 * 66 / 100 - 0.25
    bad = [x for x, y in zip(a, b) if abs((y[0] - x[0]) - (shift if abs(x[0] % 0.5 - 0.25) < EPS else 0)) > EPS]
    R.check('v_son_swing: swing 66 mueve solo las semicorcheas a contratiempo', len(a) == len(b) and not bad,
            f'{len(a)} notas' + (f', mal: {len(bad)}' if bad else ''))
    t = take(out, 'v_buleria')
    off = [n[0] for n in t.notes()[0] if abs(n[0] * 6 - round(n[0] * 6)) > EPS]
    R.check('v_buleria: todas las notas en la rejilla de tresillos (24 pasos)', not off, str(off[:3]))
    bad = []
    for n in t.voice(3):
        if abs(n[0] % 2) < EPS:
            ch = {x[4] % 12 for x in t.voice(2, lo=int(n[0] // 4) * 4, hi=int(n[0] // 4) * 4 + 4)}
            if ch and n[4] % 12 not in ch:
                bad.append(f'{n[0]:.2f}:{nn(n[4])}')
    R.check('v_buleria: la melodia en los tiempos fuertes es nota del acorde', not bad, ', '.join(bad[:5]))
    last = max(t.voice(3, lo=24, hi=32), key=lambda n: n[0], default=None)
    if last:
        ch = {x[4] % 12 for x in t.voice(2, lo=int(last[0] // 4) * 4, hi=int(last[0] // 4) * 4 + 4)}
        R.check('v_buleria: la frase B termina en nota del acorde', last[4] % 12 in ch, f'{nn(last[4])}')


def output(out):
    for name in ('o_slide', 'o_chan', 'o_bus', 'o_split', 'o_seek', 'o_loop', 'o_dest'):
        no_hung(take(out, name))
    t = take(out, 'o_slide')
    ev = [e for e in t.ev if e[2] == 0 and e[4] == 1]
    on_cc, bad = 0, []
    for i, e in enumerate(ev):
        if e[1] == 2 and e[5] == 65 and e[6] == 127:
            on_cc += 1
            # entre el CC y el NoteOn de la nota con slide puede ir el NoteOff de la nota anterior (prioridad de NoteOff)
            j = i + 1
            while j < len(ev) and ev[j][1] == 0:
                j += 1
            if j >= len(ev) or ev[j][1] != 1 or ev[j][0] - e[0] > 0.01:
                bad.append(f'{e[0]:.3f}: CC 127 sin NoteOn justo detras')
        if e[1] == 2 and e[5] == 65 and e[6] == 0 and i >= 2 and e[0] > 0.01:
            # a la misma altura el NoteOff va primero: si no, cerraria la nota nueva
            legato = ev[i - 1][1] == 0 and ev[i - 2][1] == 1
            same = ev[i - 1][1] == 1 and ev[i - 2][1] == 0 and ev[i - 1][5] == ev[i - 2][5]
            if not (legato or same):
                bad.append(f'{e[0]:.3f}: CC 0 no va tras NoteOn siguiente + NoteOff ligado')
    R.check('o_slide: CC65 127 -> NoteOn -> NoteOn siguiente -> NoteOff -> CC65 0', on_cc >= 2 and not bad,
            f'{on_cc} slides' + ('; ' + '; '.join(bad[:3]) if bad else ''))
    for name, key in (('o_chan', 'canal'), ('o_bus', 'bus')):
        t = take(out, name)
        src = Counter((e[4] if key == 'canal' else e[3] + 1) for e in t.ev if e[2] == 0 and e[1] == 1)
        bad = []
        for r in (1, 2, 3):
            got = [(e[4] if key == 'canal' else e[3] + 1) for e in t.ev if e[2] == r and e[1] == 1]
            if set(got) != {r} or len(got) != src[r]:
                bad.append(f'receptora {r}: {dict(Counter(got))} (origen {src[r]})')
        R.check(f'{name}: cada receptora recibe solo su {key}', not bad, '; '.join(bad) or str(dict(src)))
    t = take(out, 'o_split')
    chords = defaultdict(list)
    for n in t.notes()[0]:
        if 1 <= n[2] <= 6:
            chords[round(n[0], 2)].append(n[2])
    bad = [f'{k}: {sorted(v)}' for k, v in chords.items() if sorted(v) != list(range(1, len(v) + 1))]
    voices_ = Counter(n[2] for n in t.notes()[0])
    R.check('o_split: cada nota del acorde en su bus (2, 3, 4...) y bajo y melodia en el suyo',
            chords and not bad and voices_[0] > 0 and voices_[7] > 0, '; '.join(bad[:3]) or str(dict(voices_)))
    t = take(out, 'o_seek')
    ons = [e[0] for e in t.ev if e[2] == 0 and e[1] == 1]
    jump = any(ons[i] < 9 and ons[i + 1] >= 18 for i in range(len(ons) - 1))
    R.check('o_seek: el salto se ve en la toma (de antes del beat 9 a despues del 18)', jump)
    t = take(out, 'o_loop')
    laps, cur, last = [], [], -1
    for e in t.ev:
        if e[2] == 0 and e[1] == 1:
            if e[0] < last - 0.5:
                laps.append(cur)
                cur = []
            cur.append((round(e[0], 3), e[4], e[5]))
            last = e[0]
    laps.append(cur)
    full = laps[:-1]
    dup = [l for l in full if len(set(l)) != len(l)]
    R.check('o_loop: vueltas iguales y sin golpes dobles en la vuelta',
            len(full) >= 2 and all(sorted(l) == sorted(full[0]) for l in full) and not dup,
            f'{len(full)} vueltas completas de {len(full[0]) if full else 0} NoteOn')
    t = take(out, 'o_dest')
    ch1 = [n[0] for n in t.voice(1)]
    ch5 = [n[0] for n in t.voice(5)]
    R.check('o_dest: el bajo pasa del canal 1 al 5 a mitad', ch5 and (not ch1 or max(ch1) < min(ch5)),
            f'canal 1 hasta {max(ch1) if ch1 else "-"}, canal 5 desde {min(ch5) if ch5 else "-"}')


def persistence(out):
    ok, a, b = same_notes(take(out, 'p_seed7a'), take(out, 'p_seed7b'))
    R.check('p_seed: misma semilla, mismo MIDI', ok, f'{a} vs {b}')
    R.check('p_seed: otra semilla, otro MIDI', not same_notes(take(out, 'p_seed7a'), take(out, 'p_seed8'))[0])
    ok, a, b = same_notes(take(out, 'p_seed7a'), take(out, 'p_reload'))
    R.check('p_reload: tras quitar y poner el plugin, el mismo MIDI', ok, f'{a} vs {b}')
    ok, a, b = same_notes(take(out, 'p_fixed'), take(out, 'p_lock_reopen'), ch=1, hi=16)
    R.check('p_lock_reopen: el bajo bloqueado sigue en su BASE tras reabrir', ok, f'{a} vs {b}')
    ok, a, b = same_notes(take(out, 'p_dice'), take(out, 'p_dice_reopen'))
    R.check('p_dice_reopen: misma toma antes y despues de reabrir', ok, f'{a} vs {b}')


def gui(out):
    """el resto de comprobaciones son de Lua; aqui, el indicador muestreado durante g_ind (progresion 1 -> 2 en el beat 6)"""
    no_hung(take(out, 'g_ind'))
    path = os.path.join(out, 'g_ind.csv')
    if not os.path.exists(path):
        R.check('g_ind: muestras del indicador', False, 'falta g_ind.csv')
        return
    BUL = style('BULERIA')
    sq, cyc = BUL['chord_bars2'] * 2, BUL['cycle'] * 4
    rows = [list(map(float, l.split())) for l in open(path) if l.strip()]
    # Un JSFX solo conoce la posicion del bloque que procesa (tambien en @gfx), que va por delante de lo que
    # se oye: procesado anticipado de REAPER + latencia de salida. Se acepta un adelanto de hasta LEAD beats
    # (400 ms a 120 BPM) y se informa del medido. Muestra: la columna 0 es la posicion audible.
    LEAD = 0.8
    rows = [r for r in rows if r[7] == 1 and not 5.8 < r[0] < 6.5 and r[0] < 31.8]

    def want(b):
        p = 0 if b < cyc else 1
        c = int(b % cyc // sq)
        return c, p, chord_at(BUL, p, c)[0], 1 if 6.5 <= b < cyc else 0
    bad_cur, bad_root, bad_pend, leads = [], [], [], []
    for i, (b, cur, root, pend, prog, idx, key, playing, ns) in enumerate(rows):
        ok = [want(b), want(b + LEAD)]
        if not any(cur == w[0] and prog == w[1] for w in ok):
            bad_cur.append(f'{b:.2f}: hueco {int(cur) + 1} prog {int(prog) + 1} (esperado {ok[0][0] + 1}, {ok[0][1] + 1})')
        if not any(int(root) % 12 == w[2] for w in ok):
            bad_root.append(f'{b:.2f}: {NN[int(root) % 12]} (esperado {NN[ok[0][2]]})')
        if not any(pend == w[3] for w in ok):
            bad_pend.append(f'{b:.2f}: {int(pend)} (esperado {ok[0][3]})')
        # adelanto: el indicador ya muestra el hueco siguiente antes del limite
        if i and cur != rows[i - 1][1]:
            nxt = (b // sq + 1) * sq
            leads.append(nxt - b if nxt - b < LEAD + 0.2 else 0)
    n = len(rows)
    lead = f', adelanto medido {sum(leads) / len(leads):.2f} beats' if leads else ''
    R.check('g_ind: el indicador marca el hueco y la progresion que suenan', n > 20 and not bad_cur,
            '; '.join(bad_cur[:3]) or f'{n} muestras{lead}')
    R.check('g_ind: el acorde marcado es el del estilo', n > 20 and not bad_root, '; '.join(bad_root[:3]) or f'{n} muestras')
    R.check('g_ind: "cambio pendiente" desde el cambio hasta el ciclo siguiente', n > 20 and not bad_pend,
            '; '.join(bad_pend[:3]) or f'{n} muestras')


SCENARIOS = {'harmony': harmony, 'voices': voices, 'output': output, 'persistence': persistence, 'gui': gui}


def lua_log(out, name):
    path = os.path.join(out, name + '.log')
    if not os.path.exists(path):
        R.check(f'{name}: registro', False, 'falta ' + path)
        return False
    done = False
    for l in open(path):
        l = l.rstrip('\n')
        tag = l.split(' ', 1)[0]
        if tag in ('PASS', 'FAIL', 'SKIP'):
            R.add(tag, l.split(' ', 1)[1])
        elif tag == 'DONE':
            done = True
            if '(' in l:
                R.check(f'{name}: termina sin cortes', False, l)
    if not done:
        R.check(f'{name}: el escenario termino', False, 'no hay linea DONE (sigue en marcha o se corto)')
    return done


def main(argv):
    args = argv[1:]
    rdir = os.environ.get('REAPER_DIR', os.path.expanduser('~/Library/Application Support/REAPER'))
    out = os.path.join(rdir, 'Scripts', 'GenderBenderTest', 'out')
    if args[:1] == ['--out']:
        out, args = args[1], args[2:]
    if not args or any(a not in SCENARIOS for a in args):
        raise SystemExit(__doc__.strip().splitlines()[-2] + '\nescenarios: ' + ', '.join(SCENARIOS))
    for name in args:
        print(f'== {name}')
        if lua_log(out, name):
            SCENARIOS[name](out)
    print(f'== total: {R.n["PASS"]} PASS, {R.n["FAIL"]} FAIL, {R.n["SKIP"]} SKIP')
    return 1 if R.n['FAIL'] else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
