# -*- coding: utf-8 -*-
"""Erstellt einen Kontaktabzug der Untertitelbaender aller Treffer."""
import glob
import os
import sys

from PIL import Image

sys.stdout.reconfigure(encoding='latin1')
d = sys.argv[1]
out = sys.argv[2]
files = sorted(glob.glob(os.path.join(d, 'hit_*.jpg')))
if not files:
    print('keine Dateien')
    raise SystemExit(1)
crops = []
for f in files:
    img = Image.open(f).convert('RGB')
    w, h = img.size
    y0, y1 = int(h * 0.855), int(h * 0.945)
    c = img.crop((0, y0, w, y1))
    crops.append((os.path.basename(f), c))
cw = crops[0][1].width
ch = crops[0][1].height
img = Image.new('RGB', (cw, ch * len(crops)), (20, 20, 20))
for i, (name, c) in enumerate(crops):
    img.paste(c, (0, i * ch))
img.save(out)
print('ok', out, img.size, 'n=', len(crops))
