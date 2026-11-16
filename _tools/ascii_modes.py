# -*- coding: utf-8 -*-
# Testet Rotation/Transposition der 8x8-Glyphen (glyph 0x20..0x5F).
import sys

from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding='latin1')
d = open('_work/ascii_cgz/vram_pds_0.raw', 'rb').read()
bpc = 32


def pix(g, x, y):
    o = g * bpc
    byte = d[o + y * 4 + x // 2]
    return (byte >> 4) if x % 2 == 0 else (byte & 15)


def glyph(g, mode):
    out = Image.new('L', (8, 8), 0)
    for y in range(8):
        for x in range(8):
            v = pix(g, x, y)
            if mode == 'rot90':
                xx, yy = y, 7 - x
            elif mode == 'rot270':
                xx, yy = 7 - y, x
            elif mode == 'rot180':
                xx, yy = 7 - x, 7 - y
            elif mode == 'transp':
                xx, yy = y, x
            else:
                xx, yy = x, y
            out.putpixel((xx, yy), min(255, v * 17))
    return out


modes = ('orig', 'rot90', 'rot270', 'transp')
start = 0x20
n = 64
scale = 3
lab = 12
cols = 16
rows = (n + cols - 1) // cols
W = len(modes) * cols * (8 * scale + 2)
H = rows * (8 * scale + lab)
img = Image.new('RGB', (W, H), (18, 18, 18))
dr = ImageDraw.Draw(img)
for g in range(start, start + n):
    k = g - start
    col = k % cols
    row = k // cols
    for mi, mode in enumerate(modes):
        gl = glyph(g, mode)
        ox = mi * cols * (8 * scale + 2) + col * (8 * scale + 2)
        oy = row * (8 * scale + lab)
        dr.text((ox, oy), '%02x' % g, fill=(255, 80, 80))
        for y in range(8):
            for x in range(8):
                v = gl.getpixel((x, y))
                if v:
                    for sy in range(scale):
                        for sx in range(scale):
                            img.putpixel((ox + x * scale + sx,
                                          oy + lab + y * scale + sy),
                                         (v, v, v))
img.save('_work/review_fixes/ascii_modes.png')
print('saved')
