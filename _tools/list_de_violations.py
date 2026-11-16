import csv
import glob
import os
import sys

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

name = sys.argv[1] if len(sys.argv) > 1 else 'FLD_A5_MCB'
NL = chr(10)
BSN = chr(92) + 'n'


def unesc(s):
    return s.replace(BSN, NL)


seen = {}
for path in sorted(glob.glob(f'_work/menu_de/{name}_de*.csv')):
    rd = csv.reader(open(path, encoding='latin1'), delimiter=';')
    next(rd)
    for r in rd:
        if len(r) < 6:
            continue
        en, de = unesc(r[4]), unesc(r[5])
        if len(de.encode('latin1')) > len(en.encode('latin1')):
            key = (r[4], r[5])
            if key not in seen:
                seen[key] = (len(en.encode('latin1')),
                             len(de.encode('latin1')))
print('unique violations:', len(seen))
for (en, de), (le, ld) in sorted(seen.items()):
    print('%d/%d|%s|%s' % (ld, le, en.replace(';', ','), de.replace(';', ',')))
