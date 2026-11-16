# -*- coding: utf-8 -*-
# Kontaktbogen der Glyphen eines FNT (16x16, 1bpp, MSB-first).
import csv
import os
import sys

from PIL import Image, ImageDraw

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


name = os.path.splitext(sys.argv[1])[0] if len(sys.argv) > 1 \
    else 'BTL_A52'
limit = int(sys.argv[2]) if len(sys.argv) > 2 else 0
lba, size = fs_index(1)[name + '.FNT']
d = read_file('_work/patched_disc1.bin', lba, size)
count = (len(d) - 18) // 32
if limit:
    count = min(count, limit)
SCALE = 3
COLS = 16
CELL = 16 * SCALE + 4
LABEL = 12
rows = (count + COLS - 1) // COLS
img = Image.new('RGB', (COLS * CELL, rows * (CELL + LABEL)),
                (20, 20, 20))
dr = ImageDraw.Draw(img)
for g in range(count):
    o = 18 + g * 32
    cx = (g % COLS) * CELL
    cy = (g // COLS) * (CELL + LABEL)
    dr.text((cx + 2, cy), str(g), fill=(255, 80, 80))
    for y in range(16):
        bits = (d[o + y * 2] << 8) | d[o + y * 2 + 1]
        for x in range(16):
            if bits & (1 << (15 - x)):
                for sy in range(SCALE):
                    for sx in range(SCALE):
                        img.putpixel((cx + 2 + x * SCALE + sx,
                                      cy + LABEL + y * SCALE + sy),
                                     (235, 235, 235))
out = '_work/review_fixes/font_%s.png' % name
img.save(out)
print('saved', out, 'glyphs', count)
