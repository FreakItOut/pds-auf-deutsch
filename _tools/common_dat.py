# -*- coding: utf-8 -*-
import csv
import struct
import sys

sys.stdout.reconfigure(encoding='latin1')
SECT, DATA = 2352, 2048
recs = {r['name']: (int(r['lba']), int(r['size']))
        for r in csv.DictReader(open('_work/fs_records_all.csv',
                                     encoding='latin1'), delimiter=';')
        if r['lba'].isdigit() and int(r['lba']) > 0}
for n in ('COMMON.DAT', 'ASCII.CGZ'):
    print(n, recs.get(n))

lba, size = recs['COMMON.DAT']
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
d = bytes(out[:size])
open('_work/review_fixes/common_dat.bin', 'wb').write(d)
print('COMMON.DAT size', size, 'head', d[:32].hex(' '))
print('strings:')
import re
for m in re.finditer(rb'[ -~]{5,}', d[:0x4000]):
    print(hex(m.start()), m.group()[:60])
