# -*- coding: utf-8 -*-
import collections
import glob
import io
import sys

sys.stdout.reconfigure(encoding='latin1')
cnt = collections.Counter()
rows = 0
for p in glob.glob('_work/subtitles/*_de.csv') + glob.glob('_work/menu_de/*_de.csv'):
    for ln in io.open(p, encoding='latin1'):
        q = ln.rstrip('\r\n').split(';')
        if len(q) >= 6:
            de = q[5]
            rows += 1
            for ch in de:
                cnt[ch] += 1
print('rows', rows)
for ch in ['^', '`', '~', '|', '{', '}', '[', ']', chr(92)]:
    print('%r %d' % (ch, cnt.get(ch, 0)))
print('nonascii', {c: n for c, n in cnt.items() if ord(c) > 126})
