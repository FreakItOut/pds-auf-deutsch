# -*- coding: utf-8 -*-
import csv as _csv
import re
import sys

sys.path.insert(0, '_tools')
import umlaut_conv as U

sys.stdout.reconfigure(encoding='latin1')
SECT, DATA = 2352, 2048
EN = re.compile(r"\b(the|you|your|and|that|with|have|this|what|are|is|"
                r"was|were|will|would|from|they|there|their|them|then|"
                r"than|into|can|not|for|but|all|his|her|she|him|one|out|"
                r"about|could|should|when|where|which|who|why|how|any|"
                r"some|just|only|very|more|most|now|again|still|also|"
                r"back|down|off|over|after|before|because|if|so|no|yes|"
                r"do|does|did|been|get|got|make|made|take|come|came|"
                r"know|think|see|look|say|said|tell|told|give|find|found|"
                r"want|need|must|may|might|shall|us|we|me|my|our|its)\b",
                re.I)
recs = list(_csv.DictReader(open('_work/fs_records_all.csv',
                                 encoding='latin1'), delimiter=';'))
r = [x for x in recs if x['name'] == 'MENU.SCB'][0]
lba, size = int(r['lba']), int(r['size'])
out = bytearray()
with open('_work/patched_disc1.bin', 'rb') as f:
    need, s = size, lba
    while need > 0:
        f.seek(s * SECT + 16)
        c = f.read(min(DATA, need))
        if not c:
            break
        out += c
        need -= len(c)
        s += 1
data = bytes(out[:size])
idx = data.find(b'Sturm ueber')
print('idx', hex(idx))
print('context', data[idx - 8:idx + 40])
print('EN match', EN.search('Sturm ueber uns her. Wir'))
for m in re.finditer(rb'[\x20-\x7e\x0a]{4,}', data[max(0, idx - 40):idx + 60]):
    t = m.group().decode('latin1')
    print('match', repr(t), 'len', len(t))
print('convert', repr(U.convert_text('Sturm ueber uns her. Wir')))
