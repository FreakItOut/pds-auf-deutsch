# Rendert ASCII.CGZ roh als 1bpp-Kontaktbogen (8x8/16x16, ab Offset 0/0x20).
import csv
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


lba, size = fs_index(1)['ASCII.CGZ']
d = read_file('_work/patched_disc1.bin', lba, size)
for start in (0x00, 0x20):
    for cell in (8, 16):
        bpc = cell * cell // 8
        n = min((len(d) - start) // bpc, 256)
        cols = 32
        rows = (n + cols - 1) // cols
        scale = 4 if cell == 8 else 2
        pad = 4
        img = Image.new('RGB', (cols * (cell * scale + 2),
                                rows * (cell * scale + pad)), (18, 18, 18))
        dr = ImageDraw.Draw(img)
        for g in range(n):
            off = start + g * bpc
            cx = (g % cols) * (cell * scale + 2)
            cy = (g // cols) * (cell * scale + pad)
            for y in range(cell):
                bpr = cell // 8
                row = 0
                for k in range(bpr):
                    row = (row << 8) | d[off + y * bpr + k]
                for x in range(cell):
                    if row & (1 << (cell - 1 - x)):
                        for sy in range(scale):
                            for sx in range(scale):
                                img.putpixel((cx + x * scale + sx,
                                              cy + pad + y * scale + sy),
                                             (235, 235, 235))
        out = '_work/review_fixes/ascii1_%02x_%d.png' % (start, cell)
        img.save(out)
        print('saved', out, n)
