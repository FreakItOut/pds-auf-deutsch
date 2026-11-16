# Dump flagged TWN subtitle rows WITH neighboring context for manual review
import re

def is_ok_context(rows, i):
    return i < len(rows) and len(rows[i]) >= 6

for fn in ['TWN_CAMP_PRG_de.csv', 'TWN_RUIN_PRG_de.csv', 'TWN_E022_PRG_de.csv', 'TWN_JIRI_PRG_de.csv']:
    rows = []
    for line in open('_work/subtitles/' + fn, encoding='latin1'):
        line = line.rstrip('\r\n')
        if not line:
            continue
        p = line.split(';')
        if len(p) >= 6:
            rows.append(p)
    print('#### ' + fn)
    for i, p in enumerate(rows):
        en, de = p[4], p[5]
        flags = []
        enw, dew = en.lower(), de.lower()
        if ("n't" in enw) or re.search(r'\b(not|never|no |none|nothing|nobody|without|cannot)\b', enw):
            if not re.search(r'\b(nicht|kein|keine|keinen|keiner|keinem|nie|niemals|ohne|niemand)\b', dew):
                flags.append('NEG')
        if de and not de.rstrip().endswith(('!','?','.',':',';',')','...')):
            if en.rstrip()[-1:] in '.!?':
                flags.append('TRUNC')
        if de.strip() == en.strip() and len(en.strip()) >= 5 and '%' not in en:
            flags.append('UNTR')
        for pat, name in ((r'(?<!\.)\.\.(?!\.)', 'DDOT'), (r'[,]\s', None), (r'[a-zA-Z],[.]', 'CDOT')):
            if pat == (r'[,]\s'):
                import re as r2
                if r2.search(r'\s,', de) and not r2.search(r'\s,', en):
                    flags.append('TCOMMA')
            elif r2 := None:
                pass
            else:
                if re.search(pat, de):
                    flags.append(name)
        if flags:
            print('--- uid %s [%s]' % (p[0], ','.join([f for f in flags if f])))
            if i > 0:
                print('    prev: %r | %r' % (rows[i-1][4][:70], rows[i-1][5][:70]))
            print('    CUR : %r | %r' % (en[:70], de[:70]))
            if i + 1 < len(rows):
                print('    next: %r | %r' % (rows[i+1][4][:70], rows[i+1][5][:70]))
    print()
