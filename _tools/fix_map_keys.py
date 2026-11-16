import os, csv, re
os.chdir(r'C:\Users\FreakItOut\Documents\Panzer Dragoon Saga Übersetzung')

# Read EN file to get exact keys
en_keys = set()
with open('_work/menu_de/TWN_SEEK_PRG_d4_en.csv', encoding='latin1') as f:
    rd = csv.reader(f, delimiter=';')
    next(rd)
    for r in rd:
        if len(r) >= 5:
            en_keys.add(r[4])

# Read map
map_lines = open('_work/menu_de/TWN_SEEK_PRG_d4_map.csv', encoding='latin1').read().splitlines()

def normalize(s):
    return re.sub(r'[.\)\s]+$', '', s.strip()).strip()

# Build normalized map
norm_map = {}
for i, line in enumerate(map_lines):
    if ';' not in line:
        continue
    en, de = line.split(';', 1)
    norm_map.setdefault(normalize(en), []).append(i)

# For each EN key not in map, find best match and update map
added = 0
for ek in en_keys:
    # check if exact match exists
    exact = any(line.startswith(ek + ';') for line in map_lines)
    if exact:
        continue
    # find normalized match
    nk = normalize(ek)
    if nk in norm_map:
        idx = norm_map[nk][0]
        # update the EN key in that line
        old_line = map_lines[idx]
        de = old_line.split(';', 1)[1]
        map_lines[idx] = ek + ';' + de
        added += 1

with open('_work/menu_de/TWN_SEEK_PRG_d4_map.csv', 'w', encoding='latin1', newline='') as f:
    for line in map_lines:
        f.write(line + '\n')
print('updated', added, 'map entries')