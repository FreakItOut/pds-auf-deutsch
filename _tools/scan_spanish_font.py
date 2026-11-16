# -*- coding: utf-8 -*-
import os
import sys

sys.path.insert(0, '_tools')
from pds_kosinski3 import decompress

sys.stdout.reconfigure(encoding='latin1')
d = open('_work/review_fixes/spanish_archive.bin', 'rb').read()
print('archive size', len(d))
for base in (2424 * 2048, 2424 * 2352):
    for delta in range(-0x800, 0x801, 2):
        off = base + delta
        if off < 0 or off + 16 > len(d):
            continue
        try:
            out, used, n = decompress(d[off:off + 20000])
        except Exception:
            continue
        if 15000 <= len(out) <= 25000:
            print('FOUND off', hex(off), 'len', len(out), 'delta', delta)
            open('_work/review_fixes/spanish_font.raw', 'wb').write(out)
            sys.exit(0)
print('nichts gefunden')
