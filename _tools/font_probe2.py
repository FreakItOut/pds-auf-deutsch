# -*- coding: utf-8 -*-
# Testet transponierte/4bpp-Darstellungen der FNT-Glyphen.
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
for g in range(0, 6):
    o = 18 + g * 32
    print('=== glyph %d' % g)
    # transponiert: 16 Spalten a 16 Bit
    for y in range(16):
        line = ''
        for x in range(16):
            bits = (d[o + x * 2] << 8) | d[o + x * 2 + 1]
            line += '#' if bits & (1 << (15 - y)) else '.'
        print(line)
    print('--- 8x16 4bpp (nibbles)')
    shade = '.:-=+*#%@'
    for y in range(16):
        row = d[o + y * 2:o + y * 2 + 2]
        line = ''
        for b in row:
            line += shade[b >> 4] + shade[b & 15]
        print(line)
