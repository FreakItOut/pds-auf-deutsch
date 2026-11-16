# -*- coding: utf-8 -*-
# Rendert VRAM ab 0x8000 als 16x16-4bpp-Glyphen im VDP2-Zelllayout.
import sys

from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding='latin1')
v = open('_work/review_fixes/vram_full.bin', 'rb').read()
base = 0x8000
bpc = 128
n = min(128, (len(v)-base)//bpc)
cols = 24
rows = (n+cols-1)//cols
scale = 3
lab = 11
img = Image.new('RGB', (cols*(16*scale+2), rows*(16*scale+lab)), (18,18,18))
dr = ImageDraw.Draw(img)
for g in range(n):
    o = base+g*bpc
    cx = (g % cols)*(16*scale+2)
    cy = (g // cols)*(16*scale+lab)
    dr.text((cx, cy), '%02x' % g, fill=(255,80,80))
    # VDP2 16x16 4bpp: 4 Zellen 8x8, je 8 Zeilen x 4 Bytes
    for cy8 in range(2):
        for cx8 in range(2):
            q = cy8*2+cx8
            for y in range(8):
                for x in range(8):
                    bo = o + q*32 + y*4 + x//2
                    if bo >= len(v):
                        continue
                    byte = v[bo]
                    val = (byte >> 4) if x % 2 == 0 else (byte & 15)
                    if val:
                        c = 40+val*14
                        px = cx+(cx8*8+x)*scale
                        py = cy+lab+(cy8*8+y)*scale
                        for sy in range(scale):
                            for sx in range(scale):
                                img.putpixel((px+sx, py+sy),(c,c,c))
img.save('_work/review_fixes/vram_8000.png')
print('saved', n)
