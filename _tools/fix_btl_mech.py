import os
os.chdir(r'C:\Users\FreakItOut\Documents\Panzer Dragoon Saga Übersetzung')
SRC = r'_work/menu_de/BTL_REST_map.csv'
lines = open(SRC, encoding='latin1').read().splitlines()
header = lines[0]
data_lines = lines[1:]

# Mechanical substitutions for BTL_REST
SUBS = [
    ('Alle ', 'All '), ('alle ', 'all '),
    ('Einheiten, ', 'Einheiten '),
    ('Schiffe, ', 'Schiffe '),
    ('verstaerken', 'verst.'),
    ('hoechste Vorsicht', 'hoechste Vors.'),
    ('Ziel erfassen', 'Ziel erf.'),
    ('scharf machen', 'scharf'),
    ('Raketen ', 'Rak. '),
    ('Plage-', 'Plage'),
    ('Angriffs', 'Angr.'),
    ('Schlachtkreuzer', 'Schlachtkr.'),
    ('Schlachtschiff', 'Schlachtsch.'),
    ('Klassen', 'Kl.'),
    ('Klasse', 'Kl.'),
    ('Geschwindigkeit', 'Geschw.'),
    ('Verteidigung', 'Vert.'),
    ('Staerke', 'St.'),
    ('Geschwindigkeit', 'Geschw.'),
    ('  ', ' '),
    ('   ', '  '),
]

fixed = 0
new_lines = [header]
for line in data_lines:
    if not line.strip():
        new_lines.append(line); continue
    parts = line.split(';', 1)
    if len(parts) < 2:
        new_lines.append(line); continue
    en, de = parts[0], parts[1]
    if len(de.encode('latin1')) <= len(en.encode('latin1')):
        new_lines.append(line); continue
    # Try mechanical shortening
    best = None; best_len = len(de.encode('latin1'))
    target = len(en.encode('latin1'))
    for old, new in SUBS:
        if old in de:
            cand = de.replace(old, new, 1)
            cb = cand.encode('latin1')
            if len(cb) <= target and len(cb) < best_len:
                best = cand; best_len = len(cb)
    # Try two subs
    if best is None:
        for old1, new1 in SUBS:
            if old1 not in de: continue
            d1 = de.replace(old1, new1, 1)
            for old2, new2 in SUBS:
                if old2 not in d1: continue
                d2 = d1.replace(old2, new2, 1)
                db2 = d2.encode('latin1')
                if len(db2) <= target and len(db2) < best_len:
                    best = d2; best_len = len(db2)
    if best is not None:
        new_lines.append(en + ';' + best)
        fixed += 1
    else:
        new_lines.append(line)

with open(SRC, 'w', encoding='latin1', newline='') as f:
    for line in new_lines:
        f.write(line + '\n')
print('mechanically fixed:', fixed)

# Count remaining
over = 0
for line in new_lines[1:]:
    parts = line.split(';', 1)
    if len(parts) >= 2:
        if len(parts[1].encode('latin1')) > len(parts[0].encode('latin1')):
            over += 1
print('remaining too-long:', over)