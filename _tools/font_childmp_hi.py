# Rendert Glyphen 0x80..0xFF des CHILDMP-Systemfonts.
import csv
import sys

from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding='latin1')
SECT, DATA = 2352, 2048
FONT_OFF = 0x10E98


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


lba, size = fs_index(1)['CHILDMP.MCB']
d = read_file('_work/patched_disc1.bin', lba, size)
n = 128
cols = 32
rows = (n + cols - 1) // cols
cell = 16
scale = 2
pad = 12
img = Image.new('RGB', (cols * (cell * scale + 2),
                        rows * (cell * scale + pad)), (18, 18, 18))
dr = ImageDraw.Draw(img)
for k in range(n):
    g = 128 + k
    off = FONT_OFF + 16 + g * 32
    cx = (k % cols) * (cell * scale + 2)
    cy = (k // cols) * (cell * scale + pad)
    dr.text((cx + 1, cy), '%02x' % g, fill=(255, 80, 80))
    for y in range(16):
        bits = (d[off + y * 2] << 8) | d[off + y * 2 + 1]
        for x in range(16):
            if bits & (1 << (15 - x)):
                for sy in range(scale):
                    for sx in range(scale):
                        img.putpixel((cx + x * scale + sx,
                                      cy + pad + y * scale + sy),
                                     (235, 235, 235))
img.save('_work/review_fixes/childmp_font_hi.png')
print('saved')
