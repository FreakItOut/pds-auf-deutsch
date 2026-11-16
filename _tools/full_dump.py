# full chain dump (prev,A,B,next,next2) — for manual style review
import csv
import glob
import io
import os
import sys
sys.stdout.reconfigure(encoding='latin1')

def read(path):
    with io.open(path, encoding='latin1') as f:
        rd = csv.reader(f, delimiter=';')
        first = next(rd, None)
        rows = []
        if first and first[0] == 'uid':
            for r in rd:
                if len(r) >= 6 and r[0].isdigit():
                    rows.append({'uid': int(r[0]),
                                 'off': int(r[2].split('|')[0]) if r[2] else 0,
                                 'en': r[4], 'de': r[5]})
        elif first and first[0] == 'file':
            for r in rd:
                if len(r) >= 6:
                    rows.append({'uid': -1,
                                 'off': int(r[1]) if r[1].isdigit() else 0,
                                 'en': r[4], 'de': r[5]})
    rows.sort(key=lambda x: x['off'])
    return rows

STEMS = ['TWN_CAMP_PRG', 'TWN_E022_PRG', 'TWN_JIRI_PRG',
         'TWN_RUIN_PRG', 'TWN_SEEK_PRG']

with io.open('_work/review_fixes/chain_context_full.txt', 'w',
             encoding='latin1', newline='\n') as f:
    for stem in STEMS:
        path = '_work/subtitles/%s_de.csv' % stem
        if not os.path.exists(path):
            continue
        rows = read(path)
        chains = 0
        for i in range(len(rows) - 1):
            a, b = rows[i], rows[i + 1]
            en1, en2 = a['en'].strip(), b['en'].strip()
            # treat EN1 as chain-start when: en1 ends without terminal
            if not en1 or not en2:
                continue
            if len(en1) < 3 or len(en2) < 3:
                continue
            # detect CHAIN: EN1 ends without terminal OR DE1 ends without terminal
            am = a['en'].rstrip().endswith(('.', '!', '?'))
            bm = b['en'].rstrip()[0].islower() if b['en'].rstrip() else False
            am2 = a['de'].rstrip().endswith(('.', '!', '?')) if a['de'] else True
            bm2 = \
                (len(a['de'].strip()) > 0 and b['de'].strip()
                 and b['de'].strip()[0].islower()) if b['de'].strip() else True
            if am and am2:
                continue     # disk looks complete; skip
            if (not am or not bm) and (not am2 or not bm2):
                chains += 1
                f.write('===== %s %d + %d =====\n' % (stem, a['uid'], b['uid']))
                for k in range(max(0, i - 3), min(len(rows), i + 4)):
                    mark = '*' if k in (i, i + 1) else ' '
                    r = rows[k]
                    f.write('%s %6d | %6d | %r\n         | %r\n' %
                            (mark, r['uid'], r['off'], r['en'], r['de']))
                f.write('\n')
        print(stem, 'chains: %d' % chains)
