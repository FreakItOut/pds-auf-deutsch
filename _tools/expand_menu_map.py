# Expand a unique-string map (en;de) into per-offset DE csv files.
# Matching is done on STRIPPED text (trailing spaces in EN keys ignored).
# Usage: python expand_menu_map.py <NAME> [map.csv]
# - expands _work/menu_de/<NAME>_en.csv      -> <NAME>_de.csv
# - expands _work/menu_de/<NAME>_dN_en.csv   -> <NAME>_de_dN.csv  (per disc)
# Extra rows in <NAME>_extra.csv (file;off;prefix;len;en;de[;force]) are
# appended to the main output.
import csv
import glob
import os
import sys

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

name = sys.argv[1]
map_path = (sys.argv[2] if len(sys.argv) > 2
            else f'_work/menu_de/{name}_map.csv')

mapping = {}
with open(map_path, encoding='latin1') as fh:
    for ln in fh:
        ln = ln.rstrip('\r\n')
        if not ln or ln.startswith('#') or ln.startswith('file;'):
            continue
        if ';' not in ln:
            continue
        en, de = ln.split(';', 1)
        k = en.strip()
        if k.endswith('\\n'):
            k = k[:-2].strip()
        mapping[k] = de

sources = sorted(glob.glob(f'_work/menu_de/{name}_en.csv'))
sources += sorted(glob.glob(f'_work/menu_de/{name}_d[0-9]_en.csv'))

extra_path = f'_work/menu_de/{name}_extra.csv'
extras = []
if os.path.exists(extra_path):
    with open(extra_path, encoding='latin1') as fh:
        rd = csv.reader(fh, delimiter=';')
        next(rd)
        for r in rd:
            extras.append(r)

for src in sources:
    tail = os.path.basename(src)[len(name) + 1:-7]  # '', 'd1', ...
    out = (f'_work/menu_de/{name}_de.csv' if not tail
           else f'_work/menu_de/{name}_de_{tail}.csv')
    rows = []
    missing = []
    with open(src, encoding='latin1') as fh:
        rd = csv.reader(fh, delimiter=';')
        next(rd)
        for r in rd:
            if len(r) < 5:
                continue
            key = r[4].strip()
            if key.endswith('\\n'):
                key = key[:-2].strip()
            if key not in mapping:
                missing.append(r[4])
                continue
            de = mapping[key]
            # preserve leading spaces of the EN (banner frames, indented
            # labels) unless the DE already carries them
            lead = r[4][:len(r[4]) - len(r[4].lstrip(' '))]
            if lead and not de.startswith(' '):
                if len(lead) + len(de) <= len(r[4]):
                    de = lead + de
            rows.append([r[0], r[1], r[2], r[3], r[4], de])
    if not tail:
        rows.extend(extras)
    with open(out, 'w', encoding='latin1', newline='') as fh:
        w = csv.writer(fh, delimiter=';')
        w.writerow(['file', 'off', 'prefix', 'len', 'en', 'de'])
        for r in rows:
            w.writerow(r)
    print('wrote %s: %d rows, %d missing' % (out, len(rows), len(missing)))
    for m in missing[:15]:
        print('   MISSING: %r' % m[:70])
