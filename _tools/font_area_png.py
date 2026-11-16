# -*- coding: utf-8 -*-
"""Rendert beliebige Bereiche der Font-Datei als 8x16-Raster."""
import sys

from PIL import Image

sys.stdout.reconfigure(encoding='latin1')
src, out = sys.argv[1], sys.argv[2]
start = int(sys.argv[3], 0) if len(sys.argv) > 3 else 0x2460
count = int(sys.argv[4]) if len(sys.argv) > 4 else 96
scale = int(sys.argv[5]) if len(sys.argv) > 5 else 4
d = open(src, 'rb').read()
COLS = 16
cw, ch = 8 * scale, 16 * scale
img = Image.new('RGB', (COLS * cw, ((count + COLS - 1) // COLS) * ch), (40, 40, 40))
px = img.load()
for idx in range(count):
    o = start + idx * 64
    if o + 64 > len(d):
        break
    gx = (idx % COLS) * cw
    gy = (idx // COLS) * ch
    for r in range(16):
        for c in range(8):
            byte = d[o + r * 4 + c // 2]
            v = (byte >> 4) if (c % 2 == 0) else (byte & 15)
            if v == 0:
                rgb = (40, 40, 40)
            elif v == 15:
                rgb = (0, 0, 0)
            else:
                g = max(30, min(255, (15 - v) * 36))
                rgb = (g, g, g)
            for yy in range(scale):
                for xx in range(scale):
                    px[gx + c * scale + xx, gy + r * scale + yy] = rgb
img.save(out)
print('ok', out, img.size, 'bytes', len(d))
