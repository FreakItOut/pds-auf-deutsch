# find the FLD_* mismatch cause: duplicate offs with differing de values
import glob
import io
import sys
sys.stdout.reconfigure(encoding='latin1')

import csv as c2
for tool in ('FLD_A3_MCB', 'FLD_A5_MCB', 'FLD_B6_MCB', 'FLD_C4_6_MCB'):
    rows = {}
    for path in sorted(glob.glob('_work/menu_de/%s_de*.csv' % tool)):
        rd = c2.reader(io.open(path, encoding='latin1'), delimiter=';')
        header = next(rd, None)
        for r in rd:
            if len(r) < 6:
                continue
            off = int(r[1])
            if r[-1] == '1':
                continue  # ignore force rows
            rows.setdefault(off, []).append((path.split('\\')[-1], r[4], r[5], r[2]))
    dups = {o: v for o, v in rows.items() if len(v) > 1 and len(set(x[2] for x in v)) > 1}
    print('=====', tool, 'dups', len(dups))
    for o, v in list(dups.items())[:10]:
        print(' off', o, v)
