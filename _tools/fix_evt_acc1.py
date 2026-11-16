# -*- coding: utf-8 -*-
# Acc1: zwei FMV-Zeilen praeziser formulieren, Karte + Discs neu.
import io
import subprocess
import sys

sys.stdout.reconfigure(encoding='latin1')
MAP = '_work/evt_de_map.csv'
FIX = {
    'Retreat to the second defense line.': 'Rueckzug zur zweiten Linie.',
    "but we'll have another chance.": 'doch es gibt noch eine Chance.',
}

lines = io.open(MAP, encoding='latin1').read().split('\n')
count = {k: 0 for k in FIX}
out = []
for ln in lines:
    q = ln.rstrip('\r\n')
    key = q.split(';', 1)[0] if ';' in q else None
    if key in FIX:
        en_len = len(key.encode('latin1'))
        de = FIX[key]
        if len(de.encode('latin1')) > en_len:
            print('BUDGET %r %d>%d' % (key, len(de), en_len))
        else:
            count[key] += 1
            out.append(key + ';' + de)
            continue
    out.append(ln)
for k, n in count.items():
    print('%2d x %r' % (n, k))
if all(n > 0 for n in count.values()):
    io.open(MAP, 'w', encoding='latin1', newline='').write(
        '\n'.join(out))
    r = subprocess.run([sys.executable,
                        '_tools/patch_evt_subtitles.py',
                        '--disc', 'all', '--csv', MAP])
    print('patch rc=%d' % r.returncode)
else:
    print('keine Aenderung')
