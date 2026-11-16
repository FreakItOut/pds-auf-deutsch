# -*- coding: utf-8 -*-
# Wo stehen noch ae/oe/ue-Texte (Beispiel "fuer") in der Disc?
import csv
import sys

sys.stdout.reconfigure(encoding='latin1')
SECT, DATA = 2352, 2048
needles = [b' fuer ', b' ueber ', b' koennen ', b' moechte ', b' waehrend ']
recs = list(csv.DictReader(open('_work/fs_records_all.csv',
                                encoding='latin1'), delimiter=';'))
data = open('_work/patched_disc1.bin', 'rb').read()
for n in needles:
    pos = 0
    out = []
    while True:
        p = data.find(n, pos)
        if p < 0:
            break
        lba = p // SECT
        for r in recs:
            if not (r['lba'].isdigit() and r['size'].isdigit()):
                continue
            a = int(r['lba'])
            size = int(r['size'])
            if a and a <= lba < a + (size + DATA - 1) // DATA:
                out.append((r['name'], (lba - a) * DATA))
                break
        pos = p + 1
    print(n.decode(), len(out), out[:12])
