# -*- coding: utf-8 -*-
# 16x8-Glyphen (16 Bytes = 16 Spalten a 8 Bit) - Transponierte Variante.
import sys

from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding='latin1')
d = open('_work/ascii_cgz/vram_pds_0.raw','rb').read()
bpc = 16
n = min(256, len(d)//bpc)
cols = 32
rows = (n+cols-1)//cols
scale = 5
lab = 11
img = Image.new('RGB', (cols*(16*scale+2), rows*(8*scale+lab)), (18,18,18))
dr = ImageDraw.Draw(img)
for g in range(n):
    o = g*bpc
    cx = (g % cols)*(16*scale+2)
    cy = (g // cols)*(8*scale+lab)
    dr.text((cx, cy), '%02x' % g, fill=(255,80,80))
    for x in range(16):
        b = d[o+x]
        for y in range(8):
            if b & (1 << (7-y)):
                for sy in range(scale):
                    for sx in range(scale):
                        img.putpixel((cx+x*scale+sx, cy+lab+y*scale+sy),(235,235,235))
img.save('_work/review_fixes/ascii_16x8.png')
print('saved', n)
