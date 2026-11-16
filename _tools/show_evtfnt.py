# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='latin1')
d = open('_work/review_fixes/extract_272.bin', 'rb').read()
print('size', len(d), 'head', d[:16].hex(' '))
off = 0x10
for g in range(8):
    print('glyph', g, 'off', hex(off + g * 32))
    for y in range(16):
        row = d[off + g * 32 + y * 2: off + g * 32 + y * 2 + 2]
        if len(row) < 2:
            break
        v = (row[0] << 8) | row[1]
        print('   ' + ''.join('#' if v & (1 << (15 - x)) else '.' for x in range(16)))
