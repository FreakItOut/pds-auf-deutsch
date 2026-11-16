# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw

d = open('_work/ascii_cgz/font_de.raw', 'rb').read()
text = 'Die ]berlebenden leben in'
scale = 4
img = Image.new('RGB', (len(text) * 8 * scale + 20, 16 * scale + 20),
                (0, 0, 0))
dr = ImageDraw.Draw(img)
x0 = 10
for i, ch in enumerate(text):
    base = 0xC60 + (ord(ch) - 0x20) * 64
    if base + 64 > len(d):
        continue
    for y in range(16):
        for x in range(8):
            b = d[base + y * 4 + x // 2]
            v = (b >> 4) if x % 2 == 0 else (b & 15)
            if v:
                c = 20 + v * 15
                ox = x0 + i * 8 * scale + x * scale
                oy = 10 + y * scale
                dr.rectangle([ox, oy, ox + scale - 1, oy + scale - 1],
                             fill=(c, c, c))
img.save('_work/review_fixes/font_render_text.png')
print('ok')
