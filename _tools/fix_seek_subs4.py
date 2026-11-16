import os
os.chdir(r'C:\Users\FreakItOut\Documents\Panzer Dragoon Saga Übersetzung')

fixes = {
    "(Didn't Paet hear it?)": "(Hoerte Paet?)",
    "You need not thank me,": "Brauchst nicht danken,",
}

src = '_work/subtitles/TWN_SEEK_PRG_de.csv'
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
    if en in fixes:
        new_de = fixes[en]
        if len(new_de.encode('latin1')) <= len(en.encode('latin1')):
            parts[5] = new_de
            applied += 1
        else:
            print('TOO LONG:', en, len(new_de), '>', len(en))
    new_lines.append(';'.join(parts))
with open(src, 'w', encoding='latin1', newline='') as f:
    for line in new_lines:
        f.write(line + '\n')
print('applied:', applied)