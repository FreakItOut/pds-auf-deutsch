fixes = [
("I'm Aldo and I work", "Ich bin Aldo."),
("I'm Damon, the High Priest.", "Ich bin Damon."),
("If they bring back provisions,", "Wenn Vorräte zurückbringen,"),
("If ya wanna know more,", "Wenn du mehr willst,"),
("If you still choose to desert", "Wenn noch desertieren"),
("If you want to talk,", "Wenn reden willst,"),
("It'll sell as a spice, but...", "Als Gewuerz, aber..."),
("It's our code. We must live", "Unser Kodex. Leben"),
("Leave Town", "Dorf weg"),
("No, I can't give that", "Nein, nicht geben"),
("No, I'm okay...", "Nein, okay..."),
("No, not really.", "Nein."),
("No, not really...", "Nein..."),
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
SRC = r'_work\menu_de\TWN_SEEK_PRG_d4_map.csv'
rows = []
with open(SRC, encoding='latin1') as f:
    for line in f:
        line = line.rstrip('\r\n')
        if not line: continue
        parts = line.split(';')
        if len(parts) < 2: continue
        rows.append((parts[0], parts[1]))

fixmap = dict(fixes)
new_rows = []
applied = 0
for en, de in rows:
    if en in fixmap:
        new_rows.append((en, fixmap[en]))
        applied += 1
    else:
        new_rows.append((en, de))

with open(SRC, 'w', encoding='latin1', newline='') as f:
    for en, de in new_rows:
        f.write('%s;%s\n' % (en, de))
print('applied:', applied, 'total:', len(new_rows))