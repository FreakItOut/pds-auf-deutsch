# tight-row histogram + summaries
import io
import re
import sys
sys.stdout.reconfigure(encoding='latin1')
rows = [l for l in io.open('_work/review_fixes/tight_rows.txt',
                           encoding='latin1') if l.strip()]
from collections import Counter
buckets = Counter()
exact = []
over = []
for r in rows:
    m = re.search(r'pct=(\d+)%', r)
    if m:
        p = int(m.group(1))
        buckets[p] += 1
        if p >= 100:
            exact.append(r)
        if p > 100:
            over.append(r)
print('rows scanned:', len(rows))
print('pct histogram (sorted desc):', sorted(buckets.items(), reverse=True))
print('rows >=100pc:', len(exact))
print('rows >100pc (over budget - BUG):', len(over))
for r in over[:20]:
    print('  OVER:', r[:200])
