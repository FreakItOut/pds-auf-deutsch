fixes = [
("(It's a dining table, but...)", "(Esstisch, aber...)"),
("(It's hard to tell the good junk...)", "(Schwer, Schrott...)"),
("(It's part of a monster...)", "(Monster-Teil...)"),
("(This door is locked...)", "(Tuer verschlossen...)"),
("I'm Aldo and I work", "Ich bin Aldo, arbeite"),
("I'm Damon, the High Priest.", "Ich bin Damon, Hohepriester."),
("I'm not quite sure, but", "Nicht ganz sicher, aber"),
("I'm sorry, but... no.", "Leid, aber... nein."),
("I'm sure the High Priest wouldn't", "Hohepriester wuerde nicht"),
("I'm very sorry.", "Sehr leid."),
("I've been preparing for negotiations.", "Vorbereitet auf Verhandlungen."),
("I've heard stories from Abner.", "Hoerte Geschichten von Abner."),
("I... I'm sorry.", "Ich... leid."),
("If there is an emergency, I must", "Notfall, muss ich"),
("If they bring back provisions,", "Wenn sie Vorräte zurückbringen,"),
("If ya wanna know more,", "Wenn du mehr wissen willst,"),
("If you still choose to desert", "Wenn du noch desertieren willst"),
("If you think you can handle her.", "Wenn du sie handhaben kannst."),
("If you want to talk,", "Wenn du reden willst,"),
("In this town you don't need to", "In Stadt brauchst du nicht"),
("In time memories fade. Memories", "Erinnerungen verblassen."),
("Instead, you can go to my house", "Stattdessen zu meinem Haus"),
("Is he challenging the High", "Fordert er Hohepriester"),
("Is that why the deliveries from", "Ist das Grund, Lieferungen von"),
("Isn't it for storage?", "Zur Lagerung?"),
("It has been rebuilt.)", "Wieder aufgebaut.)"),
("It seems unlikely that any new", "Unwahrscheinlich, dass neue"),
("It shows that they are no match", "Zeigt, keine Gegner"),
("It was proposed by", "Vorgeschlagen von"),
("It'll sell as a spice, but...", "Verkauft sich als Gewuerz, aber..."),
("It's a shrine for my fallen comrades.", "Schrein fuer gefallene Kameraden."),
("It's easy to stay, but it's ", "Leicht zu bleiben, aber"),
("It's okay, take it.", "Okay, nimm es."),
("It's our code. We must live", "Unser Kodex. Wir muessen leben"),
("It's something you can't get", "Etwas, das man nicht bekommt"),
("It's such a rare gun, so...", "So seltene Waffe, so..."),
("It's the body fluid of the monsters.", "Koerperfluessigkeit der Monster."),
("It's time for us to decide who", "Zeit zu entscheiden, wer"),
("Its taste is... horrible.)", "Geschmack... schrecklich.)"),
("Leave Town", "Dorf verlassen"),
("Looks like Vaiman has granted", "Sieht aus, Vaiman gewaehrt"),
("Many hunters store ammo in them.)", "Jaeger lagern Munition.)"),
("Many times I faced death and", "Viele Male Tod gegenueber"),
("Maybe I was too hard on you.", "Vielleicht zu hart."),
("My friends were killed too...", "Freunde auch getoetet..."),
("No, I can't give that", "Nein, kann nicht geben"),
("No, I'm okay...", "Nein, mir geht's gut..."),
("No, not really.", "Nein, nicht wirklich."),
("No, not really...", "Nein, nicht wirklich..."),
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