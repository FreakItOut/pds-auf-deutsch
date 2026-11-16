# -*- coding: utf-8 -*-
# Glyph 0x41 in vielen Bit-/Nibble-Orientierungen (8x8, 4bpp).
import sys

from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding='latin1')
d = open('_work/ascii_cgz/vram_pds_0.raw','rb').read()
g = 0x41
bpc = 32
scale = 12
modes = []
for nib in ('hi', 'lo'):
    for xf in (0, 1):
        for yf in (0, 1):
            for tr in (0, 1):
                modes.append((nib, xf, yf, tr))
cols = 8
rows = (len(modes)+cols-1)//cols
cellw = 8*scale
cellh = 8*scale+16
img = Image.new('RGB', (cols*cellw, rows*cellh), (18,18,18))
dr = ImageDraw.Draw(img)
for i, (nib, xf, yf, tr) in enumerate(modes):
    ox = (i % cols)*cellw
    oy = (i // cols)*cellh
    dr.text((ox+2, oy+2), '%s xf%d yf%d tr%d' % (nib, xf, yf, tr),
            fill=(255,80,80))
    for y in range(8):
        for x in range(8):
            o = g*bpc + y*4 + x//2
            byte = d[o]
            if nib == 'hi':
                v = (byte >> 4) if x % 2 == 0 else (byte & 15)
            else:
                v = (byte & 15) if x % 2 == 0 else (byte >> 4)
            if not v:
                continue
            xx, yy = x, y
            if xf:
                xx = 7-xx
            if yf:
                yy = 7-yy
            if tr:
                xx, yy = yy, xx
            c = 40+v*14
            for sy in range(scale):
                for sx in range(scale):
                    img.putpixel((ox+xx*scale+sx, oy+16+yy*scale+sy),(c,c,c))
img.save('_work/review_fixes/glyph41_variants.png')
print('saved', len(modes))
