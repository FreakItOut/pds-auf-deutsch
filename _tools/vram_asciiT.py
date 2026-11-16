# -*- coding: utf-8 -*-
# 8x8-4bpp ASCII-Font, Bytes als SPALTEN (transponiert).
import sys

from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding='latin1')
v = open('_work/review_fixes/vram_full.bin', 'rb').read()
base = int(sys.argv[1], 16) if len(sys.argv) > 1 else 0x460
n = 96
cols = 24
rows = (n+cols-1)//cols
scale = 5
lab = 11
img = Image.new('RGB', (cols*(8*scale+2), rows*(8*scale+lab)), (18,18,18))
dr = ImageDraw.Draw(img)
for k in range(n):
    o = base+k*32
    cx = (k % cols)*(8*scale+2)
    cy = (k // cols)*(8*scale+lab)
    dr.text((cx, cy), '%02x' % (0x20+k), fill=(255,80,80))
    for y in range(8):
        for x in range(8):
            if o+x*4+y//2 >= len(v):
                continue
            byte = v[o+x*4+y//2]
            val = (byte >> 4) if y % 2 == 0 else (byte & 15)
            if val:
                c = 40+val*14
                for sy in range(scale):
                    for sx in range(scale):
                        img.putpixel((cx+x*scale+sx, cy+lab+y*scale+sy),(c,c,c))
img.save('_work/review_fixes/vram_asciiT_%x.png' % base)
print('saved')
