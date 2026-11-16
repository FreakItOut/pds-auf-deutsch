# -*- coding: utf-8 -*-
# Zeigt Textstellen mit Font-Slots, die englisch aussehen koennten.
import csv
import re
import sys

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
recs = list(csv.DictReader(open('_work/fs_records_all.csv',
                                encoding='latin1'), delimiter=';'))
with open('_work/patched_disc1.bin', 'rb') as f:
    data = f.read()
count = 0
for m in re.finditer(rb'[\x20-\x7e\x0a]{6,}', data):
    t = m.group().decode('latin1')
    if not any(c in t for c in '^|~{}`[]'):
        continue
    if EN.search(t) and sum(c.isalpha() for c in t) > 8:
        # Disc-Datei ermitteln
        lba = m.start() // SECT
        name = '?'
        for r in recs:
            if not (r['lba'].isdigit() and r['size'].isdigit()):
                continue
            a = int(r['lba'])
            if a and a <= lba < a + (int(r['size']) + DATA - 1) // DATA:
                name = r['name']
                break
        print('%s @%x %r' % (name, m.start(), t[:100]))
        count += 1
        if count >= 40:
            break
print('shown', count)
