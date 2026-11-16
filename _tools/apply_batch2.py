fixes = [
("(It's a dining table, but...)", "(Esstisch, aber...)"),
("(It's hard to tell the good junk...)", "(Schwer, Schrott..."),
("(It's part of a monster...)", "(Monster-Teil...)"),
("(The base of a lamp...)", "(Lampensockel...)"),
("(The door is blocked by the tables.)", "(Tuer blockiert.)"),
("(The gate is closed...)", "(Tor geschlossen...)"),
("(The glowing drink stained the table.)", "(Leucht. Getraenk befleckte Tisch.)"),
("(The grain is for sale.)", "(Korn zu verkaufen.)"),
("(The land here is fertile.)", "(Boden fruchtbar.)"),
("(The pleasant aroma of incense.)", "(Duft von Weihrauch.)"),
("(The pots are covered with lids.)", "(Toepfe mit Deckeln.)"),
("(The pots contain grain and water.)", "(Toepfe: Korn u. Wasser.)"),
("(The pottery is unglazed.)", "(Unglasierte Toepferware.)"),
("(The sound of rushing water.", "(Fliessendes Wasser.)"),
("(The stairs are blocked...", "(Treppe blockiert..."),
("(The tables are set aside.)", "(Tische beiseite.)"),
("(There are items on sale...)", "(Gegenst. zum Verkauf...)"),
("(There's a lamp on the desk.)", "(Lampe auf Schreibtisch.)"),
("(There's a well over the wall.)", "(Brunnen ueber Wand.)"),
("(There's lamp on the desk.)", "(Lampe auf Tisch.)"),
("(These pots are plain but durable.)", "(Toepfe schlicht, haltbar.)"),
("(These pots are unglazed.)", "(Toepfe unglasiert.)"),
("(They killed Kenny.)", "(Sie toeteten Kenny.)"),
("(They're hunter's tools.", "(Jaegerwerkzeuge.)"),
("(This door is locked...)", "(Tuer verschlossen...)"),
("(This lamp looks valuable.)", "(Wertvolle Lampe.)"),
("(This looks almost too big to move.)", "(Zu gross zum Bewegen.)"),
("(This one needs repairs.)", "(Muss repariert werden.)"),
("(This place makes more money", "(Mehr Geld hier"),
("(This pot contains medicine.)", "(Topf mit Medizin.)"),
("(This pot is big.", "(Grosser Topf."),
("(This smell...", "(Dieser Geruch..."),
("(This well has been dry for years.", "(Brunnen trocken seit Jahren."),
("(What a dirty sheet...)", "(Schmutziges Laken...)"),
("A black ship? Is it nearby?", "Schwarzes Schiff? Naehe?"),
("A blessed gun for a good hunt?)", "Gesegn. Waffe?"),
("A broken device and some fluid.)", "Kaputtes Geraet u. Fluessigkeit.)"),
("All right... But I don't want you", "Na gut... Aber ich will nicht"),
("And he gives me exactly what I need.", "Gibt mir was ich brauche."),
("Are ya sure? Looks like you're", "Bist du sicher? Du siehst aus, als"),
("Are ya sure? Looks to me like", "Bist du sicher? Fuer mich"),
("Are you sure we can trust him?", "Ihm trauen?"),
("As long as they pay, ya know.", "Solange sie zahlen."),
("At least the troops would buy drinks.", "Truppen kauften Drinks."),
("Books on the Dragon", "Buecher ueber Drachen"),
("But, to rule, we need a legend.", "Zum Herrschen: Legende."),
("Call me a coward if you want.", "Nenn mich Feigling."),
("Did you hear about the black ship?", "Hoertest du vom schwarzen Schiff?"),
("Do you think it's because we never", "Denkst du, wir nie"),
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