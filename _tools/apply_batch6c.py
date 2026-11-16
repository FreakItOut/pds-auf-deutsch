fixes = [
("When I close my eyes, I can still", "Wenn Augen schliesse, noch"),
("Why would he...", "Warum wuerde er..."),
("You can stay here if you want.", "Du kannst bleiben, wenn"),
("You need not thank me,", "Brauchst nicht danken,"),
("You scared the $#!+ outta me!", "Du hast mir Schreck!"),
("You'd better leave this town, if", "Du solltest Stadt besser verlassen"),
("Your town isn't my responsibility.", "Deine Stadt nicht meine Resp."),
("a real man.", "echter Mann"),
("about the black ship?", "schwarzes Schiff?"),
("airship?", "Luftsch."),
("all costs!", "jeden Preis"),
("and you look so calm.", "und ruhig aus."),
("but I can't hear.)", "kann nicht hoeren"),
("but it is still a mess.)", "immer Durcheinander.)"),
("destroy us all.", "uns alle zerstoeren"),
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