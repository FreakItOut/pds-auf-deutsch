# -*- coding: utf-8 -*-
import sys

sys.path.insert(0, '_tools')
from pds_kosinski3 import decompress

sys.stdout.reconfigure(encoding='latin1')
d = open('_work/review_fixes/spanish_archive.bin', 'rb').read()
for base in (0, 0x10, 0x800, 0x1000, 0x8000, 0x9300, 0x9300 - 0x11):
    for delta in range(-0x4000, 0x4001, 2):
        off = base + 2424 * 2048 + delta
        if off < 0 or off + 16 > len(d):
            continue
        try:
            out, used, n = decompress(d[off:off + 20000])
        except Exception:
            continue
        if 15000 <= len(out) <= 30000:
            print('FOUND base', hex(base), 'off', hex(off), 'len', len(out))
            open('_work/review_fixes/spanish_font.raw', 'wb').write(out)
            sys.exit(0)
print('nichts')
