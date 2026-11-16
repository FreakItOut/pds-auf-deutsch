# -*- coding: utf-8 -*-
"""Rendert die 8x16-Zeichentabelle als PNG (fuer Sichtpruefung)."""
import sys

from PIL import Image

sys.stdout.reconfigure(encoding='latin1')
src, out = sys.argv[1], sys.argv[2]
scale = int(sys.argv[3]) if len(sys.argv) > 3 else 3
d = open(src, 'rb').read()
BASE = 0xC60
COLS, ROWS = 16, 6
cw, ch = 8 * scale, 16 * scale
img = Image.new('RGB', (COLS * cw, ROWS * ch), (40, 40, 40))
px = img.load()
for idx in range(96):
    code = 0x20 + idx
    gx = (idx % COLS) * cw
    gy = (idx // COLS) * ch
    o = BASE + idx * 64
    for r in range(16):
        for c in range(8):
            byte = d[o + r * 4 + c // 2]
            v = (byte >> 4) if (c % 2 == 0) else (byte & 15)
            if v == 0:
                rgb = (40, 40, 40)          # transparent
            elif v == 15:
                rgb = (0, 0, 0)             # Outline
            else:
                # 8 = hellste Fuellung, e = dunkelster Zwischenwert
                g = max(30, min(255, (15 - v) * 36))
                rgb = (g, g, g)
            for yy in range(scale):
                for xx in range(scale):
                    px[gx + c * scale + xx, gy + r * scale + yy] = rgb
img.save(out)
print('ok', out, img.size)
