# Report adjacent rows with identical DE but different EN (possible shift).
import io
import sys

sys.stdout.reconfigure(encoding='latin1')
STEMS = ['TWN_E022_PRG', 'TWN_JIRI_PRG', 'TWN_CAMP_PRG', 'TWN_RUIN_PRG',
         'TWN_SEEK_PRG']

for stem in STEMS:
    rows = []
    for ln in io.open('_work/subtitles/%s_de.csv' % stem, encoding='latin1'):
        q = ln.rstrip('\r\n').split(';')
        if len(q) >= 6 and q[0].isdigit():
            rows.append((int(q[0]), q[4], q[5]))
    print('=== %s ===' % stem)
    for i in range(len(rows) - 1):
        u1, e1, d1 = rows[i]
        u2, e2, d2 = rows[i + 1]
        if d1.strip() and d1 == d2 and e1.strip() != e2.strip():
            print('DUP %d/%d  DE=%r' % (u1, u2, d1))
            print('    EN1=%r' % e1)
            print('    EN2=%r' % e2)
