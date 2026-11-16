import os, glob
os.chdir(r'C:\Users\FreakItOut\Documents\Panzer Dragoon Saga Übersetzung')

label_fixes = {
    'Disp Collision': 'Disp Kollision',
    'Buy Gun Part': 'Teil kaufen',
    'Sell Gun Part': 'Verk. Teil',
    'Switch Sell/Buy': 'Kauf/Verkauf',
}

total_fixed = 0
for pattern in ['_work/subtitles/*_de.csv', '_work/menu_de/*_de*.csv']:
    for fpath in glob.glob(pattern):
        with open(fpath, encoding='latin1') as f:
            lines = f.read().splitlines()
        new_lines = []
        fixed = 0
        for line in lines:
            if not line.strip():
                new_lines.append(line); continue
            # For menu_de files, format is file;off;prefix;len;en;de
            # For subtitles, format is uid;len;offset;offsets;en;de
            # In both cases, DE is the last field
            parts = line.split(';')
            if len(parts) >= 2:
                de = parts[-1]
                en = parts[-2] if len(parts) >= 2 else ''
                if de in label_fixes and de == en:
                    new_de = label_fixes[de]
                    if len(new_de.encode('latin1')) <= len(de.encode('latin1')):
                        parts[-1] = new_de
                        fixed += 1
            new_lines.append(';'.join(parts))
        if fixed > 0:
            with open(fpath, 'w', encoding='latin1', newline='') as f:
                for line in new_lines:
                    f.write(line + '\n')
            total_fixed += fixed
            print('%s: fixed %d' % (os.path.basename(fpath), fixed))
print('Total fixed:', total_fixed)