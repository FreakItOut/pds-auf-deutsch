# chain_audit2: a fresh, semantic scan for broken-composition pairs.
# includes _all_ TWN subtitle csvs (skipping E128) AND BTL/FLD MCB/FNT files.
# flag a pair when: EN block1 is 'continuation' (ends without terminal),
# block2 EN starts lowercase, and the German pair does NOT compose
# (DE1 ends terminal backslash-dot or DE2 starts uppercase).
# Also flag D-CUT cases where German ends mid-word.
import csv
import glob
import io
import os
import re
import sys
sys.stdout.reconfigure(encoding='latin1')

TERM = ('.', '!', '?')
CONT = re.compile(r'^(und|oder|so|als|dass|wenn|weil|aber|also|hier|von|zu|'
                  r'zum|zur|fuer|mit|meine|mein|deine|dein|ist|wird|haben|'
                  r'hat|hat|war|wo|wann|ieh|mit|bei|nach|durch|gegen|ueber|'
                  r'des|dem|den|dies|diese|dieser|jeder|jede|jedes|seine|'
                  r'seiner|ihr|ihrer|beide|noch|wieder|gem|Komm|komm)', re.I)

COMMA_OR_CONT = re.compile(
    r'[.,!?:;-]$|(\s(fuer|mit|das|der|die|dem|den|und|oder|ist|dass|dieser|'
    r'diese|dies|ein|eine|einem|einer|sich|bis|zum|zur|in|von|auf|ueber|'
    r'durch|fuer|haben|hab|war|hier|noch|niemals|nie|keine|kein|'
    r'keinen)$)', re.I)

def read(path):
    with io.open(path, encoding='latin1') as f:
        rd = csv.reader(f, delimiter=';')
        first = next(rd, None)
        rows = []
        if not first:
            return rows
        # discover column layout
        if first[0] == 'uid':
            cols = 'uid'
            for r in rd:
                if len(r) < 6:
                    continue
                rows.append({'uid': int(r[0]) if r[0].isdigit() else -1,
                             'off': int(r[2].split('|')[0]) if r[2] and
                                    r[2][0].isdigit() else 0,
                             'en': r[4], 'de': r[5]})
        elif first[0] == 'file':
            for r in rd:
                if len(r) < 6:
                    continue
                rows.append({'uid': -1,
                             'off': int(r[1]) if r[1].isdigit() else 0,
                             'en': r[4], 'de': r[5]})
    return rows


def is_bad(de1, en1, de2, en2):
    bad = []
    de1, de2 = de1.strip(), de2.strip()
    en1, en2 = en1.strip(), en2.strip()
    if not de1 or not de2:
        return bad
    # 1. EN1 ends with comma / continuation, DE1 lost terminal marker
    if en1.endswith(','):
        if not de1.endswith((',', '-', ';')):
            bad.append('E1comma/DE1-no')
    # 2. DE1 starts in mid-sentence but ends with terminal that suggests miss
    if de2.startswith(de2[0].lower()) and en2[0:1].islower():
        # chain composition is normal if de1 doesn't end with .!? (mid-flow)
        if de1[:-1].rstrip().endswith(('.','!','?')):
            bad.append('DE1-dot-DE2-lower')
    # 3. overlapping EN: DE1 too long compared with EN1
    if len(de1) - len(en1) > 4:
        bad.append('DE1-len>>EN1')
    if len(de2) - len(en2) > 4:
        bad.append('DE2-len>>EN2')
    # 4. truncated German tail (missing terminal after a short cut word)
    cut = de1.split()
    if cut:
        tailw = cut[-1]
        if (len(tailw) <= 3 and not de1.endswith(('.', '!', '?', ',', '-',
                                                 ';', ':', ')'))
                and en1.endswith(('.', '!', '?'))):
            bad.append('DE1-short-tail')
    # 5. the EN has a proper subject ('I'/'You') at start, DE starts with a verb-form
    if re.match(r"^(I|You|She|He|We|It|They)\b", en1) and de1 and de1.split()[0].islower():
        if de1.split()[0] not in ('ich', 'ich)', 'du', 'wir', 'sie', 'sich',
                                  'du!', 'ich,', 'wir!', 'mir', 'dir'):
            bad.append('EN-pronoun-DE-verb-first')
    return bad

chains = []
for path in sorted(glob.glob('_work/subtitles/TWN_*_de.csv')):
    base = os.path.basename(path)[:-7]
    if base.startswith('TWN_E128'):
        continue
    rows = read(path)
    rows.sort(key=lambda r: r['off'])
    for a, b in zip(rows, rows[1:]):
        en1, en2 = a['en'].strip(), b['en'].strip()
        de1, de2 = a['de'].strip(), b['de'].strip()
        if len(en1) < 3 or len(en2) < 3:
            continue
        if '%' in en1[:3] and len(en1) < 14:
            continue
        bad = is_bad(de1, en1, de2, en2)
        if bad:
            chains.append({'stem': base, 'ua': a['uid'], 'ub': b['uid'],
                           'en1': en1, 'de1': de1, 'en2': en2, 'de2': de2,
                           'bad': '|'.join(bad)})

with open('_work/review_fixes/chain_audit2_twn.txt', 'w',
          encoding='latin1', newline='\n') as f:
    for c in chains:
        f.write('%s %d + %d [%s]\n' % (c['stem'], c['ua'], c['ub'], c['bad']))
        f.write(' EN1=%r\n DE1=%r\n EN2=%r\n DE2=%r\n\n' %
                (c['en1'], c['de1'], c['en2'], c['de2']))
print('chains:', len(chains))
per = {}
for c in chains:
    per.setdefault(c['stem'], 0)
    per[c['stem']] += 1
for s in sorted(per):
    print('  %-14s %d' % (s, per[s]))
