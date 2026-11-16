fixes = [
("(It's a dining table, but...)", "(Esstisch, aber...)"),
("(It's hard to tell the good junk...)", "(Schwer, Schrott...)"),
("(It's part of a monster...)", "(Monster-Teil...)"),
("(This door is locked...)", "(Tuer verschlossen...)"),
("This smell...", "(Geruch..."),
("fight. You can just stay here and", "kaempfen. Du kannst hier bleiben und"),
("from the bad.)", "von dem Schlechten.)"),
("future citizen of the Holy District.", "zukuenftiger Buerger Heil. Bez."),
("giving up, right?", "gibst du auf?"),
("gods, and you still come to pray?", "Goetter, und du betest trotzdem?"),
("hard to leave.", "schwer zu verlassen."),
("know it's safe again.", "weiss, dass es sicher ist."),
("know who I am? I am Aldo,", "weiss, wer ich bin? Ich bin Aldo,"),
("leave this town.", "verlasse diese Stadt."),
("leaving me, and one other...", "laesst mich und einen anderen..."),
("make a deal with the Empire. To", "Abkommen mit Reich zu treffen. Um"),
("may have to sell information about", "vielleicht Informationen verkaufen ueber"),
("me a favor and convince him", "mir Gefallen und ueberzeuge ihn"),
("monsters for all I care.", "Monster, wen interessiert's."),
("next to someone who was killed.", "neben jemandem, getoetet."),
("on duty, okay?", "im Dienst, okay?"),
("once a hunter like you.", "einmal Jaeger wie du."),
("one of the chosen champions.", "einer der auserwaehlten Champions."),
("out, the town will be safe. As", "raus, Stadt sicher. Sobald"),
("outsider! Go away!", "Aussenstehender! Geh weg!"),
("pay your dues.", "deine Schulden bezahlen."),
("prophesy would come true.", "Prophezeiung wuerde wahr."),
("protecting this town is also", "Stadt schuetzen ist auch"),
("risking our lives for some old junk?", "Leben fuer alten Schrott riskieren?"),
("see a wall. Go right along the wall.", "siehst Wand. Rechts entlang."),
("so long. We are unlike", "solange. Wir sind ungleich"),
("some new weapon that can destroy", "neue Waffe, die zerstoeren kann"),
("some of it is partially covered,", "einiges teilweise bedeckt,"),
("than ya think, ya know.", "als du denkst, weisst du."),
("that this town was paradise, right?", "dass Stadt Paradies war, oder?"),
("that's the last thing you want.", "das ist Letzte, das du willst."),
("the Empire won't attack again.", "Reich greift nicht wieder an."),
("the Gods must protect this town,", "Goetter muessen Stadt schuetzen,"),
("the Gods will protect us.", "Goetter werden uns schuetzen."),
("the Gods!", "die Goetter!"),
("the Gods.", "die Goetter."),
("the High Priest hasn't come home.", "Hohepriester nicht nach Hause."),
("the options available to us.", "Optionen, die uns zur Verfuegung."),
("the outside.", "die Aussenwelt."),
("them, but most are rejected.", "sie, aber die meisten abgelehnt."),
("this town I would be forced to ", "diese Stadt wuerde ich gezwungen"),
("those ruthless, lawless outsiders.", "diese ruchlosen, gesetzlosen."),
("to touch another weapon.", "eine weitere Waffe anzufassen."),
("why are they here?)", "warum sind sie hier?)"),
("will be the next High Priest.", "wird naechster Hohepriester."),
("with my son Paet. Can you do", "mit Sohn Paet. Kannst du"),
("would bend the rules.", "wuerde Regeln beugen."),
("you a pass.", "dir einen Pass."),
("you can ask him yourself.", "du kannst ihn selbst fragen."),
("you'll never see that money again.", "du wirst Geld nie wieder sehen."),
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