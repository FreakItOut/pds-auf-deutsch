fixes = [
("fight. You can just stay here and", "kaempfen. Du kannst hier bleiben"),
("from the bad.)", "von dem Schlechten)"),
("hard to leave.", "schwer zu verlassen"),
("know it's safe again.", "weiss, dass sicher."),
("know who I am? I am Aldo,", "weiss, wer ich bin? Aldo,"),
("leave this town.", "verlasse Stadt."),
("leaving me, and one other...", "laesst mich und einen..."),
("make a deal with the Empire. To", "Abkommen mit Reich. Um"),
("may have to sell information about", "vielleicht Info verkaufen ueber"),
("me a favor and convince him", "mir Gefallen, ueberzeuge ihn"),
("monsters for all I care.", "Monster, wen interessiert."),
("on duty, okay?", "im Dienst, ok?"),
("one of the chosen champions.", "einer der auserwaehlten Champs."),
("outsider! Go away!", "Aussenstehender! Geh!"),
("pay your dues.", "Schulden bezahlen."),
("so long. We are unlike", "solange. Wir ungleich"),
("than ya think, ya know.", "als du denkst, weisst."),
("the Gods will protect us.", "Goetter schuetzen uns."),
("the Gods!", "Goetter!"),
("the Gods.", "Goetter."),
("the options available to us.", "Optionen fuer uns."),
("the outside.", "Aussenwelt."),
("them, but most are rejected.", "sie, meist abgelehnt."),
("this town I would be forced to ", "Stadt, gezwungen"),
("to touch another weapon.", "weitere Waffe anfassen."),
("why are they here?)", "warum hier?)"),
("you a pass.", "dir Pass."),
("you can ask him yourself.", "du kannst ihn fragen."),
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