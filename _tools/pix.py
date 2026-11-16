# -*- coding: utf-8 -*-
import sys

from PIL import Image

sys.stdout.reconfigure(encoding='latin1')
a = sys.argv[1:]
img = Image.open(a[0]).convert('L')
if a[1] == 'map':
    x, y, w, h = map(int, a[2:6])
    chars = ' .:-=+*#%@'
    for yy in range(y, y + h):
        line = ''
        for xx in range(x, x + w):
            v = img.getpixel((xx, yy))
            i = min(9, v // 26)
            line += chars[i]
        print(line)
else:
    x, y, w, h, s = map(int, a[2:7])
    crop = img.crop((x, y, x + w, y + h)).resize((w * s, h * s), Image.NEAREST)
    crop.save(a[7])
    print('ok', a[7], img.size)
