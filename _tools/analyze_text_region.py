# -*- coding: utf-8 -*-
import re
import sys

sys.stdout.reconfigure(encoding='latin1')
d = open('_work/review_fixes/region_17d600c0000.bin', 'rb').read()
i = d.find(b'Geniesse')
print('text at', hex(i), 'size', len(d))
print('before:', repr(d[i - 64:i + 200]))
print()
# Strings in der Umgebung
start = max(0, i - 0x1000)
for m in re.finditer(rb'[ -~]{5,}', d[start:i + 0x800]):
    off = start + m.start()
    print('%06x %r' % (off, m.group()[:70]))
