# Zeigt zu Stem+uid die Nachbarschaft + Laengenbudget.
import glob
import io
import os
import sys

sys.stdout.reconfigure(encoding='latin1')
WANT = {
    'TWN_CAMP_PRG': [163, 746, 107, 108, 109, 585],
    'TWN_RUIN_PRG': [205, 388],
    'TWN_SEEK_PRG': [677, 749, 1052, 1090, 1311, 1318, 1357, 1367,
                     1369, 1447],
    'TUTORIAL_CGB': [55688, 60993, 66971],
    'TWN_SEEK_PRG_d4': [105441, 114060],
    'TWN_E128_cd3': [436],
    'TWN_E128': [64447],
}


def unesc(s):
    return s.replace('\\n', '\n')


for stem, uids in WANT.items():
    path = None
    for cand in ('_work/subtitles/%s_de.csv' % stem,
                 '_work/menu_de/%s_de.csv' % stem):
        if os.path.isfile(cand):
            path = cand
            break
    if not path:
        print('FEHLT', stem)
        continue
    rows = []
    for i, line in enumerate(io.open(path, encoding='latin1')):
        if i == 0 and line.startswith('file;'):
            continue
        p = line.rstrip('\r\n').split(';')
        if len(p) < 6:
            continue
        rows.append({'id': p[0] if path.find('subtitles') >= 0 else p[1],
                     'en': p[4], 'de': p[5]})
    print('==== %s' % stem)
    for k, r in enumerate(rows):
        try:
            n = int(r['id'])
        except ValueError:
            continue
        if n in uids:
            print('  ctx:')
            for j in range(max(0, k - 1), min(len(rows), k + 2)):
                m = rows[j]
                print('   %6s EN(%3d) %r' % (m['id'], len(m['en']),
                                             unesc(m['en'])))
                print('          DE(%3d) %r' % (len(m['de']), unesc(m['de'])))
            print()
