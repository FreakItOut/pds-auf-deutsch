# -*- coding: utf-8 -*-
# Liest Strings an Overlay-Adressen (Basis 0x06050000) aus einer Disc-Datei.
import csv
import io
import sys

sys.stdout.reconfigure(encoding='latin1')
SECT, DATA = 2352, 2048
name = sys.argv[1]
addrs = [int(x, 16) for x in sys.argv[2:]]
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
for a in addrs:
    o = a - 0x06050000
    if 0 <= o < len(data):
        e = o
        while e < len(data) and 32 <= data[e] < 127:
            e += 1
        print('%08x off=%06x %r' % (a, o, data[o:e].decode('latin1')))
    else:
        print('%08x off=%06x out of range' % (a, o))
