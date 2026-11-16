# Dump all remaining untranslated entries with length budgets
import re, glob, os

def is_unclear(en, de):
    if en.strip() != de.strip():
        return False
    e = en.strip()
    if len(e) < 3 or '%' in e or re.match(r'^[A-Z0-9_:, ]*$', e):
        return False
    return len(e) >= 5

def load(path, mode):
    rows = []
    f = open(path, encoding='latin1')
    for i, line in enumerate(f):
        line = line.rstrip('\r\n')
        if not line:
            continue
        p = line.split(';')
        if mode == 'sub' and len(p) >= 6:
            rows.append((p[0], p[4], p[5]))
        elif mode == 'menu' and len(p) >= 6 and i > 0:
            rows.append((p[1], p[4], p[5]))
    f.close()
    return rows

for path in sorted(glob.glob('_work/subtitles/*_de.csv')) + sorted(glob.glob('_work/menu_de/*_de.csv')) + ['_work/menu_de/BTL_REST_map.csv']:
    mode = 'sub' if 'subtitles' in path else 'menu'
    if path.endswith('_map.csv'):
        mode = 'menu'  # en;de -> p0,p1 special
        f = open(path, encoding='latin1'); rows = []
        for i, line in enumerate(f):
            if i == 0: continue
            p = line.rstrip().split(';')
            if len(p) >= 2: rows.append(('', p[0], p[1]))
        f.close()
        mode_used = 'map'
    else:
        rows = load(path, mode); mode_used = mode
    hits = [r for r in rows if is_unclear(r[1], r[2])]
    if not hits:
        continue
    print('==== %s' % os.path.basename(path))
    for rid, en, de in hits:
        print('   id=%s lenEN=%3d | %r | de: %r' % (rid, len(en), en[:120], de[:60]))
