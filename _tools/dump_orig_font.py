# -*- coding: utf-8 -*-
"""Dumpt Glyphen aus dem Original-ASCII.CGZ (Disc 1) und dem gepatchten Font."""
import sys

sys.path.insert(0, '_tools')
sys.stdout.reconfigure(encoding='latin1')
from iso9660 import ISO9660Reader

SECT, DATA = 2352, 2048


def read(lba, size, path):
    out = bytearray()
    need, s = size, lba
    with open(path, 'rb') as f:
        while need > 0:
            f.seek(s * SECT + 16)
            c = f.read(min(DATA, need))
            if not c:
                break
            out += c
            need -= len(c)
            s += 1
    return bytes(out[:size])


iso = ISO9660Reader('Original_CD1/Panzer Dragoon Saga (Europe) (Disc 1) (Track 1).bin')
rec = None
for f in iso.list_files():
    if f['name'].upper() == 'ASCII.CGZ':
        rec = f
        break
print('rec', rec)
font = read(rec['lba'], rec['size'], 'Original_CD1/Panzer Dragoon Saga (Europe) (Disc 1) (Track 1).bin')
open('_work/ascii_cgz/font_orig.raw', 'wb').write(font)
print('len', len(font))


def rows8x16(data, ch, base=0xC60):
    o = base + (ord(ch) - 0x20) * 64
    return [''.join('%x%x' % (b >> 4, b & 15) for b in data[o + r * 4:o + r * 4 + 4])
            for r in range(16)]


for ch in [':', ';', '"', "'", '`', '^', '~', '|', '[', ']', 'u', 'U']:
    print('=== orig %r' % ch)
    for i, r in enumerate(rows8x16(font, ch)):
        print('%2d %s' % (i, r))
