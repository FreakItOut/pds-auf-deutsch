# -*- coding: utf-8 -*-
import glob
import sys

sys.stdout.reconfigure(encoding='latin1')
font = open('_work/ascii_cgz/font_de.raw', 'rb').read()
sig = font[0x200:0x240]
files = sorted(glob.glob('_work/review_fixes/subfont_*.bin'))
print('files', files)
for f in files:
    d = open(f, 'rb').read()
    i = d.find(sig)
    nz_scratch = sum(1 for b in d[0x6000:0x6800] if b)
    print('==', f, 'sig@', hex(i) if i >= 0 else -1,
          'scratch nz', nz_scratch)
