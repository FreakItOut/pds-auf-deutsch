# -*- coding: utf-8 -*-
# Rendert die ersten Glyphen eines FNT als ASCII-Kunst (16x16, 1bpp).
import csv
import sys

sys.stdout.reconfigure(encoding='latin1')
SECT, DATA = 2352, 2048


def read_file(binp, lba, size):
    out = bytearray()
    need, s = size, lba
    with open(binp, 'rb') as f:
        while need > 0:
            f.seek(s * SECT + 16)
            c = f.read(min(DATA, need))
            if not c:
                break
            out += c
            need -= len(c)
            s += 1
    return bytes(out[:size])


def fs_index(disc):
    fs = ('_work/fs_records_all.csv' if disc == 1
          else '_work/fs_records_cd%d.csv' % disc)
    return {r['name']: (int(r['lba']), int(r['size']))
            for r in csv.DictReader(open(fs, encoding='latin1'),
                                    delimiter=';') if int(r['lba']) > 0}


name = sys.argv[1] if len(sys.argv) > 1 else 'EVTCAMP.FNT'
n = int(sys.argv[2]) if len(sys.argv) > 2 else 16
lba, size = fs_index(1)[name]
d = read_file('_work/patched_disc1.bin', lba, size)
count = (len(d) - 18) // 32
print(name, 'size', size, 'glyphs(18+32n)', count,
      'header', d[:18].hex(' '))
for g in range(min(n, count)):
    o = 18 + g * 32
    rows = []
    for y in range(16):
        bits = (d[o + y * 2] << 8) | d[o + y * 2 + 1]
        rows.append(''.join('#' if bits & (1 << (15 - x)) else '.'
                            for x in range(16)))
    print('--- glyph %d' % g)
    for r in rows:
        print(r)
