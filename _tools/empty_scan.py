# scan all TWN subtitle csvs for remaining EMPTY de rows; count + sample
import glob
import io
import os
import re
import sys
sys.stdout.reconfigure(encoding='latin1')

rows = {}
for path in sorted(glob.glob('_work/subtitles/TWN_*_de.csv')):
    base = os.path.basename(path)[:-7]
    if base.startswith('TWN_E128'):
        continue
    for i, ln in enumerate(io.open(path, encoding='latin1'), 1):
        q = ln.rstrip('\r\n').split(';')
        if len(q) < 6 or q[0] not in ('0', '1', '2', '3', '4', '5', '6', '7',
                                      '8', '9', '10', '11') and not q[0].isdigit():
            if len(q) < 6 or not q[0].isdigit():
                continue
        uid = q[0]
        if not q[0].isdigit():
            continue
        uid = int(q[0])
        en, de = q[4], q[5]
        if not en.strip() or not de.strip():
            rows.setdefault((base, uid), (q[2], q[4], q[5]))
empty_by_file = {}
for (base, uid), (off, en, de) in rows.items():
    empty_by_file.setdefault(base, []).append((uid, off, en))
print('files with EMPTY de rows:')
for base, lst in sorted(empty_by_file.items()):
    print(' ', base, len(lst))
total = sum(len(v) for v in empty_by_file.values())
print('total empty:', total)
# sample collected
with open('_work/review_fixes/twn_empty_list.txt', 'w', encoding='latin1',
          newline='\n') as f:
    for base, lst in sorted(empty_by_file.items()):
        for uid, off, en in lst:
            f.write('%s;%s;%s;%s\n' % (base, uid, off, en))
print('written _work/review_fixes/twn_empty_list.txt')
