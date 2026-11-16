# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='latin1')
d = open('_work/review_fixes/region_17d600c0000.bin', 'rb').read()
first_text = 0x8faa0
# Bereich davor auf Inhalt pruefen
for off in range(0x8d000, first_text, 0x200):
    seg = d[off:off + 0x200]
    nz = sum(1 for b in seg if b)
    print('%06x nz=%d %s' % (off, nz, seg[:16].hex(' ')))
