# summarize broken_all.txt: group MM by stem+disc, list unique uid ranges
import io
import re
import sys

sys.stdout.reconfigure(encoding='latin1')


def summarize(uids):
    out = []
    start = prev = None
    for u in uids:
        if start is None:
            start = prev = u
        elif u == prev + 1:
            prev = u
        else:
            out.append('%d-%d' % (start, prev) if prev != start else str(start))
            start = prev = u
    if start is not None:
        out.append('%d-%d' % (start, prev) if prev != start else str(start))
    return ','.join(out)


txt = io.open('_work/review_fixes/broken_all.txt', encoding='latin1').read()
mm = re.findall(r"MM (\S+) d(\d) uid=(\d+) off=(\d+)", txt)
from collections import Counter
groups = Counter((s, d) for s, d, u, o in mm)
print('MM per stem/disc:')
for (s, d), n in sorted(groups.items()):
    uids = sorted(set(int(u) for s2, d2, u, o in mm if s2 == s and d2 == d))
    print('  %-14s d%d n=%4d uids: %s' % (s, int(d), n, summarize(uids)))
