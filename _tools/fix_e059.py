fixes = [
("(...A body something's fed on.)", "(...Etwas frass diesen Koerper.)"),
("(...All the valuable items are gone.", "(...Alle wertvollen Gegenst. weg."),
("(An old Container.)", "(Alter Behaelter.)"),
("(Empty eye sockets stare at you...)", "(Leere Augenhoehlen starren...)"),
("(He would have wanted a", "(Er haette eine haben wollen"),
("(I must end this...", "(Ich muss das beenden..."),
("(I remember now...", "(Ich erinnere mich..."),
("(It's Radgam, the hunter.", "(Es ist Radgam, der Jaeger."),
("(It's a mangled corpse...)", "(Zerfetzter Leichnam...)"),
("(It's empty.)", "(Es ist leer.)"),
("(It's my Captain!!!)", "(Es ist mein Chef!!!)"),
("(The bridge was destroyed...", "(Bruecke zerstoert..."),
("(The entrance is blocked by rubble.)", "(Eingang durch Schutt blockiert.)"),
("...How did I survive the fall?)", "...Wie ueberlebte ich den Sturz?)"),
("But I never walked the land.", "Aber ich betrat nie das Land."),
("Don't Exit", "Nicht verlassen"),
("His severed hand still grips a gun.", "Seine abgetrennte Hand haelt Waffe."),
("I won't leave you again.", "Ich verlasse dich nicht wieder."),
("I wonder what they're up to.", "Ich frage mich, was sie treiben."),
("If only I'd gotten here sooner.", "Haette ich frueher gefunden."),
("It's a battleship's engine.)", "Motor eines Schlachtschiffs.)"),
("Looks like he's waiting for me...)", "Sieht aus, als warte er..."),
("That madman shot me off the bridge.", "Dieser Wahnsinnige schoss mich."),
("The Black Fleet was here.", "Die schwarze Flotte war hier."),
("They have really outdone", "Sie haben wirklich uebertroffen"),
("but I can't be afraid forever.", "aber nicht ewig Angst haben."),
("ruins.", "Ruinen."),
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
# Read as text
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