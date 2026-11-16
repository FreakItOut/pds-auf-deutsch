# coverage: menu group counting fix (map rows + expanded subtitle maps)
import csv
import glob
import io
import os
import re
import sys
sys.stdout.reconfigure(encoding='latin1')

de_refs = {}
tot = tr = ok = ident = 0
for path in sorted(glob.glob('_work/menu_de/*_de*.csv')):
    base = os.path.basename(path)
    if base.endswith('_en.csv'):
        continue
    f = io.open(path, encoding='latin1')
    rd = csv.reader(f, delimiter=';')
    header = next(rd, None)
    if header and header and header[0] == 'file':
        for r in rd:
            if len(r) < 6:
                continue
            en, de = r[4], r[5]
            if not en or not en.strip() or len(en.strip()) < 4:
                continue
            if '%' in en[:3] and len(en.strip()) < 14:
                continue
            tot += 1
            if re.match(r'^[A-Z0-9_ \-]{4,}$', en):
                continue
            tr += 1
            if de.strip() and de.strip() != en.strip():
                ok += 1
            elif de.strip() == en.strip():
                ident += 1
    else:
        f.close()
        continue
    f.close()

print('menu group total=%d translatable=%d german=%d identity=%d'
      % (tot, tr, ok, ident))
