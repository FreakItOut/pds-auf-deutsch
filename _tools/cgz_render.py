# -*- coding: utf-8 -*-
# Rendert Ausschnitte aus dem entpackten ASCII.CGZ als 8x8/16x16-Glyphen.
import sys

from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding='latin1')
d = open('_work/ascii_cgz/vram_pds_0.raw', 'rb').read()
for off in (0, 0x10, 0x20, 0x40, 0x60, 0x80, 0x100, 0x120, 0x140):
    for cell in (8, 16):
        bpc = cell * cell // 8
        n = min(96, (len(d) - off) // bpc)
        if n < 32:
            continue
        cols = 24
        rows = (n + cols - 1) // cols
        scale = 4 if cell == 8 else 2
        pad = 4
        img = Image.new('RGB', (cols * (cell * scale + 2),
                                rows * (cell * scale + pad)), (18, 18, 18))
        dr = ImageDraw.Draw(img)
        for g in range(n):
            o = off + g * bpc
            cx = (g % cols) * (cell * scale + 2)
            cy = (g // cols) * (cell * scale + pad)
            for y in range(cell):
                bpr = cell // 8
                row = 0
                for k in range(bpr):
                    row = (row << 8) | d[o + y * bpr + k]
                for x in range(cell):
                    if row & (1 << (cell - 1 - x)):
                        for sy in range(scale):
                            for sx in range(scale):
                                img.putpixel((cx + x * scale + sx,
                                              cy + pad + y * scale + sy),
                                             (235, 235, 235))
        out = '_work/review_fixes/cgz_%03x_%d.png' % (off, cell)
        img.save(out)
        print('saved', out, n)
