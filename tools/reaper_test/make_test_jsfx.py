#!/usr/bin/env python3
"""Genera la copia de prueba de GenderBender Melo para el banco de pruebas de REAPER.

La copia es el JSFX publicado con unas lineas inyectadas: el raton y los menus los pone el script de prueba
y la GUI exporta lo que dibuja. Todo pasa por gmem "gbtestgui" (tabla de posiciones en README.md).
Cada ancla tiene que aparecer exactamente una vez; si el plugin cambia, el generador falla y no escribe nada.

Uso: python3 tools/reaper_test/make_test_jsfx.py [origen.jsfx] destino.jsfx
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_SRC = os.path.join(HERE, '..', '..', 'GenderBenderMelo', 'genderbender_melo.jsfx')

# (ancla, texto, despues_del_ancla). El orden no importa: cada ancla es unica.
INJECTIONS = [
    ('desc: MIDI GenderBender Melo\n',
     'options:gmem=gbtestgui\n', True),
    # menus: devuelven la opcion que pone Lua (1-based, 0 = cancelar) y cuentan las llamadas
    ('@init\n',
     'function tmenu(s)( gmem[5] += 1; gmem[4] );\n', True),
    # raton simulado: una cola de pasos (x, y, mouse_cap, fotogramas) en gmem[100 + 4k ..], en unidades de la GUI
    # (900x540). gmem[0] = pasos que quedan, gmem[6] = paso actual. Toda la secuencia de un clic o un arrastre
    # se consume sin huecos: un fotograma con el raton real en medio soltaria el arrastre.
    ('ox = floor((gfx_w - UI_W * sc) / 2); oy = floor((gfx_h - UI_H * sc) / 2);\n',
     'gmem[0] > 0 ? ( tstB = 100 + gmem[6] * 4;\n'
     '\tmouse_x = ox + gmem[tstB] * sc; mouse_y = oy + gmem[tstB + 1] * sc; mouse_cap = gmem[tstB + 2];\n'
     '\tgmem[tstB + 3] -= 1; gmem[tstB + 3] <= 0 ? ( gmem[6] += 1; gmem[0] -= 1; );\n'
     ');\n', True),
    # aviso de estilo invalido por voz
    ('SD[v * SDSIZE + H_VALID] ? 0 : strcpy(#snb, "estilo invalido");\n',
     '\tgmem[40 + v] = !strcmp(#snb, "estilo invalido");\n', True),
    # indicador de progresion
    ('pend ? ( col(240, 200, 90); txt(PX + 420, PY + 50, "cambio pendiente"); );\n',
     '\tgmem[50] = cur; gmem[51] = c[C_ROOT + cur]; gmem[52] = pend; gmem[53] = c[C_PROG]; gmem[54] = c[C_IDX];\n'
     '\tgmem[55] = c[C_KEY]; gmem[56] = (play_state & 1) && cur >= 0 && cur < ns; gmem[57] = ns;\n'
     '\ts = 0; loop(ns, gmem[60 + s] = c[C_ROOT + s]; s += 1;);\n', True),
    # estado general y contador de fotogramas, al final de cada fotograma
    ('lastCap = mouse_cap;\n',
     'gmem[20] = sc; gmem[21] = ox; gmem[22] = oy; gmem[23] = gfx_w; gmem[24] = gfx_h;\n'
     'gmem[25] = UI_W * sc <= gfx_w + 0.5 && UI_H * sc <= gfx_h + 0.5 && ox >= 0 && oy >= 0;\n'
     'gmem[30] = motifCounter[0]; gmem[31] = motifCounter[1]; gmem[32] = motifCounter[2];\n'
     'gmem[33] = progSalt; gmem[34] = diceN; gmem[35] = slider5; gmem[36] = slider6; gmem[37] = dragId;\n'
     'gmem[9] += 1;\n', False),
]


def generate(src_text):
    s = src_text
    for anchor, text, after in INJECTIONS:
        n = s.count(anchor)
        if n != 1:
            raise SystemExit(f'make_test_jsfx: el ancla aparece {n} veces (tiene que ser 1): {anchor.strip()!r}')
        s = s.replace(anchor, anchor + text if after else text + anchor)
    n = s.count('gfx_showmenu(')
    if n == 0:
        raise SystemExit('make_test_jsfx: no hay ningun gfx_showmenu( que sustituir')
    s = s.replace('gfx_showmenu(', 'tmenu(')
    s = s.replace('desc: MIDI GenderBender Melo\n', 'desc: MIDI GenderBender Melo TEST\n', 1)
    return s


def main(argv):
    if len(argv) not in (2, 3):
        raise SystemExit(__doc__.strip().splitlines()[-1])
    src, dst = (DEFAULT_SRC, argv[1]) if len(argv) == 2 else (argv[1], argv[2])
    out = generate(open(src, encoding='utf-8').read())
    os.makedirs(os.path.dirname(os.path.abspath(dst)), exist_ok=True)
    with open(dst, 'w', encoding='utf-8') as f:
        f.write(out)
    print(f'ok -> {dst}')


if __name__ == '__main__':
    main(sys.argv)
