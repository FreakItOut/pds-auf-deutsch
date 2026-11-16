# -*- coding: utf-8 -*-
# 16x16-Glyphen, 4 Zellen (TL,TR,BL,BR) spaltenweise, 0..127.
import sys

from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding='latin1')
d = open('_work/ascii_cgz/vram_pds_0.raw','rb').read()
bpc = 32
n = min(128, len(d)//bpc)
cols = 24
rows = (n+cols-1)//cols
scale = 3
lab = 11
img = Image.new('RGB', (cols*(16*scale+2), rows*(16*scale+lab)), (18,18,18))
dr = ImageDraw.Draw(img)
for g in range(n):
    o = g*bpc
    cx = (g % cols)*(16*scale+2)
    cy = (g // cols)*(16*scale+lab)
    dr.text((cx, cy), '%02x' % g, fill=(255,80,80))
    for y in range(16):
        for x in range(16):
            q = (y//8)*2 + (x//8)
            byi = o + q*8 + (x % 8)
            b = d[byi]
            if b & (1 << (7-(y % 8))):
                for sy in range(scale):
                    for sx in range(scale):
                        img.putpixel((cx+x*scale+sx, cy+lab+y*scale+sy),(235,235,235))
img.save('_work/review_fixes/ascii_16cells.png')
print('saved', n)
