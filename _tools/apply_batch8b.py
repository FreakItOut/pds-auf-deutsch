fixes = [
('"(It\'s a dining table, but..."', '(Esstisch, aber...)'),
('"(It\'s a part of a monster.)"', '(ein Teil eines Monsters.)'),
('"(It\'s hard to tell the good junk..."', '(Schwer, Schrott...)'),
('"(It\'s part of a monster..."', '(Monster-Teil...)'),
('\'(This door is locked...\'', '(Tuer verschlossen...)'),
]

# Actually, the EN keys in the map are different. Let me just match by substring.
import os
os.chdir(r'C:\Users\FreakItOut\Documents\Panzer Dragoon Saga Übersetzung')
SRC = r'_work\menu_de\TWN_SEEK_PRG_d4_map.csv'
rows = []
with open(SRC, encoding='latin1') as f:
    for line in f:
        line = line.rstrip('\r\n')
        if not line: continue
        parts = line.split(';')
        if len(parts) < 2: continue
        rows.append((parts[0], parts[1]))

# Apply fixes by matching substrings
replacements = {
    "dining table, but": "(Esstisch, aber...)",
    "part of a monster.)": "(ein Teil e. Monsters.)",
    "good junk...": "(Schwer, Schrott...)",
    "part of a monster...": "(Monster-Teil...)",
    "door is locked...": "(Tuer verschlossen...)",
}

new_rows = []
applied = 0
for en, de in rows:
    matched = False
    for key, new_de in replacements.items():
        if key in en:
            # validate length
            if len(new_de.encode('latin1')) <= len(en.encode('latin1')):
                new_rows.append((en, new_de))
                applied += 1
                matched = True
                break
            else:
                print('STILL TOO LONG:', new_de, len(new_de.encode('latin1')), '>', len(en.encode('latin1')))
    if not matched:
        new_rows.append((en, de))

with open(SRC, 'w', encoding='latin1', newline='') as f:
    for en, de in new_rows:
        f.write('%s;%s\n' % (en, de))
print('applied:', applied, 'total:', len(new_rows))