# -*- coding: utf-8 -*-
# Zeigt 8x16-Glyphen aus ASCII.CGZ (Basis 0xC60, 64 B/Zeichen).
import sys

sys.stdout.reconfigure(encoding='latin1')
d = open('_work/ascii_cgz/vram_pds_0.raw', 'rb').read()
base = 0xC60


def glyph(ch):
    o = base + (ord(ch) - 0x20) * 64
    rows = []
    for y in range(16):
        line = ''
        for x in range(8):
            idx = o + y*4 + x//2
            b = d[idx]
            v = (b >> 4) if x % 2 == 0 else (b & 15)
            line += ' .:+*#@'[min(6, v)] if v else '.'
        rows.append(line)
    return rows


for ch in 'AaOoUusSB':
    print('==== %r' % ch)
    for r in glyph(ch):
        print(r)
