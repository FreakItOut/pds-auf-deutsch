# Build translation backlog: untranslated real prose + over-short rows.
# Sources: menu maps (en;de) and expanded menu csv (file;off;len;en;de).
import glob
import os
import re

CTRL_OK = re.compile(r'^[A-Z0-9_%\-,:; .\\]*$')


def is_ctrl(en):
    e = en.strip()
    if '%' in e or not e:
        return True
    # all-caps labels: ITEM, DOOR, WND_GEAR ...
    words = e.split()
    if all((w.upper() == w and not any(c.islower() for c in w)) or w.isdigit() or w in ('', '+', '-') for w in e.replace('\n', ' ').split(' ')):
        if not re.search(r'[a-z]', e):
            return True
    # debug-ish tokens
    if re.match(r'^(E_|lrudnf|g7g8|rate:|hit_| oposi|aim)', e):
        return True
    return False


def words_from(en, de):
    return en, de


def load_map(path):
    rows = []
    with open(path, encoding='latin1') as f:
        for i, line in enumerate(f):
            if i == 0:
                continue
            p = line.rstrip('\r\n').split(';')
            if len(p) >= 2:
                rows.append((p[0], p[1]))
    return rows


def load_exp(path):
    rows = []
    with open(path, encoding='latin1') as f:
        for i, line in enumerate(f):
            if i == 0:
                continue
            p = line.rstrip('\r\n').split(';')
            if len(p) >= 6:
                rows.append((p[4], p[5]))
    return rows


out = open('_work/review_fixes/translation_backlog.txt', 'w', encoding='latin1', newline='\n')
stats = {}
for path in sorted(glob.glob('_work/menu_de/*_map.csv')) + ['_work/menu_de/BTL_REST_map.csv']:
    base = os.path.basename(path)
    if base == 'BTL_REST_map.csv' or base.startswith(('BTL_', 'CHILDMP', 'FLD_', 'TWN_', 'TUTORIAL', 'MENUEN')):
        pass
    else:
        continue
    items = load_map(path)
    untr = [x for x in items if x[0].strip() == x[1].strip() and not is_ctrl(x[0]) and len(x[0].strip()) >= 4]
    oshort = [x for x in items if x[0].strip() != x[1].strip()
              and len(x[1].strip()) and len(x[0].encode('latin1')) >= 30
              and len(x[1].encode('latin1')) < 0.5 * len(x[0].encode('latin1'))]
    toolong = [x for x in items if len(x[1].encode('latin1')) > len(x[0].encode('latin1'))]
    if untr or oshort or toolong:
        out.write('#### %s  (untr=%d oshort=%d toolong=%d)\n' % (base, len(untr), len(oshort), len(toolong)))
        stats[base] = (len(untr), len(oshort), len(toolong))
        for en, de in untr:
            out.write('UNTR    %r || de EN==DE, budget %d\n' % (en, len(en)))
        for en, de in oshort:
            out.write('SHORT   budget=%d now=%d | %r || %r\n' % (len(en), len(de), en, de))
        for en, de in toolong:
            out.write('LONG    budget=%d now=%d | %r || %r\n' % (len(en), len(de), en, de))

# expanded csv (file;off;len;en;de): used for FLD_* etc.
for path in sorted(glob.glob('_work/menu_de/FLD_*_de.csv')) + ['_work/menu_de/TUTORIAL_CGB_de.csv',
                                                              '_work/menu_de/CHILDMP_MCB_de.csv',
                                                              '_work/menu_de/MENUEN_FNT_de.csv',
                                                              '_work/menu_de/MENU_SCB_de_p2.csv']:
    base = os.path.basename(path)
    items = load_exp(path)
    untr = [x for x in items if x[0].strip() == x[1].strip() and not is_ctrl(x[0]) and len(x[0].strip()) >= 4]
    oshort = [x for x in items if x[0].strip() != x[1].strip()
              and len(x[1].strip()) and len(x[0].encode('latin1')) >= 30
              and len(x[1].encode('latin1')) < 0.5 * len(x[0].encode('latin1'))]
    if untr or oshort:
        out.write('#### %s  (untr=%d oshort=%d)\n' % (base, len(untr), len(oshort)))
        stats[base] = (len(untr), len(oshort), 0)
        for en, de in untr:
            out.write('UNTR    %r || budget %d\n' % (en, len(en)))
        for en, de in oshort:
            out.write('SHORT   budget=%d now=%d | %r || %r\n' % (len(en), len(de), en, de))
out.close()
print('written backlog; totals:')
tot_untr = tot_short = tot_long = 0
for k in sorted(stats):
    u, s, l = stats[k]
    print('  %-24s untr=%4d short=%4d long=%4d' % (k, u, s, l))
    tot_untr += u
    tot_short += s
    tot_long += l
print('TOTAL untr=%d short=%d long=%d' % (tot_untr, tot_short, tot_long))
