import sys, glob, os, re
sys.stdout.reconfigure(encoding='latin1')
def is_ident(en):
    if '%' in en:
        return True
    if re.match(r'^[A-Z0-9_ %,:.\-]+$', en) and not any(ch.islower() for ch in en):
        return True
    return False
for fn in ('_work/menu_de/CHILDMP_MCB_de.csv',
           '_work/menu_de/CHILDMP_MCB_de_d1.csv',
           '_work/menu_de/CHILDMP_MCB_de_d2.csv',
           '_work/menu_de/FLD_B6_MCB_de.csv',
           '_work/menu_de/FLD_C4_6_MCB_de.csv',
           '_work/menu_de/FLD_A3_MCB_de.csv',
           '_work/menu_de/FLD_A5_MCB_de.csv',
           '_work/menu_de/BTL_REST_map.csv'):
    print('=====', os.path.basename(fn))
    seen = set()
    for l in open(fn, encoding='latin1'):
        q = l.rstrip('\r\n').split(';')
        if len(q) < 6 or l.startswith('#'):
            continue
        en, de = q[4], q[5]
        e = en.strip()
        if e and de.strip() == e and len(e) >= 3 and not is_ident(e):
            if e not in seen:
                seen.add(e)
                print('  UNTR [%2d] %r' % (len(e), e[:80]))
