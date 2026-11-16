fixes = [
("(...A body something's fed on.)", "(...Etwas frass den Koerper.)"),
("(He would have wanted a", "(Er haette einen wollen"),
("(I must end this...", "(Ich muss das beenden..."),
("(I remember now...", "(Ich erinnere mich..."),
("(It's Radgam, the hunter.", "(Es ist Radgam, Jaeger."),
("(It's empty.)", "(Es ist leer.)"),
("(It's my Captain!!!)", "(Es ist mein Chef!!!)"),
("...How did I survive the fall?)", "...Wie ueberlebte ich Sturz?)"),
("But I never walked the land.", "Aber nie das Land betreten."),
("Don't Exit", "Nicht verlassen"),
("I won't leave you again.", "Ich verlasse dich nicht wieder."),
("I wonder what they're up to.", "Ich frage mich, was sie treiben."),
("It's a battleship's engine.)", "Motor eines Schlachtschiffs.)"),
("The Black Fleet was here.", "Die schwarze Flotte war hier."),
("They have really outdone", "Sie haben uebertroffen"),
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