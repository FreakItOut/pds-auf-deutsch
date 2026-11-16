# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='latin1')
d = open('_work/ascii_cgz/font_de.raw', 'rb').read()


def art(ch):
    base = 0xC60 + (ord(ch) - 0x20) * 64
    out = []
    for y in range(16):
        row = ''
        for x in range(8):
            b = d[base + y * 4 + x // 2]
            v = (b >> 4) if x % 2 == 0 else (b & 15)
            row += '#' if v else '.'
        out.append(row)
    return out


cols = ['A', 'Ä', 'O', 'Ö', 'U', 'Ü', 'a', 'ä', 'o', 'ö', 'u', 'ü', 's', 'ß']
labels = ['A', 'Ae', 'O', 'Oe', 'U', 'Ue', 'a', 'ae', 'o', 'oe', 'u', 'ue',
          's', 'ss']
print('  ' + '  '.join('%-8s' % l for l in labels))
for y in range(16):
    print('  ' + '  '.join(art(c)[y] for c in cols))
