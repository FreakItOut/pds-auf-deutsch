# -*- coding: utf-8 -*-
# Rendert 'A' gross und zeigt Nibble-Werte.
import sys

from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding='latin1')
d = open('_work/ascii_cgz/vram_pds_0.raw','rb').read()
base = 0xC60
ch = 'A'
o = base + (ord(ch)-0x20)*64
scale = 24
img = Image.new('RGB', (8*scale, 16*scale), (0,0,0))
for y in range(16):
    for x in range(8):
        b = d[o+y*4+x//2]
        v = (b >> 4) if x % 2 == 0 else (b & 15)
        if v:
            c = 20+v*15
            for sy in range(scale):
                for sx in range(scale):
                    img.putpixel((x*scale+sx, y*scale+sy),(c,c,c))
img.save('_work/review_fixes/glyphA_big.png')
print('saved')
for y in range(16):
    row=''
    for x in range(8):
        b=d[o+y*4+x//2]
        v=(b>>4) if x%2==0 else (b&15)
        row += '%x'%v
    print(row)
