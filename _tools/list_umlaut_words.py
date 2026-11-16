# -*- coding: utf-8 -*-
# Sammelt alle DE-Woerter mit ae/oe/ue/ss aus allen Textquellen.
import glob
import io
import re
import sys

sys.stdout.reconfigure(encoding='latin1')
texts = []
for p in glob.glob('_work/subtitles/*_de.csv'):
    for ln in io.open(p, encoding='latin1'):
        q = ln.rstrip('\r\n').split(';')
        if len(q) >= 6:
            texts.append(q[5])
for p in glob.glob('_work/menu_de/*_de.csv'):
    for ln in io.open(p, encoding='latin1'):
        q = ln.rstrip('\r\n').split(';')
        if len(q) >= 6:
            texts.append(q[5])
for ln in io.open('_work/evt_de_map.csv', encoding='latin1'):
    q = ln.rstrip('\r\n').split(';')
    if len(q) >= 2:
        texts.append(q[1])

words = {}
for t in texts:
    for w in re.findall(r"[A-Za-zÄÖÜäöüß']+", t):
        lw = w.lower()
        if 'ae' in lw or 'oe' in lw or 'ue' in lw or 'ss' in lw:
            words[w] = words.get(w, 0) + 1
for w, n in sorted(words.items(), key=lambda kv: (-kv[1], kv[0])):
    print('%4d %s' % (n, w))
print('unique:', len(words))
