# -*- coding: utf-8 -*-
# Entpackt ASCII.CGZ (LZ-Decompressor aus VDP2.cpp) und rendert die
# Font-Muster als Kontaktbogen.
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


def unpack(src):
    d = bytearray()
    p = 0
    r6 = src[p]
    p += 1
    r7 = 9
    while True:
        if r7 == 1:
            r6 = src[p]
            p += 1
            r7 = 9
        r7 -= 1
        bit = r6 & 1
        r6 >>= 1
        if bit:
            d.append(src[p])
            p += 1
            continue
        if r7 == 1:
            r6 = src[p]
            p += 1
            r7 = 9
        r7 -= 1
        bit2 = r6 & 1
        r6 >>= 1
        if bit2:
            r0 = src[p]
            r1 = src[p + 1]
            p += 2
            comp = (r1 << 8) | r0
            if comp == 0:
                return bytes(d)
            if comp & 0x8000:
                comp -= 0x10000
            off = comp >> 3
            n = r0 & 7
            if n:
                n += 2
            else:
                n = src[p] + 1
                p += 1
            s = len(d) + off
            for i in range(n):
                d.append(d[s + i])
        else:
            r0 = 0
            if r7 == 1:
                r6 = src[p]
                p += 1
                r7 = 9
            r7 -= 1
            r0 |= r6 & 1
            r6 >>= 1
            if r7 == 1:
                r6 = src[p]
                p += 1
                r7 = 9
            r7 -= 1
            r0 <<= 1
            r0 |= r6 & 1
            r6 >>= 1
            r2 = src[p] | 0xFF00
            if r2 < 0x8000:
                pass
            p += 1
            off = r2 - 0x10000 if r2 >= 0x8000 else r2
            n = r0 + 2
            s = len(d) + off
            for i in range(n):
                d.append(d[s + i])


lba, size = fs_index(1)['ASCII.CGZ']
raw = read_file('_work/patched_disc1.bin', lba, size)
d = unpack(raw)
print('ASCII.CGZ', size, '-> unpacked', len(d))
open('_work/review_fixes/ascii_cgz.bin', 'wb').write(d)

for cell, cols in ((16, 16), (8, 32)):
    n = len(d) // (cell * cell // 8)
    n = min(n, 512)
    rows = (n + cols - 1) // cols
    scale = 3 if cell == 16 else 5
    pad = 4 + (12 if cell == 16 else 0)
    img = Image.new('RGB', (cols * (cell * scale + 4),
                            rows * (cell * scale + pad)), (20, 20, 20))
    dr = ImageDraw.Draw(img)
    for g in range(n):
        off = g * (cell * cell // 8)
        cx = (g % cols) * (cell * scale + 4)
        cy = (g // cols) * (cell * scale + pad)
        if cell == 16:
            dr.text((cx + 1, cy), str(g), fill=(255, 80, 80))
        for y in range(cell):
            row = d[off + y * (cell // 8)] if cell == 8 else None
            if cell == 16:
                bits = (d[off + y * 2] << 8) | d[off + y * 2 + 1]
            else:
                bits = d[off + y]
            for x in range(cell):
                if bits & (1 << (cell - 1 - x)):
                    for sy in range(scale):
                        for sx in range(scale):
                            img.putpixel((cx + x * scale + sx,
                                          cy + pad + y * scale + sy),
                                         (235, 235, 235))
    out = '_work/review_fixes/ascii_font_%d.png' % cell
    img.save(out)
    print('saved', out, 'glyphs', n)
