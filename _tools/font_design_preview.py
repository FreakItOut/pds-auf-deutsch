# -*- coding: utf-8 -*-
"""Baut Umlaut-/ss-Glyphen aus dem Original-Font und rendert eine Vorschau.

Aufruf: python font_design_preview.py <out.png> <variant>
"""
import sys

from PIL import Image

sys.stdout.reconfigure(encoding='latin1')
BASE = 0xC60
orig = open('_work/ascii_cgz/font_orig_real.raw', 'rb').read()


def get(code):
    o = BASE + (code - 0x20) * 64
    rows = []
    for r in range(16):
        rows.append([(b >> 4) if (i % 2 == 0) else (b & 15)
                     for i, b in enumerate(orig[o + r * 4:o + r * 4 + 4])
                     for _ in (0,)][:8])
    # rows: list of 8 nibbles
    return rows


def get2(code):
    o = BASE + (code - 0x20) * 64
    rows = []
    for r in range(16):
        vals = []
        for b in orig[o + r * 4:o + r * 4 + 4]:
            vals.append(b >> 4)
            vals.append(b & 15)
        rows.append(vals)
    return rows


def put(rows):
    out = bytearray()
    for r in rows:
        for i in range(0, 8, 2):
            out.append((r[i] << 4) | r[i + 1])
    return bytes(out)


def dot(rows, cols, style):
    """Setzt zwei Punkte ueber die angegebenen Spaltenpaare."""
    if style == 'A3':
        # 3 Zeilen, 4 Spalten je Punkt: Rand f, Kern 8
        for c0 in cols:
            for dx in (0, 1, 2, 3):
                pass
            rows[0][c0] = 0
            rows[0][c0 + 1] = 15
            rows[0][c0 + 2] = 15
            rows[0][c0 + 3] = 0
            rows[1][c0] = 15
            rows[1][c0 + 1] = 8
            rows[1][c0 + 2] = 8
            rows[1][c0 + 3] = 15
            rows[2][c0] = 0
            rows[2][c0 + 1] = 15
            rows[2][c0 + 2] = 15
            rows[2][c0 + 3] = 0
    elif style == 'A2':
        # 2 Zeilen (fuer Grossbuchstaben)
        for c0 in cols:
            rows[0][c0] = 0
            rows[0][c0 + 1] = 15
            rows[0][c0 + 2] = 15
            rows[0][c0 + 3] = 0
            rows[1][c0] = 15
            rows[1][c0 + 1] = 8
            rows[1][c0 + 2] = 8
            rows[1][c0 + 3] = 15
    elif style == 'B':
        # 2x2 voll, darunter Schatten
        for c0 in cols:
            rows[0][c0 + 1] = 8
            rows[0][c0 + 2] = 8
            rows[1][c0 + 1] = 8
            rows[1][c0 + 2] = 8
            rows[2][c0] = 0
            rows[2][c0 + 1] = 15
            rows[2][c0 + 2] = 15
            rows[2][c0 + 3] = 0
    elif style == 'C':
        for c0 in cols:
            rows[0][c0 + 1] = 8
            rows[0][c0 + 2] = 8
            rows[1][c0 + 1] = 8
            rows[1][c0 + 2] = 8


def condense(body, drop=2):
    """Entfernt <drop> Zeilen aus der Mitte (runde Striche)."""
    keep = body[:16 - drop]
    return keep


def build(variant):
    low_style = 'A3' if variant in ('A', 'B', 'C') else 'A3'
    up_style = 'A2'
    if variant == 'B':
        low_style = 'B'
    if variant == 'C':
        low_style = 'C'
    out = {}
    for code, base in ((0x5E, ord('a')), (0x7C, ord('o')), (0x7E, ord('u'))):
        g = get2(base)
        dot(g, [0, 4], low_style)
        out[code] = g
    for code, base in ((0x60, ord('A')), (0x5B, ord('O')), (0x5D, ord('U'))):
        g = get2(base)
        g = condense(g, 2)          # 14 Zeilen
        body = [[0] * 8 for _ in range(2)] + g   # rows 2..15
        body = body[:16]
        dot(body, [0, 4], up_style)
        out[code] = body
    return out


def render(glyphs, out, scale=8):
    codes = list(glyphs.keys())
    cw, ch = 8 * scale, 16 * scale
    img = Image.new('RGB', (len(codes) * cw + 10, ch), (40, 40, 40))
    px = img.load()
    for i, code in enumerate(codes):
        rows = glyphs[code]
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
    print('ok', out, [hex(c) for c in codes])


if __name__ == '__main__':
    out = sys.argv[1]
    variant = sys.argv[2] if len(sys.argv) > 2 else 'A'
    render(build(variant), out)
