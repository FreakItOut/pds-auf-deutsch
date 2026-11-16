# curated broken-chain filter: specifically flags suspicious compositions.
# This is the "second eye" for the user's Satz-und-Sinn review pass.
import csv
import glob
import io
import os
import re
import sys
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


def is_suspicious(de1, de2, en1, en2):
    """Priority patterns that clearly break German sense."""
    flags = []
    d1, d2 = de1.strip(), de2.strip()
    e1, e2 = en1.strip(), en2.strip()
    if not d1 or not d2:
        return flags
    # 1. DUPLICATE: DE2 roughly repeats DE1
    a_words = set(re.findall(r'\w+', d1.lower()))
    b_words = set(re.findall(r'\w+', d2.lower()))
    shared = a_words & b_words
    if len(shared) > 1 and len(d1) > 6 and len(d2) > 4:
        if d1.lower()[-4:] == d2.lower()[:4]:
            flags.append('DUP-WORD')
    # 2. German cut-off: DE ends in a short lowercase fragment without terminal
    words = d1.split()
    if words:
        last_w = words[-1]
        # last word is 'short' + lowercase-only = cut
        if len(last_w) <= 4 and last_w.islower() and not d1.endswith(('.', '!',
                                                                        '?', ',',
                                                                        '-')):
            flags.append('DE1-cut-short')
    # 3. DE1 ends terminal but DE2 is a short lowercase continuation
    if d1.endswith(('.', '!', '?')):
        if d2 and d2[0].islower() and len(d2) < 12:
            flags.append('DE1-dot-DE2-lower')
    # 4. missing subject (EN1 has pronoun, DE1 starts with verb form)
    if re.match(r"^(I|You|She|He|We|It|They)\b", e1) and d1:
        first_w = d1.split()[0].lower()
        if (first_w in ('ist', 'werden', 'wird', 'hab', 'habe', 'macht',
                        'spreche', 'war', 'waren') and
                first_w not in ('ich', 'du', 'wir', 'sie', 'er', 'es',
                                'sich', 'ist', 'mir', 'dir')):
            flags.append('missing-subject')
    # 5. German ends dangling article
    if d1.split() and d1.split()[-1].lower() in ('das', 'der', 'die', 'dem',
                                                'den', 'ein', 'eine', 'einem',
                                                'einer', 'fuer', 'mit',
                                                'an', 'auf'):
        flags.append('dangling-article')
    # 6. DE1-too-long beyond EN1
    if len(d1) - len(e1) > 5:
        flags.append('DE1-over-budget')
    return flags


STEMS = ['TWN_CAMP_PRG', 'TWN_E022_PRG', 'TWN_JIRI_PRG',
         'TWN_RUIN_PRG', 'TWN_SEEK_PRG']
suspects = []
for stem in STEMS:
    path = '_work/subtitles/%s_de.csv' % stem
    if not os.path.exists(path):
        continue
    rows = read(path)
    for i in range(len(rows) - 1):
        a, b = rows[i], rows[i + 1]
        en1, en2 = a['en'].strip(), b['en'].strip()
        de1, de2 = a['de'].strip(), b['de'].strip()
        if len(en1) < 4 or len(en2) < 3 or len(de1) < 3:
            continue
        sub = is_suspicious(de1, de2, en1, en2)
        if sub:
            suspects.append((stem, a['uid'], b['uid'],
                             en1, de1, en2, de2, ' / '.join(sub)))

with io.open('_work/review_fixes/curated_suspects.txt', 'w',
             encoding='latin1', newline='\n') as f:
    for s in suspects:
        f.write('%s %d + %d [%s]\n' % (s[0], s[1], s[2], s[7]))
        f.write(' EN1=%r\n DE1=%r\n EN2=%r\n DE2=%r\n\n' %
                (s[3], s[4], s[5], s[6]))
print('curated suspects:', len(suspects))
from collections import Counter
cnt = Counter(x[0] for x in suspects)
for s, n in sorted(cnt.items()):
    print('  %-14s %d' % (s, n))
