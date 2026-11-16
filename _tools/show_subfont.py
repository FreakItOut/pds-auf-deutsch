# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='latin1')
d = open('_work/ascii_cgz/font_de.raw', 'rb').read()


def art(ch):
    base = ord(ch) * 32
    rows = []
    for y in range(8):
        row = ''
        for x in range(8):
            b = d[base + y * 4 + x // 2]
            v = (b >> 4) if x % 2 == 0 else (b & 15)
            row += '#' if v else '.'
        rows.append(row)
    return rows


chars = 'Die Ube'
for c in chars:
    if c == ' ':
        continue
    print('==', repr(c), hex(ord(c) * 32))
    for r in art(c):
        print('  ' + r)
