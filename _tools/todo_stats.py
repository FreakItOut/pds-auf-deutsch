# Sample UNTRANSLATED rows per file, filter obvious control strings
import re, glob, os

def is_translatable(en, de):
    if en.strip() != de.strip():
        return False
    e = en.strip()
    if len(e) < 3:
        return False
    if '%' in e or re.match(r'^[A-Z0-9_:, ]*$', e):
        return False
    if re.match(r'^(aim|dh|lo|hi)\b|^[a-z]{1,2}%|[0-9]{2,}$', e):
        return False
    if e in ('ITEM', 'ITEM ', 'MENU', 'BACK', 'DOOR', 'EXIT', 'LOCK', 'PULL LEVER',
             'AERODANCE', 'AC', 'TC', 'VOL CANAL', 'START', 'PAUSE', 'OPTION', 'E_WAIT', 'EYE_MOVE', 'BOX_MOVE'):
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
        elif mode == 'map' and len(p) >= 2 and i > 0:
            rows.append(('', p[0], p[1]))
    f.close()
    return rows

seen = {}
for path in sorted(glob.glob('_work/subtitles/*_de.csv')) + sorted(glob.glob('_work/menu_de/*_de*.csv')) + [
        '_work/menu_de/BTL_REST_map.csv', '_work/menu_de/CHILDMP_MCB_map.csv', '_work/menu_de/MENUEN_FNT_map.csv']:
    mode = 'sub' if 'subtitles' in path else 'menu'
    if os.path.basename(path).endswith('_de_p2.csv'):
        mode = 'menu'
    if path.endswith('_map.csv'):
        mode = 'map'
    rows = load(path, mode)
    hits = [r for r in rows if is_translatable(r[1], r[2])]
    if hits:
        print('== %s: %d untranslated-looking / %d rows' % (os.path.basename(path), len(hits), len(rows)))
        seen[os.path.basename(path)] = len(hits)
print()
print('summary:', seen)
