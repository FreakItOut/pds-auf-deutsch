# -*- coding: utf-8 -*-
import sys

from PIL import Image

sys.stdout.reconfigure(encoding='latin1')
img = Image.open(sys.argv[1]).convert('RGB')
w, h = img.size
minx, miny, maxx, maxy = w, h, -1, -1
for y in range(0, h):
    for x in range(0, w):
        r, g, b = img.getpixel((x, y))
        if r > 170 and g > 170 and b < 120:
            minx = min(minx, x); maxx = max(maxx, x)
            miny = min(miny, y); maxy = max(maxy, y)
print('yellow bbox', minx, miny, maxx, maxy)
