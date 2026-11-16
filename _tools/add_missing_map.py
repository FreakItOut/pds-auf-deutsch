import os, csv, re
os.chdir(r'C:\Users\FreakItOut\Documents\Panzer Dragoon Saga Übersetzung')

# Read EN file to get exact keys
en_keys_list = []
with open('_work/menu_de/TWN_SEEK_PRG_d4_en.csv', encoding='latin1') as f:
    rd = csv.reader(f, delimiter=';')
    next(rd)
    for r in rd:
        if len(r) >= 5:
            en_keys_list.append(r[4])

# Read map
map_lines = open('_work/menu_de/TWN_SEEK_PRG_d4_map.csv', encoding='latin1').read().splitlines()

def normalize(s):
    return re.sub(r'[.\)\s]+$', '', s.strip()).strip()

# Build normalized map: norm_key -> de
norm_to_de = {}
for line in map_lines:
    if ';' not in line:
        continue
    en, de = line.split(';', 1)
    nk = normalize(en)
    if nk not in norm_to_de:
        norm_to_de[nk] = de

# Find missing EN keys
map_en_set = set(line.split(';')[0] for line in map_lines if ';' in line)
missing = set()
for ek in en_keys_list:
    if ek not in map_en_set:
        missing.add(ek)

# Add new entries for missing keys
added = 0
for ek in missing:
    nk = normalize(ek)
    if nk in norm_to_de:
        de = norm_to_de[nk]
        # validate length
        if len(de.encode('latin1')) <= len(ek.encode('latin1')):
            map_lines.append(ek + ';' + de)
            added += 1
        else:
            print('TOO LONG:', ek, len(de), '>', len(ek))

with open('_work/menu_de/TWN_SEEK_PRG_d4_map.csv', 'w', encoding='latin1', newline='') as f:
    for line in map_lines:
        f.write(line + '\n')
print('added', added, 'new entries, missing was', len(missing))