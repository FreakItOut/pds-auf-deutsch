# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='latin1')
d = open('_work/review_fixes/spanish_font.raw', 'rb').read()
print('len', len(d))
BASE = 0xC60


def rows(data, code, base=BASE):
    o = base + (code - 0x20) * 64
    return [''.join('%x%x' % (b >> 4, b & 15) for b in data[o + r * 4:o + r * 4 + 4])
            for r in range(16)]


codes = [ord('u'), 0x5E, 0x60, 0x7E, 0x7C, 0x5B, 0x5D, 0xE4, 0xF6, 0xFC]
for code in codes:
    print('=== %02x %r' % (code, chr(code)))
    if code * 64 + BASE + 64 > len(d):
        print('   (ausserhalb)')
        continue
    for i, r in enumerate(rows(d, code)):
        print('%2d %s' % (i, r))
