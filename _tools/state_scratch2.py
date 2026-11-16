# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='latin1')
font = open('_work/ascii_cgz/font_de.raw', 'rb').read()
sig = font[0x200:0x240]
for name in ('slot0', 'slot1'):
    st = open(r'_build\pds-recompile-de\state\%s.state' % name, 'rb').read()
    p = st.find(sig)
    print('==', name, 'sig at', hex(p) if p >= 0 else -1)
    if p < 0:
        continue
    base = p - 0x200
    blob = st[base + 0x6000:base + 0x6000 + 0x800]
    nz = sum(1 for b in blob if b)
    print('   scratch nonzero', nz, 'head', blob[:32].hex(' '))
    # erste 8 Tiles mit Inhalt zeigen
    shown = 0
    for t in range(64):
        g = blob[t * 32:(t + 1) * 32]
        ink = sum(1 for b in g for nib in (b >> 4, b & 15) if nib)
        if ink > 8:
            print('   tile', t, 'ink', ink)
            for y in range(16):
                row = ''
                for x in range(16):
                    b = g[y * 2 + x // 8]
                    bit = (b >> (7 - (x % 8))) & 1
                    row += '#' if bit else '.'
                print('     ' + row)
            shown += 1
            if shown >= 3:
                break
