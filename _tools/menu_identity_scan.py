# menu identity rows: EN==DE; filter real prose / labels worth German
import csv
import glob
import io
import os
import re
import sys
sys.stdout.reconfigure(encoding='latin1')

SKIPNESS = re.compile(r'^[A-Z0-9_ %\-,:;.!?]+$')

suspects = []
tot_ident = 0
for path in sorted(glob.glob('_work/menu_de/*_de*.csv')):
    base = os.path.basename(path)
    if base.endswith('_en.csv'):
        continue
    f = io.open(path, encoding='latin1')
    rd = csv.reader(f, delimiter=';')
    header = next(rd, None)
    if not header or header[0] != 'file':
        f.close()
        f = io.open(path, encoding='latin1')
        rd = csv.reader(f, delimiter=';')
    for r in rd:
        if len(r) < 6:
            continue
        en, de = r[4], r[5]
        if not en or not en.strip() or len(en.strip()) < 3:
            continue
        if de.strip() != en.strip():
            continue
        tot_ident += 1
        # skip debug/format/all-caps label patterns
        if SKIPNESS.match(en) or re.match(r'^[%\dA-Z_.:\-]{4,}$', en):
            continue
        # skip known name families and short lowercase labels (camp1 etc.)
        if re.match(r'^[a-z0-9_]+$', en):
            continue
        # skip PCM/track markers
        if re.search(r'\.PCM|_PCM|T_[A-Z]{2}_', en):
            continue
        # skip obvious identical words and pure numbers
        if en.strip().lower() in ('laser', 'items', 'level up', 'yes', 'no',
                                  'caution!! no encout data !!',
                                  'caution!! no result data !!'):
            continue
        suspects.append((base, r[1], en))
print('menu identity total:', tot_ident)
print('suspects:', len(suspects))
for x in suspects[:80]:
    print(' ', x)
with open('_work/review_fixes/menu_identity_suspects.txt', 'w',
          encoding='latin1', newline='\n') as f:
    f.write('file;off;en\n')
    for base, off, en in suspects:
        f.write('%s;%s;%s\n' % (base, off, en))
print('written _work/review_fixes/menu_identity_suspects.txt')
