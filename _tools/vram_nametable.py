# -*- coding: utf-8 -*-
# Rendert die VDP2-Name-Table (0x6000..0x7FFF) mit Patterns ab VRAM 0.
import sys

from PIL import Image

sys.stdout.reconfigure(encoding='latin1')
v = open('_work/review_fixes/vram_full.bin', 'rb').read()
NT = 0x6000
W = H = 64
scale = 3
img = Image.new('RGB', (W*8*scale, H*8*scale), (0, 0, 0))
for cy in range(H):
    for cx in range(W):
        o = NT + (cy*W + cx)*2
        entry = (v[o] << 8) | v[o+1]
        if entry == 0:
            continue
        pn = entry & 0x7FF
        # 1x1 4bpp pattern = 32 Bytes
        po = pn*32
        for y in range(8):
            for x in range(8):
                if po + y*4 + x//2 >= len(v):
                    continue
                byte = v[po + y*4 + x//2]
                val = (byte >> 4) if x % 2 == 0 else (byte & 15)
                if val:
                    c = 40 + val*14
                    for sy in range(scale):
                        for sx in range(scale):
                            img.putpixel(((cx*8+x)*scale+sx,
                                          (cy*8+y)*scale+sy), (c, c, c))
img.save('_work/review_fixes/nametable.png')
print('saved')
# Nichtleere Eintraege ausgeben
used = []
for cy in range(H):
    for cx in range(W):
        o = NT + (cy*W + cx)*2
        entry = (v[o] << 8) | v[o+1]
        if entry:
            used.append((cy, cx, entry))
print('nonempty', len(used))
for u in used[:120]:
    print('y=%2d x=%2d entry=%04x pn=%03x pal=%d' % (
        u[0], u[1], u[2], u[2] & 0x7FF, u[2] >> 13))
