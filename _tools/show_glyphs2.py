# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='latin1')
d = open('_work/ascii_cgz/vram_pds_0.raw', 'rb').read()


def art(c, h=16):
    base = 0xC60 + (ord(c) - 0x20) * 64
    out = []
    for y in range(h):
        row = ''
        for x in range(8):
            b = d[base + y * 4 + x // 2]
            v = (b >> 4) if x % 2 == 0 else (b & 15)
            if v == 0:
                row += '.'
            elif v == 15:
                row += '@'
            elif v <= 7:
                row += ':'
            else:
                row += '+'
        out.append(row)
    return out


chars = sys.argv[1] if len(sys.argv) > 1 else 'ABCDEFGH'
print('  ' + '  '.join('%-8s' % c for c in chars))
for y in range(16):
    print('  ' + '  '.join(art(c)[y] for c in chars))
