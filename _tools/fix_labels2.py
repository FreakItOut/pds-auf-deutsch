import os
os.chdir(r'C:\Users\FreakItOut\Documents\Panzer Dragoon Saga Übersetzung')

# Fix too-long labels
fixes = {
    'TWN_CAMP_PRG_de.csv': {
        'Sell Gun Part': 'Verk. Teil',
    },
    'TWN_RUIN_PRG_de.csv': {
        'Sell Gun Part': 'Verk. Teil',
        'Defense is as': 'Vert. ist wie',
    },
}

for fn, fixmap in fixes.items():
    src = '_work/subtitles/' + fn
    lines = open(src, encoding='latin1').read().splitlines()
    new_lines = []
    applied = 0
    for line in lines:
        if not line:
            new_lines.append(line); continue
        parts = line.split(';')
        if len(parts) < 6:
            new_lines.append(line); continue
        en = parts[4]
        if en in fixmap:
            new_de = fixmap[en]
            if len(new_de.encode('latin1')) <= len(en.encode('latin1')):
                parts[5] = new_de
                applied += 1
            else:
                print('STILL TOO LONG:', fn, en, len(new_de), '>', len(en))
        new_lines.append(';'.join(parts))
    with open(src, 'w', encoding='latin1', newline='') as f:
        for line in new_lines:
            f.write(line + '\n')
    print(fn, 'applied:', applied)