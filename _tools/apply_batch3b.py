fixes = [
("Don't shoot!", "Schiess nicht"),
("Enter", "Betreten"),
("Even if the Guardian Fire dies", "Selbst Waechterfeuer stirbt"),
("Forget it... it's no big deal...", "Vergiss es..."),
("He can leave and get swallowed by", "Er kann gehen, verschlungen"),
("Here, keep this.", "Hier, behalt."),
("Hey boy...", "He, Junge."),
("Hey!? That gun...", "Hey!? Waffe..."),
("How can you be so relaxed", "Wie entspannt?"),
("I am a very busy man.", "Sehr beschaeftigt."),
("I can't feel my legs.)", "Beine nicht fuehlen.)"),
("I can't use it, anyways.", "Kann nicht nutzen."),
("I don't even know", "Weiss nicht."),
("I don't like outsiders.", "Mag Aussenstehende nicht"),
("I don't think that will happen.", "Glaube nicht."),
("I see why you quit... but...", "Sehe, warum..."),
("I won't be able to pay you back", "Nicht zurueckzahlen"),
("I won't stop ya.", "Nicht aufhalten."),
("I'm Abner, the gatekeeper.", "Ich bin Abner."),
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