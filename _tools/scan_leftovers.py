# Scan evt_de_map.csv and menu_de CSVs for suspicious rows.
import glob
import io
import re
import sys

sys.stdout.reconfigure(encoding='latin1')
EN_WORDS = set('the you your are and with that this from have will was were '
               'for not but his her their they what when who why how '
               'there here about into over only just like'.split())
WORD = re.compile(r"[A-Za-z']+")


def check_label(label, en, de):
    issues = []
    if not de.strip():
        issues.append('EMPTY')
        return issues
    if de.strip() == en.strip():
        issues.append('IDENT')
    words = [w.lower() for w in WORD.findall(de)]
    hits = [w for w in words if w in EN_WORDS]
    if hits:
        issues.append('EN:' + ','.join(sorted(set(hits))))
    if len(de) > len(en):
        issues.append('LONG %d>%d' % (len(de), len(en)))
    if any(ord(c) > 126 for c in de):
        issues.append('NONASCII')
    if len(en) >= 20 and len(de) < len(en) * 0.45:
        issues.append('SHORT %d/%d' % (len(de), len(en)))
    if issues:
        print('%s | %s | EN=%r | DE=%r' % (label, ' '.join(issues), en, de))
    return issues


rows = []
for ln in io.open('_work/evt_de_map.csv', encoding='latin1'):
    ln = ln.rstrip('\r\n')
    if ';' not in ln:
        continue
    en, de = ln.split(';', 1)
    rows.append((en, de))

print('=== evt_de_map rows=%d ===' % len(rows))
n = 0
for i, (en, de) in enumerate(rows):
    if check_label('evt%03d' % i, en, de):
        n += 1
print('evt flagged=%d' % n)

print('=== menu_de files ===')
for path in sorted(glob.glob('_work/menu_de/*_de*.csv')):
    if path.endswith('_en.csv'):
        continue
    bad = 0
    for ln in io.open(path, encoding='latin1'):
        q = ln.rstrip('\r\n').split(';')
        if len(q) < 6 or not q[0].isdigit():
            continue
        en, de = q[4].replace('\\n', ' '), q[5].replace('\\n', ' ')
        if check_label(path.split('\\')[-1], en, de):
            bad += 1
    if bad:
        print('--- %s flagged=%d' % (path, bad))
