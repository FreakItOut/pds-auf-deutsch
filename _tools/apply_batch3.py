fixes = [
("(It's a dining table, but...)", "(Esstisch, aber...)"),
("(It's hard to tell the good junk...)", "(Schwer, Schrott...)"),
("(It's part of a monster...)", "(Monster-Teil...)"),
("(This door is locked...)", "(Tuer verschlossen...)"),
("Don't shoot!", "Schiess nicht!"),
("Drinking ain't as good when those", "Trinken macht nicht so Spass"),
("Enter", "Betreten"),
("Even if the Guardian Fire dies", "Selbst wenn Waechterfeuer stirbt"),
("Forget it... it's no big deal...", "Vergiss es... nicht der Rede wert"),
("Go through it and turn right.", "Geh hindurch, rechts ab."),
("Guardian Fire is inside", "Waechterfeuer drinnen"),
("He can leave and get swallowed by", "Er kann gehen und verschlungen werden"),
("He roams around outside the gates.", "Streift ausserhalb der Tore."),
("He used it to take the lamp down.)", "Nutze es, Lampe herunter."),
("He's an odd guy, tinkering with", "Komischer Kauz, bastelt mit"),
("He's second in", "Zweiter im"),
("Here is the key to the sanctuary.", "Schluessel zum Heiligtum."),
("Here, keep this.", "Hier, behalt das."),
("Hey boy...", "He, Junge..."),
("Hey!? That gun...", "Hey!? Diese Waffe..."),
("How can you be so relaxed", "Wie kannst du so entspannt sein"),
("I am a very busy man.", "Sehr beschaeftigter Mann."),
("I can't believe you're involved", "Kann nicht glauben, verwickelt"),
("I can't feel my legs.)", "Kann Beine nicht fuehlen.)"),
("I can't get up there.)", "Komme nicht hoch.)"),
("I can't use it, anyways.", "Kann es ohnehin nicht nutzen."),
("I did the right thing by", "Tat das Richtige, indem"),
("I don't even know", "Weiss nicht einmal"),
("I don't like outsiders.", "Mag Aussenstehende nicht."),
("I don't need your help, boy.", "Brauche Hilfe nicht, Junge."),
("I don't plan to stay in this town", "Plane nicht, in Stadt zu bleiben"),
("I don't think that will happen.", "Glaube nicht, dass das passiert."),
("I get nothing... I'm gonna quit.", "Nichts... Ich hoere auf."),
("I have no time for church.", "Keine Zeit fuer Kirche."),
("I have one.", "Habe eine."),
("I hear he's fixing a flying ship", "Hoere, repariert Flugschiff"),
("I hear that the Imperial Base", "Hoere, Reichsbasis"),
("I hear there's a passage next to the", "Hoere, Durchgang neben dem"),
("I heard that Paet's father had a", "Hoerte, Paets Vater hatte"),
("I hope we can help each other,", "Hoffe, helfen"),
("I never thought that a High Priest", "Dachte nie, Hohepriester"),
("I really don't trust him.", "Vertraue ihm nicht."),
("I see why you quit... but...", "Sehe, warum aufhoerst... aber..."),
("I see... But why are you hiding?", "Warum versteckst du dich?"),
("I see... he's gone...", "Er ist fort..."),
("I think we're in deep trouble.", "Wir sind in Schwierigkeiten."),
("I won't be able to pay you back", "Werde nicht zurueckzahlen koennen"),
("I won't stop ya.", "Halte dich nicht auf."),
("I'll give ya a discount", "Gebe Rabatt"),
("I'm Abner, the gatekeeper.", "Ich bin Abner, Torwaechter."),
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