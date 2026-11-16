# -*- coding: utf-8 -*-
"""Baut den deutschen Font (Umlaute + ss) aus dem Original-ASCII.CGZ.

Ergebnis: _work/ascii_cgz/font_de.raw  (19648 Bytes, 8x16-Tabelle ab 0xC60)

Wichtig: Im Font ist 0xF die schwarze Kontur, 0x8 die hellste Fuellung.
Frueher wurden die Umlautpunkte mit 0xF gezeichnet -> im Spiel unsichtbar.
"""
import sys

from PIL import Image

sys.stdout.reconfigure(encoding='latin1')
BASE = 0xC60
ORIG = '_work/ascii_cgz/font_orig_real.raw'
OUT = '_work/ascii_cgz/font_de.raw'
FILL = 8          # hellste Fuellung
OUTLINE = 15      # schwarz

SLOT_A = 0x5E
SLOT_O = 0x7C
SLOT_U = 0x7E
SLOT_AE = 0x60
SLOT_OE = 0x5B
SLOT_UE = 0x5D
SLOT_SS = 0x7B


def get(data, code):
    o = BASE + (code - 0x20) * 64
    rows = []
    for r in range(16):
        vals = []
        for b in data[o + r * 4:o + r * 4 + 4]:
            vals.append(b >> 4)
            vals.append(b & 15)
        rows.append(vals)
    return rows


def put(data, code, rows):
    o = BASE + (code - 0x20) * 64
    out = bytearray()
    for r in rows:
        for i in range(0, 8, 2):
            out.append((r[i] << 4) | r[i + 1])
    data[o:o + 64] = out


def dots(rows, col1, col2, top=0):
    """Zwei 2x2-Punkte (Fuellfarbe) in den Zeilen top/top+1."""
    for c0 in (col1, col2):
        rows[top][c0] = FILL
        rows[top][c0 + 1] = FILL
        rows[top + 1][c0] = FILL
        rows[top + 1][c0 + 1] = FILL


def condense(rows, drop_at):
    return rows[:drop_at] + rows[drop_at + 2:]


def build():
    d = bytearray(open(ORIG, 'rb').read())

    # --- Kleinbuchstaben: Grundzeichen + Punkte in Zeile 0/1 ---
    for slot, base in ((SLOT_A, ord('a')), (SLOT_O, ord('o')),
                       (SLOT_U, ord('u'))):
        g = get(d, base)
        dots(g, 1, 4, 0)
        put(d, slot, g)

    # --- Grossbuchstaben: Koerper um 2 Zeilen kuerzen, dann Punkte ---
    for slot, base, drop_at, col1, col2 in (
            (SLOT_AE, ord('A'), 11, 1, 5),
            (SLOT_OE, ord('O'), 7, 1, 5),
            (SLOT_UE, ord('U'), 7, 1, 5)):
        g = condense(get(d, base), drop_at)     # 14 Zeilen
        g = [[0] * 8 for _ in range(2)] + g     # Zeilen 2..15
        dots(g, col1, col2, 0)
        put(d, slot, g)

    # --- ss: B-Koerper (Zeilen 2..15) mit hohem Stamm ---
    b = get(d, ord('B'))
    g = [list(r) for r in b[2:16]]          # 14 Zeilen = Zeilen 2..15
    g = [[0] * 8, [0] * 8] + g
    # Stamm ueber dem Koerper (Zeilen 0/1), an B-Stamm (Spalten 0..3)
    g[0] = [0, OUTLINE, FILL, OUTLINE, 0, 0, 0, 0]
    g[1] = [OUTLINE, FILL, FILL, OUTLINE, 0, 0, 0, 0]
    put(d, SLOT_SS, g)

    return d


def render(data, out, scale=8):
    codes = [SLOT_A, SLOT_O, SLOT_U, SLOT_AE, SLOT_OE, SLOT_UE, SLOT_SS,
             ord('a'), ord('o'), ord('u'), ord('A'), ord('O'), ord('U')]
    gap = 6 * scale
    cw, ch = 8 * scale + gap, 16 * scale
    img = Image.new('RGB', (len(codes) * cw + 10, ch), (40, 40, 40))
    px = img.load()
    for i, code in enumerate(codes):
        rows = get(data, code)
        gx = i * cw + 10
        for r in range(16):
            for c in range(8):
                v = rows[r][c]
                if v == 0:
                    rgb = (40, 40, 40)
                elif v == 15:
                    rgb = (0, 0, 0)
                else:
                    g = max(30, min(255, (15 - v) * 36))
                    rgb = (g, g, g)
                for yy in range(scale):
                    for xx in range(scale):
                        px[gx + c * scale + xx, r * scale + yy] = rgb
    img.save(out)
    print('preview', out)


if __name__ == '__main__':
    data = build()
    open(OUT, 'wb').write(bytes(data))
    print('geschrieben', OUT, len(data))
    render(data, '_work/review_fixes/design_final.png')
