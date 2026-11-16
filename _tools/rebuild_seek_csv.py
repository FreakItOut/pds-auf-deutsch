# -*- coding: utf-8 -*-
# Rekonstruiert _work/subtitles/TWN_SEEK_PRG_de.csv aus EN-Liste + gepatchtem PRG.
import io
import sys

sys.stdout.reconfigure(encoding='latin1')
EN = '_work/subtitles/TWN_SEEK_PRG_en.csv'
PRG = '_work/seek_current.prg'
d = open(PRG, 'rb').read()


def read_str(o):
    e = o
    while e < len(d) and d[e] not in (0, 255):
        e += 1
    return d[o:e].decode('latin1')


rows = []
for line in io.open(EN, encoding='latin1'):
    p = line.rstrip('\r\n').split(';')
    if len(p) < 5:
        continue
    uid, ln, first, copies, en = p[0], p[1], p[2], p[3], p[4]
    offs = [int(x) for x in copies.split('|') if x]
    texts = [(o, read_str(o)) for o in offs]
    # bevorzuge nicht-englische Texte; dann haeufigste Variante
    cand = [t for o, t in texts if t and t != en]
    if not cand:
        cand = [t for o, t in texts if t]
    if cand:
        de = max(set(cand), key=cand.count)
        use = [o for o, t in texts if t == de]
    else:
        de = en
        use = offs
    rows.append((uid, ln, str(use[0]), '|'.join(str(o) for o in use),
                 en, de))
out = io.open('_work/subtitles/TWN_SEEK_PRG_de.csv', 'w',
              encoding='latin1', newline='\n')
for r in rows:
    out.write(';'.join(r) + '\n')
out.close()
print('rows=%d' % len(rows))
for r in rows[:10]:
    print(' | '.join(r[:6]))
