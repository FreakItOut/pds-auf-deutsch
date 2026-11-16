# -*- coding: utf-8 -*-
# Erzeugt _tools/assets/pds_logo.ico (+ _64/_32/_16 PNGs) aus der
# Logo-Sporn (assets/logo_roh_0.jpg).
# Emblem = Adlerkopf + FREAKITOUT-Banner, zentriert auf dunklem
# Grund, Ecken abgerundet.  Einfach idempotent lauffbar.
import os
from PIL import Image, ImageDraw, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'assets', 'logo_roh_0.jpg')
OUTDIR = os.path.join(HERE, 'assets')

im = Image.open(SRC).convert('RGB')
w, h = im.size
# Ausschnitt: Adler + Banner (Fractions des Originals)
box = (int(0.085 * w), int(0.175 * h), int(0.930 * w), int(0.870 * h))
emblem = im.crop(box)

# Quadratische Buehne mit Rand
epw, eph = emblem.size
side = int(max(epw, eph) * 1.10)
canvas = Image.new('RGB', (side, side), (0x1a, 0x1a, 0x1a))
canvas.paste(emblem, ((side - epw) // 2, (side - eph) // 2))

# Master 256 + abgerundete Ecken (RGBA)
master = canvas.resize((256, 256), Image.LANCZOS).convert('RGBA')
radius = 42
mask = Image.new('L', (256, 256), 0)
d = ImageDraw.Draw(mask)
d.rounded_rectangle([0, 0, 255, 255], radius=radius, fill=255)
master.putalpha(mask)

ico = os.path.join(OUTDIR, 'pds_logo.ico')
master.save(ico, format='ICO',
            sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64),
                   (128, 128), (256, 256)])
for s in (64, 32, 16):
    master.resize((s, s), Image.LANCZOS).save(
        os.path.join(OUTDIR, 'pds_logo_%d.png' % s))
print('ok:', ico, os.path.getsize(ico))
