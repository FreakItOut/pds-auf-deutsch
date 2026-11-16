# Build TWN_E128_cd3 translation: reuse verified DE from other TWN csvs
# (EN-key match), plus manual overrides. Output: _work/menu_de/TWN_E128_de.csv
# then menu_text_tool --validate/--patch can run.
import sys
sys.stdout.reconfigure(encoding='latin1')

# manual overrides (budget-checked below)
FIX = {
    "Don't Exit": 'Bleib hier',
    'ruins.': 'Ruinen',
    '(Ragdam...': '(Radgam...',
    'Town of Zoah': 'Stadt Zoah',
    'Holy District': 'Heil. Bezirk',
    'Leave Town': 'Raus hier',
    '(It is dark up there...)': '(Dunkel dort oben...)',
    'Zoah': 'Zoah',
    'Exit': 'Ende',
    'Buy Item': 'Kaufen',
    'Sell Item': 'Verkauf',
    'FREE': 'FREI',
}

# 1) auto EN->DE pool from verified TWN subtitle csvs
import glob
m = {}
for fn in glob.glob('_work/subtitles/TWN_*_de.csv'):
    if 'E128' in fn:
        continue
    for ln in open(fn, encoding='latin1'):
        q = ln.rstrip('\r\n').split(';')
        if len(q) >= 6 and q[5].strip():
            m.setdefault(q[4], q[5])

# 2) read source EN rows
rows = []
for ln in open('_work/subtitles/TWN_E128_cd3_en.csv', encoding='latin1'):
    q = ln.rstrip('\r\n').split(';')
    if len(q) >= 5 and q[0] != 'uid':
        rows.append(q)

# binary/debug detection: printable ASCII (space..z) or known identifiers
def is_binary(en):
    if not en.strip():
        return True
    if any((ord(c) < 32 and c != '\n') or ord(c) > 126 for c in en):
        return True
    import re
    if re.match(r'^[a-zA-Z0-9_:/#&`\[\]\'".,! -]{1,3}$', en):
        pass
    # mojibake/debug garbage: odd case packing, digits, &/#
    if re.search(r'[a-z][A-Z]', en):
        return True
    if '&' in en or '#' in en or '`' in en or re.search(r'[0-9].*[A-Za-z]', en) and len(en) <= 8:
        return True
    return False

DEBUG_OK = {'Clip Mdl', 'Shade', 'ShadeVec', 'PointLight', 'Camera', 'Camera2',
            'Camera3', 'NpcPos', 'DRAM:%6x', 'DIV: %6x', 'VRAM:%6x',
            'pos:', 'Res:', 'Lcs:', 'wwp', 'wwx', 'ff`'}

out_rows = []
n_auto = n_fix = n_bin = n_miss = 0
for q in rows:
    uid, slen, off, copies, en = q[0], q[1], q[2], q[3], q[4]
    en_c = en.strip()
    de = None
    if en_c in FIX:
        de = FIX[en_c]
        n_fix += 1
    elif en_c in DEBUG_OK or is_binary(en):
        de = en
        n_bin += 1
    elif en in m:
        de = m[en]
        n_auto += 1
    else:
        de = ''
        n_miss += 1
        print('MISSING uid=%s %r' % (uid, en[:70]))
        continue
    eb = en.replace('\n', '\\n').encode('latin1')
    db = de.replace('\n', '\\n').encode('latin1')
    if len(db) > len(eb):
        print('TOO LONG uid=%s %d>%d %r' % (uid, len(db), len(eb), de[:60]))
        continue
    out_rows.append(['TWN_E128.PRG', off, '', slen, en.replace('\n', '\\n'),
                     de.replace('\n', '\\n')])

with open('_work/menu_de/TWN_E128_de.csv', 'w', encoding='latin1', newline='\n') as fh:
    fh.write('file;off;prefix;len;en;de\n')
    for r in out_rows:
        fh.write(';'.join(r) + '\n')
print('auto=%d fixed=%d binary/debug=%d missing=%d rows=%d'
      % (n_auto, n_fix, n_bin, n_miss, len(out_rows)))
