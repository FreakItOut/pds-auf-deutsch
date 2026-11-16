fixes = [
("Not so loud, eh?", "Nicht so laut."),
("Of course.", "Natuerlich"),
("Oh, it's you...", "Oh, du..."),
("Oh, you can tell, eh?", "Oh, du sagst es, eh?"),
("Sharing it with outsiders is", "Teilen mit Aussenst. ist"),
("So, Quitor...", "Also, Quitor."),
("Some books, you shouldn't see...", "Buecher nicht sehen..."),
("Sounds crazy, don't ya think?", "Hoert sich verrueckt an?"),
("Still no, eh?", "Immer noch nein?"),
("Stop by at night.", "Komm abends."),
("Tell him Boaz said so!", "Sag, Boaz sagte das!"),
("They must be stopped at", "Gestoppt werden an"),
("Things Useful for Battle", "Dinge f. Kampf"),
("This is my home.", "Mein Zuhause."),
("This pot is big.", "Grosser Topf."),
("(This smell...", "(Geruch..."),
("To tell you the truth, I was", "Um Wahrheit zu sagen, ich"),
("Trust the outside, and...", "Vertraue Aussenwelt..."),
("Warning, accessing now...", "Warnung, Zugriff..."),
("Watch your mouth kid! Do you", "Pass auf Mund auf, Junge!"),
("We got no business in there.", "Kein Geschaeft da."),
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