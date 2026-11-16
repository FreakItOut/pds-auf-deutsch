# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='latin1')
d = open('_work/ascii_cgz/font_de.raw', 'rb').read()
print('font size', len(d))
base = 0xC60


def rows8x16(ch):
    o = base + (ord(ch) - 0x20) * 64
    out = []
    for r in range(16):
        out.append(''.join('%x%x' % (b >> 4, b & 15)
                           for b in d[o + r * 4:o + r * 4 + 4]))
    return out


for ch in ['u', '^', '|', '~', 'A', '`', '[', ']', 'a', 'o']:
    print('=== %r' % ch)
    for i, r in enumerate(rows8x16(ch)):
        print('%2d %s' % (i, r))
