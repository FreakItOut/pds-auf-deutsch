# -*- coding: utf-8 -*-
# Einzelglyph 0x21 in allen Orientierungen, gross.
import sys

from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding='latin1')
d = open('_work/ascii_cgz/vram_pds_0.raw', 'rb').read()
bpc = 32
g = 0x21
scale = 16
modes = ('orig', 'rot90', 'rot180', 'rot270', 'transp',
         'transp+rot90', 'flipx', 'flipy')
W = len(modes) * (8 * scale + 8)
H = 8 * scale + 24
img = Image.new('RGB', (W, H), (18, 18, 18))
dr = ImageDraw.Draw(img)
for mi, mode in enumerate(modes):
    ox = mi * (8 * scale + 8)
    dr.text((ox + 2, 2), mode, fill=(255, 80, 80))
    for y in range(8):
        for x in range(8):
            o = g * bpc
            byte = d[o + y * 4 + x // 2]
            v = (byte >> 4) if x % 2 == 0 else (byte & 15)
            if not v:
                continue
            xx, yy = x, y
            if mode == 'rot90':
                xx, yy = y, 7 - x
            elif mode == 'rot180':
                xx, yy = 7 - x, 7 - y
            elif mode == 'rot270':
                xx, yy = 7 - y, x
            elif mode == 'transp':
                xx, yy = y, x
            elif mode == 'transp+rot90':
                xx, yy = 7 - y, x
            elif mode == 'flipx':
                xx, yy = 7 - x, y
            elif mode == 'flipy':
                xx, yy = x, 7 - y
            c = 40 + v * 14
            for sy in range(scale):
                for sx in range(scale):
                    img.putpixel((ox + xx * scale + sx,
                                  20 + yy * scale + sy), (c, c, c))
img.save('_work/review_fixes/glyph_modes.png')
print('saved')
