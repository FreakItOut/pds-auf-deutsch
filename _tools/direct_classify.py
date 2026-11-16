# direct classification for TWN subtitle rows (no double counting)
import glob
import io
import os
import re
import sys
sys.stdout.reconfigure(encoding='latin1')

tot = 0; empty = 0; diff = 0; ident = 0; identList = []
for path in sorted(glob.glob('_work/subtitles/TWN_*_de.csv')):
    base = os.path.basename(path)[:-7]
    if base.startswith('TWN_E128'):
        continue
    for ln in io.open(path, encoding='latin1'):
        q = ln.rstrip('\r\n').split(';')
        if len(q) < 6 or not q[0].isdigit():
            continue
        en, de = q[4], q[5]
        if not en or not en.strip() or len(en.strip()) < 3:
            continue
        tot += 1
        if not de.strip():
            empty += 1
        elif de.strip() == en.strip():
            ident += 1
            identList.append((base, int(q[0]), en))
        else:
            diff += 1
print('rows:', tot, 'empty:', empty, 'diff:', diff, 'ident:', ident)
for x in identList:
    print('  ', x)
