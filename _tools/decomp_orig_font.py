# -*- coding: utf-8 -*-
import sys

sys.path.insert(0, '_tools')
sys.stdout.reconfigure(encoding='latin1')
from pds_kosinski3 import decompress

raw = open('_work/ascii_cgz/real_disc1.cgz', 'rb').read()
orig = decompress(raw)[0]
print('decompressed', len(orig))
open('_work/ascii_cgz/font_orig_real.raw', 'wb').write(orig)

patched = open('_work/ascii_cgz/font_de.raw', 'rb').read()
print('patched len', len(patched))

BASE = 0xC60


def rows(data, code):
    o = BASE + (code - 0x20) * 64
    return [''.join('%x%x' % (b >> 4, b & 15) for b in data[o + r * 4:o + r * 4 + 4])
            for r in range(16)]


chars = 'u U i j : ; " \' ` ^ ~ | [ ]'.split()
for ch in chars:
    print('=== orig %r' % ch)
    for i, r in enumerate(rows(orig, ord(ch))):
        print('%2d %s' % (i, r))
