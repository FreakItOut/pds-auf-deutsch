# -*- coding: utf-8 -*-
# 8x8-Glyphen als planar 4bpp (4 Bitplanes pro Zeile, 32 B/Glyphe).
import sys

from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding='latin1')
d = open('_work/ascii_cgz/vram_pds_0.raw','rb').read()
bpc = 32
n = min(256, len(d)//bpc)
cols = 32
rows = (n+cols-1)//cols
scale = 5
lab = 11
img = Image.new('RGB', (cols*(8*scale+2), rows*(8*scale+lab)), (18,18,18))
dr = ImageDraw.Draw(img)
for g in range(n):
    o = g*bpc
    cx = (g % cols)*(8*scale+2)
    cy = (g // cols)*(8*scale+lab)
    dr.text((cx, cy), '%02x' % g, fill=(255,80,80))
    for y in range(8):
        planes = d[o+y*4:o+y*4+4]
        for x in range(8):
            v = 0
            for p in range(4):
                v |= ((planes[p] >> (7-x)) & 1) << p
            if v:
                c = 40+v*14
                for sy in range(scale):
                    for sx in range(scale):
                        img.putpixel((cx+x*scale+sx, cy+lab+y*scale+sy),(c,c,c))
img.save('_work/review_fixes/ascii_planar.png')
print('saved', n)
