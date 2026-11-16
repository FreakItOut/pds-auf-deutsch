# Build the real TWN_E128 cd3 translation from _work/subtitles/TWN_E128_cd3_de.csv
# (451 rows: uid;len;firstOff;copies;en;de). Empty de rows get translations by
# EN-key from the verified TWN pools; binary/debug rows stay as-is.
# Output: _work/menu_de/TWN_E128_de.csv + _work/menu_de/TWN_E128_en.csv
import sys
sys.stdout.reconfigure(encoding='latin1')

FIX = {
    "Don't Exit": 'Bleib hier',
    'ruins.': 'Ruinen',
    "(Ragdam...": '(Radgam...',
    'Town of Zoah': 'Stadt Zoah',
    'Holy District': 'Heil. Bezirk',
    'Leave Town': 'Raus hier',
    '(It is dark up there...)': '(Dunkel dort oben...)',
    'Zoah': 'Zoah',
    'Exit': 'Ende',
    'Buy Item': 'Kaufen',
    'Sell Item': 'Verkauf',
    'FREE': 'FREI',
    'front': 'vorn',
    'back': 'Heck',
    'sides': 'Seit.',
    'Wait Until Nightfall': 'Warte bis zum Abend',
    'Wait Until Morning': 'Warte bis Morgen',
    'Stay': 'Wart',
    'Enter': 'Rein',
    'Stay Out': 'Draussen',
    'Leave': 'Raus',
    'Vaiman...': 'Vaiman...',
}

import glob
import re

pool = {}
for fn in glob.glob('_work/subtitles/TWN_*_de.csv'):
    if 'E128' in fn:
        continue
    for ln in open(fn, encoding='latin1'):
        q = ln.rstrip('\r\n').split(';')
        if len(q) >= 6 and q[5].strip():
            k = q[4].strip()
            pool.setdefault(k, q[5])
for fn in glob.glob('_work/menu_de/TWN_*_map.csv'):
    for ln in open(fn, encoding='latin1'):
        if ';' not in ln:
            continue
        en, de = ln.rstrip('\r\n').split(';', 1)
        if de.strip() and not en.startswith('#'):
            pool.setdefault(en.strip(), de)

DEBUG_OK = {'Clip Mdl', 'Shade', 'ShadeVec', 'PointLight', 'Camera', 'Camera2',
            'Camera3', 'NpcPos', 'DRAM:%6x', 'DIV: %6x', 'VRAM:%6x',
            'pos:', 'Res:', 'Lcs:', 'wwp', 'wwx', 'ff`', 'front', 'back', 'sides'}

def is_binary(en):
    if not en.strip():
        return True
    if any((ord(c) < 32 and c != '\n') or ord(c) > 126 for c in en):
        return True
    if re.search(r'[a-z][A-Z]', en):
        return True
    if '&' in en or '#' in en or '`' in en:
        return True
    return False

probs = {}
rows_out = []
n_auto = n_fix = n_bin = n_miss = n_keep = n_skipbudget = 0
for ln in open('_work/subtitles/TWN_E128_cd3_de.csv', encoding='latin1'):
    q = ln.rstrip('\r\n').split(';')
    if len(q) < 6 or not q[0].isdigit():
        continue
    uid, slen, off0, copies, en, de = q[0], q[1], q[2], q[3], q[4], q[5]
    en_c = en.strip()
    db_km = None  # unused marker
    de_final = None
    if de.strip() and len(de.encode('latin1')) > len(en.encode('latin1')) and en_c in FIX:
        de_final = FIX[en_c]          # existing de too long -> better value
        n_fix += 1
    elif de.strip():
        de_final = de
        n_keep += 1
    elif en_c in FIX:
        de_final = FIX[en_c]
        n_fix += 1
    elif en_c in DEBUG_OK or is_binary(en):
        de_final = en
        n_bin += 1
    elif en_c in pool:
        de_final = pool[en_c]
        n_auto += 1
    else:
        n_miss += 1
        print('MISSING uid=%s [%3d] %r' % (uid, len(en), en[:70]))
        continue
    eb = en.encode('latin1')
    db = de_final.encode('latin1')
    if len(db) > len(eb):
        n_skipbudget += 1
        print('TOO-LONG uid=%s %d>%d %r -> %r' % (uid, len(db), len(eb), en[:50], de_final[:50]))
        continue
    offs = [x for x in copies.split('|') if x] or [off0]
    for o in offs:
        rows_out.append(['TWN_E128.PRG', o, '', slen, en.replace('\n', '\\n'),
                         de_final.replace('\n', '\\n')])

for name, rows in (('TWN_E128_de', rows_out), ('TWN_E128_en',
                   [r[:5] for r in rows_out])):
    with open('_work/menu_de/%s.csv' % name, 'w', encoding='latin1', newline='\n') as fh:
        cols = 'file;off;prefix;len;en;de' if len(rows[0]) == 6 else 'file;off;prefix;len;en'
        fh.write(cols + '\n')
        for r in rows:
            fh.write(';'.join(r) + '\n')
print('keep=%d auto=%d fixed=%d binary=%d missing=%d toolong=%d rows_out=%d'
      % (n_keep, n_auto, n_fix, n_bin, n_miss, n_skipbudget, len(rows_out)))
