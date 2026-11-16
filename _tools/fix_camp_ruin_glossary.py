import csv, os, re
os.chdir(r'C:\Users\FreakItOut\Documents\Panzer Dragoon Saga Übersetzung')

# Fix glossary in both CAMP and RUIN
for fn in ['TWN_CAMP_PRG_de.csv', 'TWN_RUIN_PRG_de.csv']:
    src = '_work/subtitles/' + fn
    lines = open(src, encoding='latin1').read().splitlines()
    new_lines = []
    fixed = 0
    for line in lines:
        if not line:
            new_lines.append(line); continue
        parts = line.split(';')
        if len(parts) < 6:
            new_lines.append(line); continue
        # Reconstruct: uid;len;offset;offsets;en;de
        de = parts[5]
        new_de = de
        if 'Imperium' in de or 'imperium' in de.lower():
            new_de = new_de.replace('Imperium', 'Reich').replace('imperium', 'Reich')
        if 'Altertum' in de or 'altertum' in de.lower():
            new_de = new_de.replace('Altertum', 'Vorzeit').replace('altertum', 'Vorzeit')
        if 'Kapit' in de or 'kapit' in de.lower():
            new_de = re.sub(r'Kapit[aä]n', 'Chef', new_de, flags=re.IGNORECASE)
        if new_de != de:
            # Validate length
            en = parts[4]
            if len(new_de.encode('latin1')) <= len(en.encode('latin1')):
                parts[5] = new_de
                fixed += 1
            else:
                # Try shorter
                pass
        new_lines.append(';'.join(parts))
    with open(src, 'w', encoding='latin1', newline='') as f:
        for line in new_lines:
            f.write(line + '\n')
    print(fn, 'glossary fixed:', fixed)