# -*- coding: utf-8 -*-
# Erzeugt Umlaut-Glyphen im ASCII.CGZ-Font (8x16, 4bpp, 64 B/Zeichen).
import sys

from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding='latin1')
SRC = '_work/ascii_cgz/vram_pds_0.raw'
BASE = 0xC60
SLOTS = {'ä': 0x5E, 'ö': 0x7C, 'ü': 0x7E, 'ß': 0x7B,
         'Ä': 0x60, 'Ö': 0x5B, 'Ü': 0x5D}


def get(d, ch):
    o = BASE + (ord(ch)-0x20)*64
    return bytearray(d[o:o+64])


def setpx(g, x, y, v):
    idx = y*4 + x//2
    if x % 2 == 0:
        g[idx] = (g[idx] & 0x0F) | (v << 4)
    else:
        g[idx] = (g[idx] & 0xF0) | v


def getpx(g, x, y):
    b = g[y*4 + x//2]
    return (b >> 4) if x % 2 == 0 else (b & 15)


def add_dots(g, positions):
    """Setzt zwei 2x2-Punkte (Kern 15)."""
    for cx, cy in positions:
        for dx in range(2):
            for dy in range(2):
                setpx(g, cx+dx, cy+dy, 15)


def make_ss():
    """Handgezeichnetes scharfes S (8x16)."""
    g = bytearray(64)
    # Maske 8x16, Stil: links Stem, oben Bogen, Mitte Schleife
    rows = [
        '..####..',
        '.##..##.',
        '.##..##.',
        '.##.##..',
        '.####...',
        '.##.##..',
        '.##..##.',
        '.##..##.',
        '.##..##.',
        '.##..##.',
        '.##..##.',
        '.##..##.',
        '.##..##.',
        '.##.##..',
        '.####...',
        '.##.....',
    ]
    for y, r in enumerate(rows):
        for x, c in enumerate(r):
            if c == '#':
                setpx(g, x, y, 15)
    # weiche Kanten
    for y, r in enumerate(rows):
        for x, c in enumerate(r):
            if c == '#' and (x == 0 or x == 7 or y == 0 or y == 15):
                setpx(g, x, y, 12)
    return g


def make_upper(d, base_char):
    """Grossbuchstabe mit Umlautpunkten: 2 Zeilen kuerzer, Punkte oben."""
    src = get(d, base_char)
    g = bytearray(64)
    for y in range(14):
        sy = int(round(y * 15.0 / 13.0))
        if sy > 15:
            sy = 15
        for x in range(8):
            setpx(g, x, y + 2, getpx(src, x, sy))
    add_dots(g, [(1, 0), (5, 0)])
    return g


def main():
    d = bytearray(open(SRC, 'rb').read())
    out = {}
    for ch, base in (('ä', 'a'), ('ö', 'o'), ('ü', 'u')):
        g = get(d, base)
        add_dots(g, [(1, 0), (5, 0)])
        out[ch] = bytes(g)
    out['ß'] = bytes(make_ss())
    for ch, base in (('Ä', 'A'), ('Ö', 'O'), ('Ü', 'U')):
        out[ch] = bytes(make_upper(d, base))
    for ch, slot in SLOTS.items():
        o = BASE + (slot-0x20)*64
        d[o:o+64] = out[ch]
    open('_work/ascii_cgz/font_de.raw', 'wb').write(d)
    # Vorschau
    chars = ['a', 'ä', 'A', 'Ä', 'o', 'ö', 'O', 'Ö',
             'u', 'ü', 'U', 'Ü', 's', 'ß', '^', '|', '~', '{', '`', '[', ']']
    scale = 8
    img = Image.new('RGB', (len(chars)*(8*scale+8), 16*scale+20),
                    (0, 0, 0))
    dr = ImageDraw.Draw(img)
    for i, ch in enumerate(chars):
        o = BASE + (ord(ch)-0x20)*64
        ox = i*(8*scale+8)
        dr.text((ox+2, 2), ch, fill=(255, 80, 80))
        for y in range(16):
            for x in range(8):
                idx = o+y*4+x//2
                b = d[idx]
                v = (b >> 4) if x % 2 == 0 else (b & 15)
                if v:
                    c = 20+v*15
                    for sy in range(scale):
                        for sx in range(scale):
                            img.putpixel((ox+x*scale+sx, 18+y*scale+sy),
                                         (c, c, c))
    img.save('_work/review_fixes/umlaut_preview.png')
    print('saved preview')


if __name__ == '__main__':
    main()
