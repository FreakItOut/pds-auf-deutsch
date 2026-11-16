# -*- coding: utf-8 -*-
"""Setzt die EVT-Untertitel (evt_de_map.csv) auf Font-Slots um."""
import io
import sys

sys.path.insert(0, '_tools')
import umlaut_conv as U

sys.stdout.reconfigure(encoding='latin1')
SRC = '_work/evt_de_map.csv'
OUT = '_work/evt_de_map.csv'
lines = io.open(SRC, encoding='latin1').read().split('\n')
changed = 0
budget = 0
res = []
for ln in lines:
    q = ln.rstrip('\r\n')
    if ';' not in q or q.startswith('#'):
        res.append(ln)
        continue
    en, de = q.split(';', 1)
    new = U.convert_text(de)
    if new != de:
        if len(new.encode('latin1')) > len(en.encode('latin1')):
            budget += 1
            res.append(ln)
            continue
        changed += 1
        res.append(en + ';' + new)
    else:
        res.append(ln)
io.open(OUT, 'w', encoding='latin1', newline='\n').write('\n'.join(res))
print('changed=%d budget=%d' % (changed, budget))
