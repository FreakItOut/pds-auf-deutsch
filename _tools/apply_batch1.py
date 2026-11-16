# Batch 1 fixes for TWN_SEEK d4
fixes = [
("(A bookshelf full of valuable books.)", "(Buecherregal voller Buecher.)"),
("(A bookshelf... full of books.)", "(Buecherregal... voller Buecher.)"),
("(A complicated looking machine.)", "(Kompliziert aussehende Maschine.)"),
("(A ladder was left here...", "(Leiter wurde hier gelassen..."),
("(A variety of nuts are dried here.)", "(Verschiedene Nuesse getrocknet.)"),
("(A young man hiding in the corner.)", "(Junger Mann in der Ecke.)"),
("(An ancient airship.)", "(Uraltes Luftschiff.)"),
("(An old bed sheet.)", "(Altes Bettlaken.)"),
("(An old sturdy table.)", "(Alter, stabiler Tisch.)"),
("(Didn't Paet hear it?)", "(Hoerte Paet das nicht?)"),
("(Full of technical books...)", "(Voller technischer Buecher...)"),
("(He looks as if he's already won.)", "(Wirkt, als haette er gewonnen.)"),
("(I can't trust the Imperial forces", "(Ich kann Reichstruppen nicht trauen"),
("(I don't think he'll notice me.)", "(Ich glaube, er bemerkt mich nicht.)"),
("(Is this the book I shouldn't see?)", "(Ist das das Buch, das ich nicht sehen soll?)"),
("(It must pump the water", "(Es muss das Wasser pumpen"),
("(It's a dingy looking hammock.)", "(Schmuddelige Haengematte.)"),
("(It's a dining table, but...)", "(Es ist ein Esstisch, aber...)"),
("(It's a hammock.)", "(Haengematte.)"),
("(It's a passage to another room.)", "(Durchgang zu anderem Raum.)"),
("(It's a pot for the liquid.)", "(Topf fuer die Fluessigkeit.)"),
("(It's a room for the bar's owner.)", "(Raum fuer Besitzer der Bar.)"),
("(It's a simple hammock...", "(Einfache Haengematte..."),
("(It's a toolbox.)", "(Werkzeugkiste.)"),
("(It's a very durable desk.)", "(Sehr stabiler Schreibtisch.)"),
("(It's a waterproof box.)", "(Wasserdichte Kiste.)"),
("(It's an old well...)", "(Alter Brunnen...)"),
("(It's emitting a strange light.)", "(Sendet seltsames Licht aus.)"),
("(It's full of glowing liquid.)", "(Voller leuchtender Fluessigkeit.)"),
("(It's hard to tell the good junk...)", "(Schwer, guten Schrott zu erkennen...)"),
("(It's locked... I can't open it.)", "(Verschlossen... Ich krieg es nicht auf.)"),
("(It's part of a monster...)", "(Teil eines Monsters...)"),
("(It's used for cooking.)", "(Zum Kochen benutzt.)"),
("(Looks like he's making his lunch.)", "(Sieht aus, als mache er Mittagessen.)"),
("(Looks like he's one of the leaders", "(Sieht aus, als sei er einer der Fuehrer"),
("(Looks like he's the owner of", "(Sieht aus, als sei er Besitzer von"),
("(Machines are also on the desk.)", "(Auch Maschinen auf dem Schreibtisch.)"),
("(More equipment?)", "(Mehr Ausruestung?)"),
("(Nice bed... but it's dirty.)", "(Schoenes Bett... aber schmutzig.)"),
("(No blood... a good sign.", "(Kein Blut... ein gutes Zeichen."),
("(Nuts have fallen to the ground.)", "(Nuesse auf den Boden gefallen.)"),
("(Records of Zoah.)", "(Aufzeichnungen von Zoah.)"),
("(Right now, I have no choice", "(Gerade jetzt keine Wahl"),
("(So that's the Guardian Fire...)", "(Also, das ist das Waechterfeuer...)"),
("(Some items for traveling, but", "(Einige Reisegegenstaende, aber"),
("(Some personal items, but there", "(Einige persoenliche Sachen, aber da"),
("(That pot is big!)", "(Dieser Topf ist gross!)"),
("(That pot is huge.)", "(Der Topf ist riesig.)"),
("(That stuff looks interesting.)", "(Das Zeug sieht interessant aus.)"),
("(That table's seen a few bar fights.)", "(Der Tisch sah Kneipenschlaegereien.)"),
]

ok = 0; bad = 0
for en, de in fixes:
    if len(de.encode('latin1')) <= len(en.encode('latin1')):
        ok += 1
    else:
        bad += 1
        print('STILL TOO LONG: %s (%d > %d)' % (de, len(de.encode('latin1')), len(en.encode('latin1'))))
print('ok:', ok, 'bad:', bad)

# Apply to map file
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