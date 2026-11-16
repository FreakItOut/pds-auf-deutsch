# -*- coding: utf-8 -*-
# Rendert 4bpp-Glyphen (8x8 = 32 B, 16x16 = 128 B) aus dem entpackten Font.
import sys

from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding='latin1')
d = open('_work/ascii_cgz/vram_pds_0.raw', 'rb').read()
for cell in (8, 16):
    bpc = cell * cell // 2
    for off in (0, 0x20, 0x40, 0x100):
        n = min(96, (len(d) - off) // bpc)
        if n < 16:
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
                for x in range(cell):
                    byte = d[o + y * (cell // 2) + x // 2]
                    v = (byte >> 4) if x % 2 == 0 else (byte & 15)
                    if v:
                        c = 40 + v * 14
                        for sy in range(scale):
                            for sx in range(scale):
                                img.putpixel((cx + x * scale + sx,
                                              cy + pad + y * scale + sy),
                                             (c, c, c))
        out = '_work/review_fixes/cgz4_%03x_%d.png' % (off, cell)
        img.save(out)
        print('saved', out, n)
