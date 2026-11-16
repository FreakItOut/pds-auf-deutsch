fixes = [
("(I must end this...", "(Ich muss enden..."),
("(I remember now...", "(Ich erinnere..."),
("(It's empty.)", "(Leer.)"),
("(It's my Captain!!!)", "(Mein Chef!!!)"),
("Don't Exit", "Nicht Exit"),
("I won't leave you again.", "Ich bleibe bei dir."),
("I wonder what they're up to.", "Was treiben sie?"),
("It's a battleship's engine.)", "Schlachtschiff-Motor.)"),
("The Black Fleet was here.", "Schwarze Flotte hier."),
("ruins.", "Ruinen"),
]

ok = 0; bad = 0
for en, de in fixes:
    if len(de.encode('latin1')) <= len(en.encode('latin1')):
        ok += 1
    else:
        bad += 1
        print('STILL TOO LONG: %s (%d > %d)' % (de, len(de.encode('latin1')), len(en.encode('latin1'))))
print('ok:', ok, 'bad:', bad)

import os
os.chdir(r'C:\Users\FreakItOut\Documents\Panzer Dragoon Saga Übersetzung')
SRC = r'_work/menu_de/TWN_E059_PRG_d2_map.csv'
with open(SRC, encoding='latin1') as f:
    lines = f.read().splitlines()
fixmap = dict(fixes)
new_lines = []
applied = 0
for line in lines:
    if ';' not in line:
        new_lines.append(line); continue
    parts = line.split(';', 1)
    en = parts[0]
    if en in fixmap:
        new_lines.append(en + ';' + fixmap[en])
        applied += 1
    else:
        new_lines.append(line)
with open(SRC, 'w', encoding='latin1', newline='') as f:
    for line in new_lines:
        f.write(line + '\n')
print('applied:', applied)