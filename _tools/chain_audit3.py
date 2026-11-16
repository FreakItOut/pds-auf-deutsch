# comprehensive sense-check audit: every 2-block chain and every shortened
# German line in TWN* across the 4 discs, scored for broken composition.
# Model: German must read as a full sentence when concatenated; flag rows
# where composition looks wrong (cut mid-word, missing verb tail, comma
# mismatch, contradicting sense order).
import csv
import glob
import io
import os
import re
import sys
sys.stdout.reconfigure(encoding='latin1')

# vocabulary of obvious-broken symptoms:
CUT_SUFFIX = re.compile(r'(sch|st|end|er|ig|en|ein|aus|mit|fuer|durch)$'
                       ).search           # lines ending like a cut German word
TERM = ('.', '!', '?')
CONT_KW = re.compile(
    r'(\bund$|für$|fuer$|mit$|aus$|zu$|zum$|zur$|von$|das$|der$|die$|'
    r'dem$|den$|sein$|ihre$|ihrem|ihren$|kommst$|kommt$|komme$|las$|les$|'
    r'ich$|ich$|bin$|bist$|wurde$|hat$|hab$|habt$|habe$|wird$|wird$|'
    r'dort$|hier$|und ich$|Bruecke$|den$|schick$|way$)', re.I)

def read_csv_cols(path):
    with io.open(path, encoding='latin1') as f:
        rd = csv.reader(f, delimiter=';')
        header = next(rd, None)
        lo = []
        if header and header[0] == 'uid':
            for r in rd:
                if len(r) >= 6 and r[0].isdigit():
                    lo.append({'uid': int(r[0]), 'off': int(r[2].split('|')[0]),
                               'en': r[4], 'de': r[5]})
        elif header and header[0] == 'file':
            for r in rd:
                if len(r) >= 6:
                    lo.append({'uid': int(r[1]) if r[1].isdigit() else -1,
                               'off': int(r[1]), 'en': r[4], 'de': r[5]})
    return lo


def looks_bad(de1, en1, de2, en2):
    """flags a 2-block German pair when the joint composition is obviously broken"""
    bad = []
    # symptom: block1 continues (ends in comma or 'und') but block2 starts uppercase-looking FINISHED sentence
    de1s = de1.strip()
    de2s = de2.strip()
    en1s = en1.strip()
    en2s = en2.strip()
    # look for a German slash-continuing English comma -> OK normally
    if en1s.endswith(',') and not de1s.endswith((',', '(', '-')):
        bad.append('EN-comma-DE-lacks')
    if en1s.endswith('-') and not de1s.endswith(('-', '')):
        bad.append('EN-hyphen-lacks')
    # symptom: EN1 says on a line but DE1 dropped the whole thing
    if re.search(r'\b(ist|are|ist|sind|sein|hat|haben)\b', en1s.lower()[-40:]) \
            and not de1s and de1s != '':
        bad.append('en1-verb-de1-empty')
    # symptom: block1 ends in a preposition ' und ' but block2 begins a new thought
    if CONT_KW.search(de1s) and de2s and de2s[0].isupper():
        bad.append('DE1-cont-DE2-upper')
    # symptom: block1 ends without final punct. but block2 really is a new sentence
    if not de1s.endswith(TERM + (',', '-', ';', ')')):
        # and DE2 begins in a way that reads as continuation
        pass
    # symptom: both DE blocks together exceed 'natural' length
    if len(de1s) + len(de2s) > len(en1s) + len(en2s) + 4:
        bad.append('composition-way-longer')
    # symptom: DE1 ends in cut-mid-word
    if (de1s and de1s[-1].islower() and len(de1s) > 2
            and de1s[-1] not in 'aehioisrulmnstcdw' + '' and
            not any(de1s.endswith(x) for x in ('.', '!', '?', ',', '-', ')',
                                               ';', ':', 'sch', 'st', 'ch',
                                               'tz', 'nd', 'rd', 'kt', 'ft',
                                               'eg', 'ht', 'ng', 'ert', 'cht',
                                               'ver', 'und', 'beit', 'luft',
                                               'ung', 'tzt', 'ner'))):
        bad.append('DE1-cut-tail')
    # symptom: DE2 starts lowercase but DE1 ended terminal (makes DE1 look
    # complete - mismatch composition)
    if de2s and de2s[0].islower() and de1s and de1s[-1] in '.!?':
        bad.append('DE2-lower-after-dot')
    return bad


chains = []
for path in sorted(glob.glob('_work/subtitles/TWN_*_de.csv')):
    base = os.path.basename(path)[:-7]
    if base.startswith('TWN_E128'):
        continue
    rows = read_csv_cols(path)
    rows.sort(key=lambda r: r['off'])
    for a, b in zip(rows, rows[1:]):
        en1, en2 = a['en'].strip(), b['en'].strip()
        de1, de2 = a['de'].strip(), b['de'].strip()
        if not en1 or not en2 or len(en1) < 3 or len(en2) < 3:
            continue
        bad = looks_bad(de1, en1, de2, en2)
        if bad:
            chains.append({'stem': base, 'ua': a['uid'], 'ub': b['uid'],
                           'en1': en1, 'de1': de1, 'en2': en2, 'de2': de2,
                           'bad': '|'.join(bad)})
# write audit
with io.open('_work/review_fixes/chain_audit2.txt', 'w',
             encoding='latin1', newline='\n') as f:
    for c in chains:
        f.write('%s %d + %d [%s]\n' % (c['stem'], c['ua'], c['ub'], c['bad']))
        f.write(' EN1=%r\n DE1=%r\n EN2=%r\n DE2=%r\n\n' %
                (c['en1'], c['de1'], c['en2'], c['de2']))
print('chains flagged:', len(chains))
items = sorted(set(c['stem'] for c in chains))
for s in items:
    n = sum(1 for c in chains if c['stem'] == s)
    print('  ', s, n)
