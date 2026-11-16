# quick diagnostic: print first 20 rows + end-of-EN distribution
import csv
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


from collections import Counter
for stem in ('TWN_CAMP_PRG',):
    path = '_work/subtitles/%s_de.csv' % stem
    print(path)
    if not os.path.exists(path):
        print('missing!')
        continue
    rows = read(path)
    print('rows', len(rows))
    c = Counter(r['en'].rstrip()[-1] for r in rows[:100])
    print('last chars of EN for first 100 rows:', c.most_common())
    print()
    for i, r in enumerate(rows[:20]):
        print(i, 'uid', r['uid'], 'off', r['off'],
              'en_last3=', repr(r['en'].rstrip()[-3:]), 'en=', repr(r['en'][:50]))
