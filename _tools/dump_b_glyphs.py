# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='latin1')
d = open('_work/ascii_cgz/font_orig_real.raw', 'rb').read()
BASE = 0xC60
for code in (ord('B'), ord('b'), ord('f'), ord('l'), ord('s'), ord('S'), ord('E')):
    o = BASE + (code - 0x20) * 64
    print('=== %r' % chr(code))
    for r in range(16):
        vals = []
        for b in d[o + r * 4:o + r * 4 + 4]:
            vals.append(b >> 4)
            vals.append(b & 15)
        print('%2d %s' % (r, ''.join('%x' % v for v in vals)))
