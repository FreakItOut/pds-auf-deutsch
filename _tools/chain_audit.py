# audit: locate EN sentence chains split across subtitles whose German
# composition looks broken (block1 ends with continuation token but the
# German block1 does NOT end with a matching German span, etc.)
# Output: review list of (stem, uid, EN1, DE1, EN2, DE2).
import csv
import glob
import os
import re
import sys
sys.stdout.reconfigure(encoding='latin1')

CONT_TAIL = re.compile(
    r"(\b(und|oder|so|als|dass|wenn|weil|aber|und dann|also|hier|von|zu|an|in|"
    r"auf|zum|zur|fuer|mit|meine|mein|deine|dein|ist|wird|haben|hat|sedan|was|"
    r"wo|wann|mit dem|mit der|in den|in der|auf den|auf der|ueber den|"
    r"ueber der|aus den|aus der|vor dem|nach dem|dazu|dies|diese|dieser|"
    r"jeder|jede|jedes|seine|seiner|ihr|ihrer|beide|wieder|noch|bloed|"
    r"gleich|einem|einer|eine| einem|eine|keine|keinen|mein| meine|"
    r"Mein|Meine|Dein|Deine|Deiner|kommst|kommt|kommen|machst|macht|"
    r"koennen|koennte|werde|werden|was|was ich|was wir|das|der|die)::?)\W*$", re.I)
CONT_HEAD = re.compile(r'^[a-z:)(),*\x09\x06\x08][A-Za-z0-9 )]*$')

def classify(en, de):
    """return reason if the pair looks broken"""
    en1, de1 = en, de
    reasons = []
    en_tail_cont = bool(CONT_TAIL.search(en1))
    de_comma = de1.rstrip().endswith((',', ''))
    # mismatch: EN breaks with a comma, DE doesn't
    if en1.rstrip().endswith(',') and not de1.rstrip().endswith(',') \
            and not de1.rstrip().endswith(('ists',)):
        reasons.append('EN-comma-DE-not')
    return reasons


def load_rows(stem):
    path = '_work/subtitles/%s_de.csv' % stem
    rows = []
    if not os.path.exists(path):
        return rows
    for ln in open(path, encoding='latin1'):
        q = ln.rstrip('\r\n').split(';')
        if len(q) < 6:
            continue
        rows.append({'uid': int(q[0]) if q[0].isdigit() else -1,
                     'len': q[1],
                     'off0': int(q[2].split('|')[0]) if q[2] and q[2][0].isdigit() else -1,
                     'offs': q[3],
                     'en': q[4],
                     'de': q[5]})
    rows.sort(key=lambda r: r['off0'])
    return rows


def is_ctrl(en):
    if '%' in en and len(en.strip()) < 14: return True
    return False

CHAINS = []
for path in sorted(glob.glob('_work/subtitles/TWN_*_de.csv')):
    base = os.path.basename(path)[:-7]
    if 'E128' in base:
        continue
    rows = load_rows(base)
    for a, b in zip(rows, rows[1:]):
        if is_ctrl(a['en']) or is_ctrl(b['en']):
            continue
        # EN1 should look like a sentence-break continuation: either ends with
        # non-terminal or the next block starts lowercase
        en1 = a['en'].rstrip()
        en2 = b['en'].lstrip()
        if len(en2) < 2 or len(en1) < 2:
            continue
        if en1[-1] in '.!?':
            continue  # clean sentence end -> skip
        de1 = a['de'].rstrip()
        de2 = b['de'].strip()
        reasons = classify(en1, de1)
        # broken chain flags:
        bad_de_starts = bool(CONT_HEAD.match(de2))
        if bad_de_starts and de1 and de1[-1] not in (',', ';', '?', '!', '-'):
            reasons.append('DE2-lowercase-DE1-terminal')
        elif bad_de_starts and de1 and de1[-1] == '-':
            pass
        elif bad_de_starts:
            reasons.append('DE2-lowercase')
        # chain may end of 'and'-like word in DE but the following sentence doesn't match
        # (already caught by EN-comma rule) ... also detect our overflow-length split tail: 'x...',
        # e.g. broken 'Dort seh' chains like 'Jaeger...'
        if reasons:
            CHAINS.append({'stem': base, 'a_uid': str(a['uid']), 'b_uid': str(b['uid']),
                           'en1': en1, 'de1': de1, 'en2': en2, 'de2': de2,
                           'reasons': '|'.join(reasons)})

with open('_work/review_fixes/chain_audit.txt', 'w', encoding='latin1', newline='\n') as f:
    for c in CHAINS:
        f.write('%s %s+-%s [%s]\n' % (c['stem'], c['a_uid'], c['b_uid'], c['reasons']))
        f.write(' EN1=%r\n' % c['en1'])
        f.write(' DE1=%r\n' % c['de1'])
        f.write(' EN2=%r\n' % c['en2'])
        f.write(' DE2=%r\n\n' % c['de2'])
print('chains:', len(CHAINS))
