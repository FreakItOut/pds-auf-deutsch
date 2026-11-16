# -*- coding: utf-8 -*-
# Rendert 16x16-Glyphen im VDP2-Zelllayout: 4 x 8x8 (TL,TR,BL,BR).
import sys

from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding='latin1')
d = open('_work/ascii_cgz/vram_pds_0.raw', 'rb').read()
for off in (0, 0x20, 0x40, 0x100, 0x200):
    n = min(128, (len(d) - off) // 32)
    if n < 16:
        continue
    cols = 24
    rows = (n + cols - 1) // cols
    cell = 16
    scale = 2
    pad = 4
    img = Image.new('RGB', (cols * (cell * scale + 2),
                            rows * (cell * scale + pad)), (18, 18, 18))
    dr = ImageDraw.Draw(img)
    for g in range(n):
        o = off + g * 32
        cx = (g % cols) * (cell * scale + 2)
        cy = (g // cols) * (cell * scale + pad)
        for qy in range(2):
            for qx in range(2):
                q = qy * 2 + qx
                for y in range(8):
                    b = d[o + q * 8 + y]
                    for x in range(8):
                        if b & (1 << (7 - x)):
                            px = cx + (qx * 8 + x) * scale
                            py = cy + pad + (qy * 8 + y) * scale
                            for sy in range(scale):
                                for sx in range(scale):
                                    img.putpixel((px + sx, py + sy),
                                                 (235, 235, 235))
    out = '_work/review_fixes/cgz_vdp2_%03x.png' % off
    img.save(out)
    print('saved', out, n)
