# -*- coding: utf-8 -*-
# Glyph 0x41 (16x16 cells_col) in Rotationen/Transpositionen.
import sys

from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding='latin1')
d = open('_work/ascii_cgz/vram_pds_0.raw','rb').read()
g = 0x41
o = g*32
scale = 14
modes = ('orig', 'rot90', 'rot180', 'rot270', 'transp', 'anti')
img = Image.new('RGB', (len(modes)*(16*scale+10), 16*scale+22), (18,18,18))
dr = ImageDraw.Draw(img)
for mi, mode in enumerate(modes):
    ox = mi*(16*scale+10)
    dr.text((ox+2, 2), mode, fill=(255,80,80))
    for y in range(16):
        for x in range(16):
            q = (y//8)*2 + (x//8)
            b = d[o+q*8+(x % 8)]
            bit = (b >> (7-(y % 8))) & 1
            if not bit:
                continue
            xx, yy = x, y
            if mode == 'rot90':
                xx, yy = y, 15-x
            elif mode == 'rot180':
                xx, yy = 15-x, 15-y
            elif mode == 'rot270':
                xx, yy = 15-y, x
            elif mode == 'transp':
                xx, yy = y, x
            elif mode == 'anti':
                xx, yy = 15-y, 15-x
            for sy in range(scale):
                for sx in range(scale):
                    img.putpixel((ox+xx*scale+sx, 20+yy*scale+sy),(235,235,235))
img.save('_work/review_fixes/glyph41_16modes.png')
print('saved')
