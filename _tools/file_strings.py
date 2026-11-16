# -*- coding: utf-8 -*-
# Extrahiert eine Datei aus patched_disc1.bin und listet ASCII-Strings.
import csv
import io
import re
import sys

sys.stdout.reconfigure(encoding='latin1')
SECT, DATA = 2352, 2048
name = sys.argv[1]
recs = {r['name']: (int(r['lba']), int(r['size']))
        for r in csv.DictReader(open('_work/fs_records_all.csv',
                                     encoding='latin1'), delimiter=';')}
if name not in recs:
    print('nicht in FS:', name)
    sys.exit(1)
lba, size = recs[name]
out = bytearray()
need, s = size, lba
with open('_work/patched_disc1.bin', 'rb') as f:
    while need > 0:
        f.seek(s * SECT + 16)
        c = f.read(min(DATA, need))
        if not c:
            break
        out += c
        need -= len(c)
        s += 1
data = bytes(out[:size])
open('_work/review_fixes/extract_%s.bin' % name.replace('.', '_'),
     'wb').write(data)
print('size', size)
for m in re.finditer(rb'[ -~]{5,}', data):
    t = m.group().decode('latin1')
    if sum(c.isalpha() for c in t) >= 4:
        print('%06x %r' % (m.start(), t[:90]))
