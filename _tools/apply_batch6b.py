fixes = [
("Well, you wouldn't understand.", "Nun, wuerdest nicht verstehen."),
("What!? You wouldn't!?", "Was!? Nicht!?"),
("When I close my eyes, I can still", "Wenn Augen schliesse, kann ich noch"),
("Why don't you ask her out?", "Warum fragst du nicht aus?"),
("Why would he...", "Warum wuerde er..."),
("Why would they give one to you?", "Warum geben sie dir einen?"),
("Yes, I know.", "Ja, weiss."),
("You can stay here if you want.", "Du kannst bleiben, wenn willst."),
("You must be new here, eh?", "Du musst neu hier sein?"),
("You must have made some", "Du musst etwas gemacht"),
("You need not thank me,", "Brauchst mir nicht danken,"),
("You scared the $#!+ outta me!", "Du hast mir Schreck eingejagt!"),
("You should leave this town.", "Du solltest Stadt verlassen"),
("You wanna drink, son?", "Willst du trinken?"),
("You'd better leave this town, if", "Du solltest Stadt besser verlassen"),
("Your town isn't my responsibility.", "Deine Stadt nicht meine Verantwortung"),
("a real man.", "echter Mann."),
("about the black ship?", "ueber schwarzes Schiff?"),
("airship?", "Luftschiff?"),
("all costs!", "jeden Preis!"),
("and you look so calm.", "und du siehst ruhig aus"),
("are here to protect us.", "hier, uns schuetzen."),
("are lots of toys too.)", "viele Spielsachen.)"),
("ask you to follow my orders.", "bitte, Befehlen zu folgen."),
("attacked the Empire.", "griffen Reich an."),
("burn a bible would be Paet...)", "Bibel verbrennen waere Paet..."),
("but I can't hear.)", "kann nicht hoeren.)"),
("but it is still a mess.)", "immer noch Durcheinander.)"),
("but it looks fragile.)", "wirkt zerbrechlich.)"),
("but to listen to this man.)", "sondern diesem Mann hoeren)"),
("by a dragon.", "von Drachen."),
("called a recording machine.", "Aufzeichnungsmaschine."),
("destroy us all.", "uns alle zerstoeren."),
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