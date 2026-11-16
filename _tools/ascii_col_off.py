# -*- coding: utf-8 -*-
# 8x16 spaltenweise, Startoffsets testen; Labels als ASCII-Codes.
import sys

from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding='latin1')
d = open('_work/ascii_cgz/vram_pds_0.raw','rb').read()
for off in (0x0, 0x300, 0x310, 0x318, 0x320, 0x600):
    n = min(96, (len(d)-off)//16)
    if n < 32:
        continue
    cols = 24
    rows = (n+cols-1)//cols
    scale = 5
    lab = 11
    img = Image.new('RGB', (cols*(8*scale+2), rows*(16*scale+lab)), (18,18,18))
    dr = ImageDraw.Draw(img)
    for k in range(n):
        o = off+k*16
        cx = (k % cols)*(8*scale+2)
        cy = (k // cols)*(16*scale+lab)
        dr.text((cx, cy), '%02x' % (0x20+k), fill=(255,80,80))
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
    out = '_work/review_fixes/ascii_col_%03x.png' % off
    img.save(out)
    print('saved', out)
