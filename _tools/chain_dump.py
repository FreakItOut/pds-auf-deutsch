# Group consecutive UIDs into chains where a block does not end a sentence.
import io
import re
import sys

sys.stdout.reconfigure(encoding='latin1')

STEMS = ['TWN_E022_PRG', 'TWN_JIRI_PRG', 'TWN_CAMP_PRG', 'TWN_RUIN_PRG',
         'TWN_SEEK_PRG']

TERM = re.compile(r'[.!?)]\s*$')


def read_stem(stem):
    rows = []
    fn = '_work/subtitles/%s_de.csv' % stem
    for ln in io.open(fn, encoding='latin1'):
        q = ln.rstrip('\r\n').split(';')
        if len(q) >= 6 and q[0].isdigit():
            rows.append({'uid': int(q[0]), 'en': q[4], 'de': q[5]})
    return rows


def chains(rows):
    out = []
    cur = []
    for r in rows:
        cur.append(r)
        if TERM.search(r['en'].rstrip()) or len(cur) >= 6:
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


for stem in STEMS:
    rows = read_stem(stem)
    ch = chains(rows)
    print('#### %s rows=%d chains=%d' % (stem, len(rows), len(ch)))
    for c in ch:
        if len(c) == 1 and TERM.search(c[0]['en'].rstrip()) and c[0]['de'].strip():
            continue  # single complete blocks are mostly fine, skip for now
        lo, hi = c[0]['uid'], c[-1]['uid']
        en = ' / '.join(x['en'].strip() for x in c)
        de = ' / '.join(x['de'].strip() for x in c)
        print('%s %d-%d' % (stem, lo, hi))
        print('  EN: ' + en)
        print('  DE: ' + de)
