# filter only obvious broken German compositions
import csv
import glob
import io
import os
import re
import sys
sys.stdout.reconfigure(encoding='latin1')

suspects = []
for path in sorted(glob.glob('_work/subtitles/TWN_*_de.csv')):
    base = os.path.basename(path)[:-7]
    if base.startswith('TWN_E128'):
        continue
    rows = []
    with io.open(path, encoding='latin1') as f:
        rd = csv.reader(f, delimiter=';')
        for r in rd:
            if len(r) >= 6 and r[0].isdigit():
                rows.append({'uid': int(r[0]),
                             'off': int(r[2].split('|')[0]) if r[2] else 0,
                             'en': r[4], 'de': r[5]})
    rows.sort(key=lambda x: x['off'])
    for i in range(len(rows) - 1):
        a, b = rows[i], rows[i + 1]
        en1, en2 = a['en'].strip(), b['en'].strip()
        de1, de2 = a['de'].strip(), b['de'].strip()
        if len(en1) < 4 or len(en2) < 3 or len(de1) < 3:
            continue
        # ---- specific translations that are clearly broken:
        # subject drops without German verb agreement: EN has "I"/"you"/"he" but DE starts with verb form
        flag = []
        m = re.match(r"^(I|You|She|He|We|It|They|I'm|I'll|I've|I'd|You'll)\b",
                     en1)
        if m:
            d1w = de1.split()
            if d1w and d1w[0].lower() in ('ist', 'werde', 'wird', 'war', 'ism',
                                          'hae', 'habe', 'hins', 'war', 'krank',
                                          'ist ', 'wird', 'eine', 'ein',
                                          'nur', 'er', 'er ', 'bei', 'komm'):
                if d1w[0].lower() not in ('ich', 'du', 'wir', 'sie', 'er',
                                          'es', 'sich', 'mir', 'dir',
                                          'fuer', 'mit', 'in einer', 'istet',
                                          'hab', 'hat', 'ich ', 'du ', 'wir ',
                                          'er ', 'sie ', 'es ', 'ihr ', 'isaa'):
                    flag.append('missing-subject')
        # DE1 ends in a dangling verb/articles boundary
        if de1.split() and de1.split()[-1].lower() in ('das', 'der', 'die', 'dem',
                                                    'den', 'ein', 'eine',
                                                    'einem', 'einer',
                                                    'Fuer', 'fuer', 'mit',
                                                    'an', 'auf', 'kommst'):
            # article ends at EN1-start (POS Pattern) - OK if DE2 completes it
            if de2.split() and de2.split()[0].islower():
                flag.append('dangling-article-lowercase-DE2')
        # DE2 continues as 'solange' style duplicate
        d1w = set(re.findall(r'\w+', de1.lower()))
        d2w = set(re.findall(r'\w+', de2.lower()))
        shared = d1w & d2w
        if len(shared) >= 3 and len(de1) > 6 and len(de2) > 4:
            common = [w for w in shared]
            if 'solange' in common or 'nur' in common:
                flag.append('DUP-MEANING')
        # German ends mid-word (~3 chars)
        if de1.split():
            last = de1.split()[-1]
            if len(last) <= 4 and last.islower() and \
                    not de1.endswith(('.', '!', '?', ',','-')):
                flag.append('DE1-shortcut')
        if flag:
            suspects.append((base, a['uid'], b['uid'], en1, de1, en2, de2,
                             ' / '.join(flag)))

with io.open('_work/review_fixes/final_satzbau_suspects.txt', 'w',
             encoding='latin1', newline='\n') as f:
    for s in suspects:
        f.write('%s %d + %d [%s]\n' % (s[0], s[1], s[2], s[7]))
        f.write(' EN1=%r\n DE1=%r\n EN2=%r\n DE2=%r\n\n' %
                (s[3], s[4], s[5], s[6]))
print('final suspects:', len(suspects))
from collections import Counter
cnt = Counter(x[0] for x in suspects)
for s, n in sorted(cnt.items()):
    print('  %-14s %d' % (s, n))
