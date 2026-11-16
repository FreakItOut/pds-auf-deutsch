# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='latin1')
d = open('_work/ascii_cgz/font_de.raw', 'rb').read()


def art16(ch):
    base = 0x60 + (ord(ch) - 0x20) * 32
    rows = []
    for y in range(16):
        v = (d[base + y * 2] << 8) | d[base + y * 2 + 1]
        rows.append(''.join('#' if v & (1 << (15 - x)) else '.' for x in range(16)))
    return rows


chars = 'Die Ube'
for c in chars:
    if c == ' ':
        continue
    print('==', repr(c), hex(0x60 + (ord(c) - 0x20) * 32))
    for r in art16(c):
        print('  ' + r)
