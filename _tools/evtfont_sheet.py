# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw

d = open('_work/review_fixes/extract_evtzoah.bin', 'rb').read()
n = (d[0] << 8) | d[1]
print('glyphs', n, 'size', len(d))
cols = 32
scale = 2
cell = 16 * scale + 2
rows = (n + cols - 1) // cols
img = Image.new('RGB', (cols * cell, rows * cell), (0, 0, 0))
dr = ImageDraw.Draw(img)
for g in range(n):
    off = 0x10 + g * 32
    if off + 32 > len(d):
        break
    cx = (g % cols) * cell
    cy = (g // cols) * cell
    for y in range(16):
        v = (d[off + y * 2] << 8) | d[off + y * 2 + 1]
        for x in range(16):
            if v & (1 << (15 - x)):
                for sy in range(scale):
                    for sx in range(scale):
                        img.putpixel((cx + x * scale + sx,
                                      cy + y * scale + sy), (230, 230, 230))
img.save('_work/review_fixes/evtzoah_font.png')
print('saved')
