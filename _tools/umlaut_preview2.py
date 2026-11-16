# -*- coding: utf-8 -*-
# Vorschau mit Schwellwert (Hintergrundindex <=8 schwarz).
import sys

from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding='latin1')
d = open('_work/ascii_cgz/font_de.raw', 'rb').read()
base = 0xC60
chars = ['a', 'ä', 'o', 'ö', 'u', 'ü', 's', 'ß', '^', '|', '~', '{']
scale = 10
img = Image.new('RGB', (len(chars)*(8*scale+10), 16*scale+24), (0, 0, 0))
dr = ImageDraw.Draw(img)
for i, ch in enumerate(chars):
    o = base + (ord(ch)-0x20)*64
    ox = i*(8*scale+10)
    dr.text((ox+2, 2), ch, fill=(255, 80, 80))
    for y in range(16):
        for x in range(8):
            b = d[o+y*4+x//2]
            v = (b >> 4) if x % 2 == 0 else (b & 15)
            if v >= 9:
                c = 255 if v >= 13 else 150
                for sy in range(scale):
                    for sx in range(scale):
                        img.putpixel((ox+x*scale+sx, 20+y*scale+sy),
                                     (c, c, c))
img.save('_work/review_fixes/umlaut_preview2.png')
print('saved')
