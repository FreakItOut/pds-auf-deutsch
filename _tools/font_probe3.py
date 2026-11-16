# -*- coding: utf-8 -*-
# 8x16 2bpp-Darstellung (2 Bytes/Zeile = 8 Pixel * 2 Bit).
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


name = sys.argv[1] if len(sys.argv) > 1 else 'BTL_A52.FNT'
n = int(sys.argv[2]) if len(sys.argv) > 2 else 8
lba, size = fs_index(1)[name]
d = read_file('_work/patched_disc1.bin', lba, size)
count = (len(d) - 18) // 32
print(name, 'glyphs', count)
for g in range(0, min(n, count)):
    o = 18 + g * 32
    print('=== glyph %d' % g)
    for y in range(16):
        b0 = d[o + y * 2]
        b1 = d[o + y * 2 + 1]
        line = ''
        for x in range(8):
            v = ((b0 >> (7 - x)) & 1) << 1 | \
                ((b1 >> (7 - x)) & 1)
            line += ' .:#'[v]
        print(line)
