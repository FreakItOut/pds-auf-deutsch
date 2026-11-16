# Sync fix_e128d.FIX into the E128 uid CSV.
import io
import sys

import fix_e128d

p = '_work/subtitles/TWN_E128_cd3_de.csv'
lines = io.open(p, encoding='latin1').read().split('\n')
done = set()
for i, ln in enumerate(lines):
    q = ln.rstrip('\r\n').split(';')
    if len(q) >= 6 and q[0].isdigit():
        uid = int(q[0])
        if uid in fix_e128d.FIX:
            q[5] = fix_e128d.FIX[uid]
            lines[i] = ';'.join(q)
            done.add(uid)
io.open(p, 'w', encoding='latin1', newline='').write('\n'.join(lines))
print('synced %d/%d' % (len(done), len(fix_e128d.FIX)))
