#!/usr/bin/env python3
"""Pruebas de la teoria y del compilador de estilos melodicos.

  python3 tools/test_melo.py
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from make_melo_style import StyleError, from_txt, parse_style, to_style, to_txt  # noqa: E402
from melo_theory import TheoryError, mask_to_list, parse_chord, parse_key, scale_mask  # noqa: E402


class Theory(unittest.TestCase):
    def test_v7_harmonic_minor(self):
        root, mask = parse_chord('V7', 'harmonic_minor')
        self.assertEqual(root, 7)
        self.assertEqual(mask_to_list(mask), [0, 4, 7, 10])

    def test_bII_phrygian_dominant(self):
        self.assertEqual(parse_chord('bII', 'phrygian_dominant'), (1, 0b10010001))

    def test_andalusian(self):
        roots = [parse_chord(c, 'phrygian_dominant')[0] for c in ('iv', 'bIII', 'bII', 'I')]
        self.assertEqual(roots, [5, 3, 1, 0])

    def test_minor_vii_vi(self):
        self.assertEqual(parse_chord('VII', 'minor')[0], 10)
        self.assertEqual(parse_chord('VI', 'minor')[0], 8)

    def test_suffixes(self):
        self.assertEqual(mask_to_list(parse_chord('ii7', 'major')[1]), [0, 3, 7, 10])
        self.assertEqual(mask_to_list(parse_chord('Imaj7', 'major')[1]), [0, 4, 7, 11])
        self.assertEqual(mask_to_list(parse_chord('im9', 'minor')[1]), [0, 2, 3, 7, 10])
        self.assertEqual(mask_to_list(parse_chord('vii°', 'major')[1]), [0, 3, 6])
        self.assertEqual(mask_to_list(parse_chord('Vsus4', 'major')[1]), [0, 5, 7])

    def test_errors(self):
        for bad in ('X', 'Iv', 'Vfoo'):
            with self.assertRaises(TheoryError):
                parse_chord(bad, 'major')
        with self.assertRaises(TheoryError):
            scale_mask('lydian_flat13')

    def test_key(self):
        self.assertEqual(parse_key('A'), 9)
        self.assertEqual(parse_key('Bb'), 10)


MINI = """name: PRUEBA
bpm: 100
key: A
scale: harmonic_minor
form.mel: A A' A B
prog: i iv V7 i
prog: i VII VI V7
sub: V7 > bII7
markov: i > iv 3, V7 2
markov: iv > V7 1, i 1
markov: V7 > i 1
markov: VII > VI 1
markov: VI > V7 1
[p0 p1 p2 p3 p4 p5 p6 p7 p8]
bass.rhy   X... ..x. X... ..x.
bass.deg   R... ..5. 5... ..a.
bass.art   .... .... ~... .../
chord.rhy  ..X. ..X. ..X. ..X.
chord.voi  ..7. ..t. ..9. ..h.
mel.rhy    X.x. X... x.x. X...
mel.cnt    ^.+. -... +.+. ^...
[p8]
mel.rhy    X.X.X.X.X.X.X.X. X.X.X.X.X.X.X.[17].
"""


class Compiler(unittest.TestCase):
    def test_build(self):
        s = parse_style(MINI, 'mini.mstyle')
        self.assertEqual(s['steps'], 32)
        self.assertEqual(len(s['progs']), 2)
        rhy, deg, art = s['voices'][0][4]
        self.assertEqual(rhy[:8], [255, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(deg[12], 2)            # '5' en la 7a semicorchea -> paso 12
        self.assertEqual(art[30], 2)            # slide al final (16a semicorchea)
        self.assertEqual(s['voices'][2][8][0][30], 17)
        txt = to_txt(s)
        self.assertTrue(txt.startswith('7714,1\n') and txt.endswith('7714\n'))
        self.assertNotIn(' ', txt)

    def test_roundtrip(self):
        txt = to_txt(parse_style(MINI))
        again = to_txt(parse_style(to_style('PRUEBA', from_txt(txt))))
        self.assertEqual(txt, again)

    def test_ternary(self):
        src = MINI.replace('bpm: 100', 'bpm: 80\nmeter: 12/8')
        src = src.split('[p0')[0] + '[p0 p1 p2 p3 p4 p5 p6 p7 p8]\n' + \
            'bass.rhy X..X.. X..X..\nchord.rhy ..X..X ..X..X\nmel.rhy X.X.X. X.X.X.\n'
        s = parse_style(src)
        self.assertEqual(s['steps'], 24)
        self.assertEqual(s['voices'][0][0][0][6], 255)
        self.assertEqual(to_txt(parse_style(to_style('X', from_txt(to_txt(s))))), to_txt(s))

    def assertFails(self, src, *parts):
        with self.assertRaises(StyleError) as cm:
            parse_style(src, 'mini.mstyle')
        for part in parts:
            self.assertIn(part, str(cm.exception))

    def test_bad_symbol(self):
        self.assertFails(MINI.replace('bass.deg   R...', 'bass.deg   Rq..'),
                         'mini.mstyle linea 16', '"q"', 'posicion 2')

    def test_missing_pattern(self):
        self.assertFails(MINI.replace('[p0 p1 p2', '[p1 p2'), 'bass.rhy', 'p0')

    def test_unknown_chord(self):
        self.assertFails(MINI.replace('prog: i iv V7 i', 'prog: i iv Q7 i'), 'linea 6', 'Q7')

    def test_markov_dead_end(self):
        self.assertFails(MINI.replace('markov: VI > V7 1\n', ''), 'VI', 'sucesores')

    def test_truncated(self):
        txt = to_txt(parse_style(MINI))
        with self.assertRaises(StyleError):
            from_txt(txt[:len(txt) // 2])
        with self.assertRaises(StyleError):
            from_txt(txt.replace('\n7714\n', '\n'))


if __name__ == '__main__':
    unittest.main()
