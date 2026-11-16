# -*- coding: utf-8 -*-
# Kontaktbogen 8x8 4bpp mit Glyphen-Nummern.
import sys

from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding='latin1')
d = open('_work/ascii_cgz/vram_pds_0.raw', 'rb').read()
cell = 8
bpc = 32
n = min(256, len(d) // bpc)
cols = 32
rows = (n + cols - 1) // cols
scale = 5
lab = 11
img = Image.new('RGB', (cols * (cell * scale + 2),
                        rows * (cell * scale + lab)), (18, 18, 18))
dr = ImageDraw.Draw(img)
for g in range(n):
    o = g * bpc
    cx = (g % cols) * (cell * scale + 2)
    cy = (g // cols) * (cell * scale + lab)
    dr.text((cx, cy), '%02x' % g, fill=(255, 80, 80))
    for y in range(cell):
        for x in range(cell):
            byte = d[o + y * 4 + x // 2]
            v = (byte >> 4) if x % 2 == 0 else (byte & 15)
            if v:
                c = 40 + v * 12
                for sy in range(scale):
                    for sx in range(scale):
                        img.putpixel((cx + x * scale + sx,
                                      cy + lab + y * scale + sy),
                                     (c, c, c))
img.save('_work/review_fixes/ascii_map.png')
print('saved ascii_map.png', n)
