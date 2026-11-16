# -*- coding: utf-8 -*-
"""Rendert ausgewaehlte Glyphen gross nebeneinander."""
import sys

from PIL import Image

sys.stdout.reconfigure(encoding='latin1')
src, out = sys.argv[1], sys.argv[2]
scale = int(sys.argv[3]) if len(sys.argv) > 3 else 8
codes = [ord(c) for c in 'aouAOUs'] + [0x5E, 0x7C, 0x7E, 0x60, 0x5B, 0x5D, 0x7B]
d = open(src, 'rb').read()
BASE = 0xC60
cw, ch = 8 * scale, 16 * scale
img = Image.new('RGB', (len(codes) * cw + 10, ch), (40, 40, 40))
px = img.load()
for i, code in enumerate(codes):
    o = BASE + (code - 0x20) * 64
    gx = i * cw + 10
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
                    px[gx + c * scale + xx, r * scale + yy] = rgb
img.save(out)
print('ok', out, img.size)
