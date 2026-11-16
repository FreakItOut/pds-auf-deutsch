# -*- coding: utf-8 -*-
import collections
import io
import sys

sys.stdout.reconfigure(encoding='latin1')
rows = []
for ln in io.open('_work/review_fixes/english_candidates.txt',
                  encoding='latin1'):
    p = ln.rstrip('\n').split(';', 3)
    if len(p) == 4:
        rows.append(p)
by_text = collections.defaultdict(list)
for d, name, off, t in rows:
    by_text[t].append((d, name, off))
print('lines', len(rows), 'unique texts', len(by_text))
for t, locs in sorted(by_text.items(), key=lambda kv: (-len(kv[1]), kv[0]))[:80]:
    files = sorted(set('%s' % x[1] for x in locs))
    print('%3d | %-40s | %s' % (len(locs), t[:40], ','.join(files)[:60]))
