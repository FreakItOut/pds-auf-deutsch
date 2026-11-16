# fresh chain-context dump (fixed to read both headered and headerless csvs)
import csv, glob, io, os, sys
sys.stdout.reconfigure(encoding='latin1')


def read(path):
    with io.open(path, encoding='latin1') as f:
        rd = csv.reader(f, delimiter=';')
        rows = [r for r in rd if r and len(r) >= 6 and r[0].isdigit()]
    out = [{'uid': int(r[0]),
            'off': int(r[2].split('|')[0]) if r[2] else 0,
            'en': r[4], 'de': r[5]} for r in rows]
    out.sort(key=lambda x: x['off'])
    return out


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
            # 2-block chain when:
            #  - EN1 does NOT end in .!?
            #  - AND DE1 doesn't end in a close (indicating unfinished)
            #  - AND en2 starts lowercase or non-alphabetical signal
            c1 = not en1.endswith(('.', '!', '?'))
            c2 = (b['en'].strip()[0].islower() if b['en'].strip()[0:1] else False) or \
                 (a['de'].strip() and not a['de'].strip().endswith(
                     ('.', '!', '?', '-', ')')) and b['de'].strip()
                  and b['de'].strip()[0:1].islower())
            is_chain = c1 and (c2 or not a['de'].rstrip().endswith(('.')))
            if not is_chain:
                continue
            nchains += 1
            f.write('===== %s %d + %d =====\n' % (stem, a['uid'], b['uid']))
            for k in range(max(0, i - 3), min(len(rows), i + 4)):
                mark = ' * ' if k in (i, i + 1) else '   '
                r = rows[k]
                f.write('%s%-5d %-6d %r\n' % (mark, r['uid'], r['off'], r['en']))
                f.write('     %r\n' % r['de'][-70:])
            f.write('\n')
        print(stem, 'chains:', nchains)
