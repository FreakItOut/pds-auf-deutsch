# -*- coding: utf-8 -*-
# Glyph 0x21 als 16x16 1bpp in verschiedenen Zellanordnungen.
import sys

from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding='latin1')
d = open('_work/ascii_cgz/vram_pds_0.raw','rb').read()
idx = 0x21
bpc = 32
o = idx*bpc
scale = 14
modes = ('rows', 'cells', 'rows_col', 'cells_col')
img = Image.new('RGB', (len(modes)*(16*scale+10), 16*scale+20), (18,18,18))
dr = ImageDraw.Draw(img)
for mi, mode in enumerate(modes):
    ox = mi*(16*scale+10)
    dr.text((ox+2, 2), mode, fill=(255,80,80))
    for y in range(16):
        for x in range(16):
            if mode == 'rows':
                word = (d[o+y*2] << 8) | d[o+y*2+1]
                bit = (word >> (15-x)) & 1
            elif mode == 'rows_col':
                word = (d[o+y*2] << 8) | d[o+y*2+1]
                bit = (word >> x) & 1
            elif mode == 'cells':
                q = (y//8)*2 + (x//8)
                b = d[o+q*8+(y % 8)]
                bit = (b >> (7-(x % 8))) & 1
            else:
                q = (y//8)*2 + (x//8)
                b = d[o+q*8+(x % 8)]
                bit = (b >> (7-(y % 8))) & 1
            if bit:
                c = 235
                for sy in range(scale):
                    for sx in range(scale):
                        img.putpixel((ox+x*scale+sx, 18+y*scale+sy),(c,c,c))
img.save('_work/review_fixes/glyph16_modes.png')
print('saved')
