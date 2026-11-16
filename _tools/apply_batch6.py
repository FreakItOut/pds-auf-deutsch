fixes = [
("(This smell...", "(Geruch..."),
("Well, whatever those guys wanna", "Nun, was diese Kerle wollen"),
("Well, you wouldn't understand.", "Nun, du wuerdest nicht verstehen."),
("What!? You wouldn't!?", "Was!? Du wuerdest nicht!?"),
("What, you didn't know?", "Was, wusstest nicht?"),
("When I close my eyes, I can still", "Wenn ich Augen schliesse, kann ich noch"),
("Why don't you ask her out?", "Warum fragst du sie nicht aus?"),
("Why not let 'em take over this town?", "Warum ueberlaesst man sie nicht?"),
("Why would he want to leave?", "Warum wuerde er gehen?"),
("Why would he...", "Warum wuerde er..."),
("Why would they give one to you?", "Warum wuerden sie dir einen geben?"),
("Yes, I know.", "Ja, ich weiss."),
("You came here because you heard", "Du kamst, weil du hoertest"),
("You can stay here if you want.", "Du kannst hier bleiben, wenn willst."),
("You got guts, I like ya.", "Du hast Mumm, mag dich."),
("You may have your business, but...", "Du magst Geschaeft haben, aber..."),
("You must be new here, eh?", "Du musst neu hier sein, eh?"),
("You must have made some", "Du musst etwas gemacht haben"),
("You need not thank me,", "Du brauchst mir nicht danken,"),
("You scared the $#!+ outta me!", "Du hast mir Schrecken eingejagt!"),
("You should leave this town.", "Du solltest Stadt verlassen."),
("You wanna drink, son?", "Willst du trinken, Junge?"),
("You want it? It's yours.", "Du willst es? Deins."),
("You'd better leave this town, if", "Du solltest Stadt besser verlassen, wenn"),
("Your town isn't my responsibility.", "Deine Stadt nicht meine Verantwortung."),
("a real man.", "ein echter Mann."),
("about the black ship?", "ueber schwarzes Schiff?"),
("airship?", "Luftschiff?"),
("all costs!", "um jeden Preis!"),
("ambushed by a horde of monsters.", "von Horde Monster ueberfallen."),
("and you look so calm.", "und du siehst ruhig aus."),
("are here to protect us.", "sind hier, uns zu schuetzen."),
("are lots of toys too.)", "sind auch viele Spielsachen.)"),
("ask you to follow my orders.", "bitte dich, Befehlen zu folgen."),
("attacked the Empire.", "griffen das Reich an."),
("burn a bible would be Paet...)", "Bibel zu verbrennen waere Paet..."),
("but I can't hear.)", "aber kann nicht hoeren.)"),
("but it is still a mess.)", "aber immer noch Durcheinander.)"),
("but it looks fragile.)", "doch wirkt zerbrechlich.)"),
("but to listen to this man.)", "sondern diesem Mann hoeren.)"),
("buy them with money. You work", "kaufe mit Geld. Du arbeitest"),
("by a dragon.", "von einem Drachen."),
("called a recording machine.", "genannt Aufzeichnungsmaschine."),
("destroy us all.", "uns alle zu zerstoeren."),
("earn a living. It's safer that way.", "zum Leben zu verdienen. Sicherer."),
("ensure the safety of my people, I", "Sicherheit meines Volkes, ich"),
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