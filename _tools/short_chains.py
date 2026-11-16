# Flag TWN chains where the German is much shorter than the English
# (possible dropped content). Skips obvious debug/binary rows.
import io
import re
import sys

sys.stdout.reconfigure(encoding='latin1')
STEMS = ['TWN_E022_PRG', 'TWN_JIRI_PRG', 'TWN_CAMP_PRG', 'TWN_RUIN_PRG',
         'TWN_SEEK_PRG']
TERM = re.compile(r'[.!?)]\s*$')


def read_stem(stem):
    rows = []
    for ln in io.open('_work/subtitles/%s_de.csv' % stem, encoding='latin1'):
        q = ln.rstrip('\r\n').split(';')
        if len(q) >= 6 and q[0].isdigit():
            rows.append({'uid': int(q[0]), 'en': q[4], 'de': q[5]})
    return rows


def is_debug(s):
    return (not s.strip() or any(ord(c) < 32 and c != '\n' for c in s)
            or any(ord(c) > 126 for c in s) or '&' in s or '#' in s)


n = 0
for stem in STEMS:
    rows = read_stem(stem)
    cur = []
    for r in rows:
        cur.append(r)
        if TERM.search(r['en'].rstrip()) or len(cur) >= 6:
            en = ' '.join(x['en'].strip() for x in cur)
            de = ' '.join(x['de'].strip() for x in cur)
            if not is_debug(en) and len(en) >= 25 and len(de) < len(en) * 0.62:
                print('%s %d-%d  DE=%d EN=%d'
                      % (stem, cur[0]['uid'], cur[-1]['uid'], len(de), len(en)))
                print('  EN: ' + en)
                print('  DE: ' + de)
                n += 1
            cur = []
print('flagged=%d' % n)
