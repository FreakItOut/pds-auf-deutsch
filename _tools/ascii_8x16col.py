# -*- coding: utf-8 -*-
# 8x16-Glyphen, Zellen spaltenweise (1 Byte = 8 vertikale Pixel).
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
img = Image.new('RGB', (cols*(8*scale+2), rows*(16*scale+lab)), (18,18,18))
dr = ImageDraw.Draw(img)
for g in range(n):
    o = g*bpc
    cx = (g % cols)*(8*scale+2)
    cy = (g // cols)*(16*scale+lab)
    dr.text((cx, cy), '%02x' % g, fill=(255,80,80))
    # zwei 8x8-Zellen, jede spaltenweise
    for cell in range(2):
        for x in range(8):
            b = d[o+cell*8+x]
            for y in range(8):
                if b & (1 << (7-y)):
                    px = cx+x*scale
                    py = cy+lab+(cell*8+y)*scale
                    for sy in range(scale):
                        for sx in range(scale):
                            img.putpixel((px+sx, py+sy),(235,235,235))
img.save('_work/review_fixes/ascii_8x16col.png')
print('saved', n)
