# fresh chain-context dump — used by the reviewer (me) to scan ALL chains
import csv, glob, io, os, sys
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
with io.open('_work/review_fixes/chain_all.txt', 'w',
             encoding='latin1', newline='\n') as f:
    for stem in STEMS:
        path = '_work/subtitles/%s_de.csv' % stem
        if not os.path.exists(path):
            continue
        rows = read(path)
        nchains = 0
        for i in range(len(rows) - 1):
            a, b = rows[i], rows[i + 1]
            en1 = a['en'].rstrip()
            en2 = b['en'].lstrip()
            if len(en1) < 3 or len(en2) < 3:
                continue
            # CHAIN if EN1 does not end in a terminal punctuation:
            is_chain = not en1.endswith(('.', '!', '?')) and en1[-1:] != '0'
            if not is_chain:
                continue
            nchains += 1
            f.write('===== %s %d + %d =====\n' % (stem, a['uid'], b['uid']))
            for k in range(max(0, i - 3), min(len(rows), i + 4)):
                mark = ' * ' if k in (i, i + 1) else '   '
                r = rows[k]
                f.write('%s%-5d %-6d %r\n' % (mark, r['uid'], r['off'], r['en']))
                f.write('     %r\n' % r['de'])
            f.write('\n')
        print(stem, 'chains:', nchains)
