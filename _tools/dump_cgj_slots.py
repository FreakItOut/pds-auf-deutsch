# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='latin1')
BASE = 0xC60
for name in ('_work/ascii_cgz/font_orig_real.raw', '_work/ascii_cgz/font_de.raw'):
    d = open(name, 'rb').read()
    print('#####', name)
    for code in (0x7B, 0x5E, 0x7C, 0x7E, 0x60, 0x5B, 0x5D):
        o = BASE + (code - 0x20) * 64
        print('=== %02x %r' % (code, chr(code)))
        for r in range(16):
            print('%2d %s' % (r, ''.join('%x%x' % (b >> 4, b & 15)
                                         for b in d[o + r * 4:o + r * 4 + 4])))
