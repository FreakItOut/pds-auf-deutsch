# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='latin1')
for name in ('_work/ascii_cgz/font_orig_real.raw', '_work/ascii_cgz/font_de.raw'):
    d = open(name, 'rb').read()
    print('#####', name, len(d))
    BASE = 0x60
    for code in (ord('u'), ord('^'), ord('`'), ord('A')):
        o = BASE + (code - 0x20) * 32
        print('=== %r %02x' % (chr(code), code))
        for r in range(8):
            print('%2d %s' % (r, ''.join('%x%x' % (b >> 4, b & 15)
                                         for b in d[o + r * 4:o + r * 4 + 4])))
