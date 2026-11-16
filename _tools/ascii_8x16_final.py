# -*- coding: utf-8 -*-
# 8x16-Zeichen ab Pattern 0x63 (0xC60): 16 B pro Zeichen (oben/unten).
import sys

from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding='latin1')
v = open('_work/review_fixes/vram_full.bin', 'rb').read()
base = 0xC60
n = 96
cols = 24
rows = (n+cols-1)//cols
scale = 4
lab = 11
img = Image.new('RGB', (cols*(8*scale+2), rows*(16*scale+lab)), (18,18,18))
dr = ImageDraw.Draw(img)
for k in range(n):
    o = base+k*16
    cx = (k % cols)*(8*scale+2)
    cy = (k // cols)*(16*scale+lab)
    dr.text((cx, cy), '%02x' % (0x20+k), fill=(255,80,80))
    for y in range(16):
        for x in range(8):
            byte = v[o+y*4+x//2] if o+y*4+x//2 < len(v) else 0
            val = (byte >> 4) if x % 2 == 0 else (byte & 15)
            if val:
                c = 40+val*14
                for sy in range(scale):
                    for sx in range(scale):
                        img.putpixel((cx+x*scale+sx, cy+lab+y*scale+sy),(c,c,c))
img.save('_work/review_fixes/ascii_8x16_final.png')
print('saved')
