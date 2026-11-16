# Sync EN keys in DE part files with the exact EN csv (matched by offset),
# and report max EN line width + list of DE strings needing rewrap.
import csv
import os
import sys

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def unesc(s):
    return s.replace('\\n', '\n')


def esc(s):
    return s.replace('\n', '\\n')


name = sys.argv[1] if len(sys.argv) > 1 else 'MENU_SCB'
enrows = {}
with open(f'_work/menu_de/{name}_en.csv', encoding='latin1') as fh:
    rd = csv.reader(fh, delimiter=';')
    next(rd)
    for r in rd:
        enrows[int(r[1])] = r[4]

maxw = max(len(l) for t in enrows.values() for l in unesc(t).split('\n'))
print('max EN line width in %s: %d' % (name, maxw))

import glob
for path in sorted(glob.glob(f'_work/menu_de/{name}_de*.csv')):
    lines = open(path, encoding='latin1').read().splitlines()
    out = []
    fixed = 0
    for ln in lines:
        parts = ln.split(';')
        if len(parts) >= 6 and parts[0] == name.replace('_', '.'):
            off = int(parts[1])
            if off in enrows and parts[4] != enrows[off]:
                parts[4] = enrows[off]
                fixed += 1
                ln = ';'.join(parts)
        out.append(ln)
    open(path, 'w', encoding='latin1', newline='').write('\n'.join(out) + '\n')
    print('%s: synced %d EN keys' % (os.path.basename(path), fixed))

# rewrap report
print()
print('=== DE strings with lines > %d (need rewrap) ===' % maxw)
for path in sorted(glob.glob(f'_work/menu_de/{name}_de*.csv')):
    rd = csv.reader(open(path, encoding='latin1'), delimiter=';')
    next(rd)
    for r in rd:
        if len(r) < 6:
            continue
        off = int(r[1])
        de = unesc(r[5])
        bad = [l for l in de.split('\n') if len(l) > maxw]
        if bad:
            print('off=%d max=%d' % (off, max(len(l) for l in bad)))
            print('  EN: %r' % r[4])
            print('  DE: %r' % r[5])
