# -*- coding: utf-8 -*-
# Rendert ein Movie-FNT (16x16 1bpp) als Kontaktbogen.
import sys

from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding='latin1')
path = sys.argv[1]
d = open(path, 'rb').read()
import struct
cnt, typ = struct.unpack('>HH', d[:4])
print(path, 'count', cnt, 'type', typ)
n = min(cnt, 128)
cols = 24
rows = (n + cols - 1) // cols
cell = 16
scale = 3
lab = 11
img = Image.new('RGB', (cols * (cell * scale + 2),
                        rows * (cell * scale + lab)), (18, 18, 18))
dr = ImageDraw.Draw(img)
for g in range(n):
    o = 16 + g * 32
    cx = (g % cols) * (cell * scale + 2)
    cy = (g // cols) * (cell * scale + lab)
    dr.text((cx, cy), '%02x' % g, fill=(255, 80, 80))
    for y in range(16):
        bits = (d[o + y * 2] << 8) | d[o + y * 2 + 1]
        for x in range(16):
            if bits & (1 << (15 - x)):
                for sy in range(scale):
                    for sx in range(scale):
                        img.putpixel((cx + x * scale + sx,
                                      cy + lab + y * scale + sy),
                                     (235, 235, 235))
out = '_work/review_fixes/movie_font_%s.png' % (
    path.split('/')[-1].split('\\')[-1])
img.save(out)
print('saved', out)
