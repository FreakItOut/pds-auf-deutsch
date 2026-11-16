# count per-file German/English ratio on the LIVE patched disc
# heuristik: German = has common German substrings/determ; else EN-ish.
import csv
import re
import sys
sys.stdout.reconfigure(encoding='latin1')

SECT, DATA = 2352, 2048
DE_MARKS = re.compile(r'\b(und|der|die|das|nicht|ist|du|wir|fuer|mit|auch|alle|und|dann|jetzt|nen|ein|eine|sich|muss|kaum|hier|doch|wird|sie|oder|mehr|bevor|Millad)\b', re.I)
EN_MARKS = re.compile(r'\b(the|you|and|your|is|are|would|will|not|this|that|with|where|here|now|all|they|they\'re|their|we|out|right|even|attack|shoot|dragon|Back|Enemy|KEY|Battle|units)\b', re.I)


def read_file(bp, lba, size):
    with open(bp, 'rb') as fh:
        out = bytearray()
        need = size
        s = lba
        while need > 0:
            fh.seek(s * SECT + 16)
            c = fh.read(min(DATA, need))
            if len(c) < min(DATA, need):
                break
            out += c
            need -= len(c)
            s += 1
    return bytes(out[:size])


idx = {r['name']: (int(r['lba']), int(r['size']))
       for r in csv.DictReader(open('_work/fs_records_all.csv', encoding='latin1'),
                               delimiter=';') if int(r['lba']) > 0}
FILES = ['BTL_A3.FNT', 'BTL_A32.FNT', 'BTL_A53.FNT', 'BTL_A5_2.PRG',
         'BTL_A7.FNT', 'BTL_A72.FNT', 'BTL_B2.FNT', 'BTL_B53.FNT',
         'BTL_B5_2.PRG', 'BTL_B6.FNT', 'BTL_B62.FNT', 'BTL_C22.FNT',
         'BTL_C4.FNT', 'BTL_C5.FNT', 'BTL_C8.FNT', 'BTL_C82.FNT',
         'BTL_D2.FNT', 'BTL_D22.FNT', 'BTL_D4.FNT', 'BTL_D5.FNT']
tot_de = tot_en = 0
for name in FILES:
    lba, size = idx[name]
    data = read_file('_work/patched_disc1.bin', lba, size)
    nd = ne = 0
    samples = []
    for part in data.split(b'\x00'):
        if len(part) < 10:
            continue
        t = part.decode('latin1', 'replace')
        # control-marker row (we don't care)
        if '%' in t and len(t) < 12:
            continue
        has_de = bool(DE_MARKS.search(t))
        has_en = bool(EN_MARKS.search(t))
        if has_de:
            nd += 1
        elif has_en and ' ' in t:
            ne += 1
            if len(samples) < 4:
                samples.append(t[:60])
    print('%-14s DE-like=%3d EN-like=%3d  %s' % (name, nd, ne, samples))
    tot_de += nd
    tot_en += ne
print('TOTAL DE-like', tot_de, 'EN-like', tot_en)
