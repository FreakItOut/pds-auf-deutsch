# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='latin1')
st = open(r'_build\pds-recompile-de\state\slot1.state', 'rb').read()
font = open('_work/ascii_cgz/font_de.raw', 'rb').read()
sig = font[0x200:0x240]
p = st.find(sig)
base = p - 0x200
print('font base in state', hex(base))
scratch = base + 0x6000
blob = st[scratch:scratch + 0x1000]
print('scratch head', blob[:64].hex(' '))
# 8x8 4bpp Kacheln rendern (16 Spalten)
for ty in range(0, 8):
    for tx in range(0, 16):
        off = (ty * 16 + tx) * 32
        g = blob[off:off + 32]
        if len(g) < 32:
            continue
        lines = []
        ink = 0
        for y in range(8):
            row = ''
            for x in range(8):
                b = g[y * 4 + x // 2]
                v = (b >> 4) if x % 2 == 0 else (b & 15)
                row += '#' if v else '.'
                ink += 1 if v else 0
            lines.append(row)
        if ink > 4:
            print('tile', ty * 16 + tx)
            for ln in lines:
                print('   ' + ln)
    print()
