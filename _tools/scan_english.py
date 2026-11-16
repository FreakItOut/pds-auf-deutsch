# -*- coding: utf-8 -*-
# Sucht in allen Dateien der Disc nach englisch aussehenden Saetzen, die
# nicht in den deutschen CSV-Texten vorkommen.
import csv
import glob
import io
import re
import sys

sys.stdout.reconfigure(encoding='latin1')
SECT, DATA = 2352, 2048
disc = int(sys.argv[1]) if len(sys.argv) > 1 else 1

# Deutsche Texte einsammeln
de_corpus = ''
for p in (glob.glob('_work/subtitles/*_de.csv') +
          glob.glob('_work/menu_de/*_de.csv')):
    try:
        de_corpus += io.open(p, encoding='latin1', errors='ignore').read()
    except Exception:
        pass

COMMON = re.compile(r'\b(the|you|your|and|that|with|have|this|what|are|'
                    r'will|from|they|there|would|about|could|should|'
                    r'when|where|which|their|them|then|than|into|'
                    r'can|not|for|but|all|his|her|she|him|one|out)\b',
                    re.I)

recs = list(csv.DictReader(open('_work/fs_records_all.csv',
                                encoding='latin1'), delimiter=';'))
oldname = None
data = b''
with open('_work/patched_disc%d.bin' % disc, 'rb') as f:
    for r in recs:
        if not (r['lba'].isdigit() and r['size'].isdigit()):
            continue
        lba, size = int(r['lba']), int(r['size'])
        if lba == 0 or size == 0 or size > 8 * 1024 * 1024:
            continue
        out = bytearray()
        need, s = size, lba
        while need > 0:
            f.seek(s * SECT + 16)
            c = f.read(min(DATA, need))
            if not c:
                break
            out += c
            need -= len(c)
            s += 1
        d = bytes(out[:size])
        for m in re.finditer(rb'[ -~]{10,}', d):
            t = m.group().decode('latin1')
            if not COMMON.search(t):
                continue
            if t in de_corpus:
                continue
            if sum(ch.isalpha() for ch in t) < len(t) * 0.7:
                continue
            print('%s @%06x %r' % (r['name'], m.start(), t[:100]))
print('done')
