# Dump chains for E128_cd3
import io
import re
import sys

sys.stdout.reconfigure(encoding='latin1')
TERM = re.compile(r'[.!?)]\s*$')
stem = 'TWN_E128_cd3'
rows = []
for ln in io.open('_work/subtitles/%s_de.csv' % stem, encoding='latin1'):
    q = ln.rstrip('\r\n').split(';')
    if len(q) >= 6 and q[0].isdigit():
        rows.append({'uid': int(q[0]), 'en': q[4], 'de': q[5]})

out = io.open('_work/review_fixes/e128_chains.txt', 'w',
              encoding='ascii', errors='backslashreplace', newline='\n')
cur = []


def flush(c):
    lo, hi = c[0]['uid'], c[-1]['uid']
    out.write('%d-%d\n' % (lo, hi))
    out.write('  EN: ' + ' / '.join(x['en'].strip() for x in c) + '\n')
    out.write('  DE: ' + ' / '.join(x['de'].strip() for x in c) + '\n')


for r in rows:
    cur.append(r)
    if TERM.search(r['en'].rstrip()) or len(cur) >= 5:
        flush(cur)
        cur = []
if cur:
    flush(cur)
out.close()
print('rows=%d' % len(rows))
