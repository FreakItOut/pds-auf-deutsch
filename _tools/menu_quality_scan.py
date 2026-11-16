# Scan menu/tutorial/battle DE CSVs for leftover English and formatting issues.
import glob
import io
import re
import sys

sys.stdout.reconfigure(encoding='latin1')
EN_WORDS = set('the you your are and with that this from have will was were '
               'for not but his her their they what when who why how there '
               'here about into over only just like can may should would '
               'does did been being'.split())
WORD = re.compile(r"[A-Za-z']+")
SKIP = re.compile(r'(^PDiary|^PDragon|^PAbout)')


def check(path):
    bad = 0
    for ln in io.open(path, encoding='latin1'):
        q = ln.rstrip('\r\n').split(';')
        if len(q) < 6 or not q[0].isdigit():
            continue
        en, de = q[4], q[5]
        if not de.strip() or en.strip() == de.strip():
            continue
        words = [w.lower() for w in WORD.findall(de)]
        hits = sorted({w for w in words if w in EN_WORDS})
        if hits:
            print('%s %s EN_WORDS=%s | EN=%r | DE=%r'
                  % (path.split('\\')[-1], q[0], ','.join(hits), en, de))
            bad += 1
        if len(de) > len(en):
            print('%s %s LONG %d>%d | EN=%r | DE=%r'
                  % (path.split('\\')[-1], q[0], len(de), len(en), en, de))
            bad += 1
        if any(ord(c) > 126 for c in de):
            print('%s %s NONASCII | DE=%r' % (path.split('\\')[-1], q[0], de))
            bad += 1
    return bad


paths = ['_work/menu_de/TUTORIAL_CGB_de.csv',
         '_work/menu_de/MENU_SCB_de.csv',
         '_work/menu_de/CHILDMP_MCB_de.csv']
total = 0
for p in paths:
    n = check(p)
    print('--- %s flagged=%d' % (p.split('\\')[-1], n))
    total += n
print('TOTAL=%d' % total)
