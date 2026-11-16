# -*- coding: utf-8 -*-
# Probiert Glyph-Formate durch (16x16/8x16, row/column, 1/2bpp).
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
lba, size = fs_index(1)[name]
d = read_file('_work/patched_disc1.bin', lba, size)
count = (len(d) - 18) // 32
print(name, 'glyphs', count)
gs, ge = 0, 8


def show(title, grid):
    print('---', title)
    for r in grid:
        print(r)


# 1) 16x16 row-major (2 bytes per row)
for g in range(gs, min(ge, count)):
    o = 18 + g * 32
    grid = []
    for y in range(16):
        bits = (d[o + y * 2] << 8) | d[o + y * 2 + 1]
        grid.append(''.join('#' if bits & (1 << (15 - x)) else '.'
                            for x in range(16)))
    show('glyph %d 16x16 row' % g, grid)
