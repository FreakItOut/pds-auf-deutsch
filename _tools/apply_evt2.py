# Write fix_evt2.FIX into _work/evt_de_map.csv by line index.
import io
import sys

import fix_evt2

path = '_work/evt_de_map.csv'
lines = io.open(path, encoding='latin1').read().split('\n')
row = -1
done = 0
for i, ln in enumerate(lines):
    body = ln.rstrip('\r\n')
    if not body or body.startswith('#') or ';' not in body:
        continue
    row += 1
    if row in fix_evt2.FIX:
        en = body.split(';', 1)[0]
        lines[i] = en + ';' + fix_evt2.FIX[row]
        done += 1
io.open(path, 'w', encoding='latin1', newline='').write('\n'.join(lines))
print('synced %d/%d' % (done, len(fix_evt2.FIX)))
