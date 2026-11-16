# -*- coding: utf-8 -*-
# Zeigt den Textbereich um einen Offset einer Disc-Datei.
import csv
import sys

sys.stdout.reconfigure(encoding='latin1')
SECT, DATA = 2352, 2048
name = sys.argv[1]
off = int(sys.argv[2], 0)
span = int(sys.argv[3], 0) if len(sys.argv) > 3 else 0x400
recs = {r['name']: (int(r['lba']), int(r['size']))
        for r in csv.DictReader(open('_work/fs_records_all.csv',
                                     encoding='latin1'), delimiter=';')}
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
lo = max(0, off - span // 2)
hi = min(len(data), off + span // 2)
print('file', name, 'size', size)
pos = lo
while pos < hi:
    e = pos
    while e < hi and 32 <= data[e] < 127:
        e += 1
    if e - pos >= 3:
        print('%06x %r' % (pos, data[pos:e].decode('latin1')))
        pos = e
    else:
        pos += 1
