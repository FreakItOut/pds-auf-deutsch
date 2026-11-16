fixes = [
("Not so loud, eh?", "Nicht so laut, eh?"),
("Now, I have an offer for you.", "Nun, Angebot fuer dich."),
("Of course, I shall reward you", "Natuerlich belohne ich dich"),
("Of course.", "Natuerlich."),
("Oh, it's you...", "Oh, du bist es..."),
("Oh, you can tell, eh?", "Oh, du kannst es sagen, eh?"),
("Please deliver us from evil.", "Befreie uns vom Boesen."),
("Please reconsider.", "Bitte ueberlege."),
("Sharing it with outsiders is", "Teilen mit Aussenstehenden ist"),
("She was approved by the", "Genehmigt von der"),
("She's just healthy.", "Sie ist gesund."),
("So our people went into the", "Unsere Leute gingen in die"),
("So, Quitor...", "Also, Quitor..."),
("So, you're interested in my library?", "Interessierst dich fuer Bibliothek?"),
("Some books, you shouldn't see...", "Buecher, die du nicht sehen solltest..."),
("Sounds crazy, don't ya think?", "Hoert sich verrueckt an, nicht?"),
("Still no, eh?", "Immer noch nein, eh?"),
("Stop by at night.", "Komm abends vorbei."),
("Take any old book you like.", "Nimm jedes alte Buch."),
("Take them, if you want.", "Nimm sie, wenn willst."),
("Tell him Boaz said so!", "Sag ihm, Boaz sagte das!"),
("Thanks! Now I can buy food!", "Danke! Kann Essen kaufen!"),
("That girl just won't keep still...", "Maedchen bleibt nicht still..."),
("The Imperial force is nearby,", "Reichstruppen in Naehe,"),
("Their own ships are shooting", "Eigene Schiffe schiessen"),
("Then I must resort to more", "Dann muss ich zu mehr"),
("There was a fight with some", "Es gab Kampf mit einigen"),
("These crops all belong to the", "Diese Ernten gehoeren dem"),
("They must be stopped at", "Sie muessen gestoppt werden an"),
("Things Useful for Battle", "Dinge nuetzlich fuer Kampf"),
("This Liberal District ain't too bad", "Liberaler Bezirk nicht so schlecht"),
("This is my home.", "Das ist mein Zuhause."),
("This neutralizes the monsters' acid.", "Neutralisiert Saeure der Monster."),
("This one needs repairs.)", "Muss repariert werden.)"),
("This pot contains medicine.)", "Topf enthaelt Medizin.)"),
("This pot is big.", "Dieser Topf ist gross."),
("(This smell...", "(Dieser Geruch..."),
("This town has a rich heritage", "Stadt hat reiches Erbe"),
("This well has been dry for years.", "Brunnen seit Jahren trocken."),
("To tell you the truth, I was", "Um Wahrheit zu sagen, ich war"),
("Trust the outside, and...", "Vertraue Aussenwelt, und..."),
("Vaiman, the new High Priest.", "Vaiman, neuer Hohepriester."),
("Warning, accessing now...", "Warnung, Zugriff laeuft..."),
("Watch your mouth kid! Do you", "Pass auf Mund auf, Junge! Tust du"),
("We got no business in there.", "Wir haben da nichts zu suchen."),
("We've got the dragon here, ya know.", "Wir haben Drachen hier, weisst du."),
]

# Fix the (This smell... entry which was in original batch as (This smell...|
fixes = [f for f in fixes if not (f[0] == "(This smell..." and f[1] == "(Dieser Geruch...")]
fixes.append(("(This smell...", "(Dieser Geruch..."))

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