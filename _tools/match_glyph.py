# -*- coding: utf-8 -*-
import glob
import sys

sys.stdout.reconfigure(encoding='latin1')
# grobe 8x8-Vorlage fuer 'G' aus dem Untertitel
T = [
    '..####..',
    '.##..##.',
    '.##.....',
    '.##.....',
    '.##.###.',
    '.##..##.',
    '.##..##.',
    '..####..',
]
tm = [[1 if c == '#' else 0 for c in row] for row in T]


def score(g, w=8, h=8, bpr=4):
    s = 0
    for y in range(h):
        for x in range(w):
            b = g[y * bpr + x // 2]
            v = (b >> 4) if x % 2 == 0 else (b & 15)
            if (1 if v else 0) == tm[y][x]:
                s += 1
    return s


for f in sorted(glob.glob('_work/review_fixes/sub2font_*.bin')):
    d = open(f, 'rb').read()
    best = []
    for off in range(0, len(d) - 32, 4):
        sc = score(d[off:off + 32])
        if sc >= 60:
            best.append((sc, off))
    best.sort(reverse=True)
    print(f.split('\\')[-1], 'hits', len(best), best[:6])
