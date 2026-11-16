# -*- coding: utf-8 -*-
import glob
import sys

sys.stdout.reconfigure(encoding='latin1')
font = open('_work/ascii_cgz/font_de.raw', 'rb').read()
sig = font[0x200:0x240]
for f in sorted(glob.glob('_work/review_fixes/sub2font_*.bin')):
    d = open(f, 'rb').read()
    i = d.find(sig)
    nz = sum(1 for b in d[0x6000:0x6800] if b)
    nz0 = sum(1 for b in d[:0x100] if b)
    print('%-46s sig@%-6s scr_nz=%-5d head_nz=%d' % (
        f.split('\\')[-1], hex(i) if i >= 0 else '-', nz, nz0))
