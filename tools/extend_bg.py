"""Genera GenderBender/bg.png (686x486) a partir de bg_original.png (686x369),
anadiendo abajo una franja de madera con el panel GROOVE.
Uso: python3 tools/extend_bg.py   (requiere Pillow)"""
import os
import random
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', 'GenderBender', 'bg_original.png')
DST = os.path.join(HERE, '..', 'GenderBender', 'bg.png')

NEW_H = 486                        # debe coincidir con @gfx en genderbender.jsfx
PANEL = (14, 373, 672, 482)        # x0, y0, x1, y1 del panel GROOVE
PANEL_DARKEN = 0.42                # mismo oscurecido que los paneles originales (~17/40)

orig = Image.open(SRC).convert('RGB')
w, h = orig.size
strip_h = NEW_H - h

# madera: la columna izquierda (sin paneles) estirada en horizontal conserva las vetas de las tablas
band = orig.crop((0, h - strip_h, 10, h)).resize((w, strip_h), Image.BILINEAR)
rnd = random.Random(5)
px = band.load()
for y in range(strip_h):
    for x in range(w):
        n = rnd.randint(-6, 6)
        r, g, b = px[x, y]
        px[x, y] = (max(0, r + n), max(0, g + n), max(0, b + n))
band = band.filter(ImageFilter.GaussianBlur(0.6))

out = Image.new('RGB', (w, NEW_H))
out.paste(orig, (0, 0))
out.paste(band, (0, h))

# panel oscuro con esquinas redondeadas, como los existentes
x0, y0, x1, y1 = PANEL
region = out.crop(PANEL)
dark = region.point(lambda v: int(v * PANEL_DARKEN))
mask = Image.new('L', region.size, 0)
ImageDraw.Draw(mask).rounded_rectangle((0, 0, region.size[0] - 1, region.size[1] - 1), radius=4, fill=255)
region.paste(dark, (0, 0), mask)
out.paste(region, (x0, y0))

out.save(DST)
print('ok', out.size)
