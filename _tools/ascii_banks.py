# -*- coding: utf-8 -*-
# Rendert ASCII.CGZ-Bereiche ab Offset 0x60/0x600 als 8x8/8x16 4bpp.
import sys

from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding='latin1')
d = open('_work/ascii_cgz/font_de.raw', 'rb').read()
for off in (0x60, 0x600, 0xC60, 0x1260):
    for cell in (8, 16):
        bpc = cell * cell // 2  # 4bpp
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
            dr.text((cx, cy), '%02x' % (0x20 + g), fill=(255, 80, 80))
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
        out = '_work/review_fixes/ascii_bank_%x_%d.png' % (off, cell)
        img.save(out)
        print('saved', out)
