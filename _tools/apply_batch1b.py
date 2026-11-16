fixes = [
("(A bookshelf full of valuable books.)", "(Buecherregal.)"),
("(A bookshelf... full of books.)", "(Buecherregal... Buecher.)"),
("(A complicated looking machine.)", "(Kompl. Maschine.)"),
("(A ladder was left here...", "(Leiter gelassen..."),
("(A variety of nuts are dried here.)", "(Nuesse getrocknet.)"),
("(A young man hiding in the corner.)", "(Junger Mann, Ecke.)"),
("(An ancient airship.)", "(Uraltes Luftschiff.)"),
("(An old bed sheet.)", "(Altes Bettlaken.)"),
("(An old sturdy table.)", "(Alter Tisch.)"),
("(Didn't Paet hear it?)", "(Hoerte Paet?)"),
("(Full of technical books...)", "(Tech. Buecher...)"),
("(He looks as if he's already won.)", "(Gewonnen.)"),
("(I can't trust the Imperial forces", "(Reichstruppen nicht trauen"),
("(I don't think he'll notice me.)", "(Bemerkt mich nicht.)"),
("(Is this the book I shouldn't see?)", "(Buch nicht sehen?)"),
("(It must pump the water", "(Wasser pumpen"),
("(It's a dingy looking hammock.)", "(Schmuddel-Haengem.)"),
("(It's a dining table, but...)", "(Esstisch, aber...)"),
("(It's a hammock.)", "(Haengematte.)"),
("(It's a passage to another room.)", "(Durchgang.)"),
("(It's a pot for the liquid.)", "(Topf Fluessigkeit.)"),
("(It's a room for the bar's owner.)", "(Raum Besitzer.)"),
("(It's a simple hammock...", "(Einf. Haengem..."),
("(It's a toolbox.)", "(Werkzeugkiste.)"),
("(It's a very durable desk.)", "(Stabiler Schreibt.)"),
("(It's a waterproof box.)", "(Wasserdichte Kiste.)"),
("(It's an old well...)", "(Alter Brunnen...)"),
("(It's emitting a strange light.)", "(Seltsames Licht.)"),
("(It's full of glowing liquid.)", "(Leucht. Fluess.)"),
("(It's hard to tell the good junk...)", "(Schwer, Schrott..."),
("(It's locked... I can't open it.)", "(Verschlossen.)"),
("(It's part of a monster...)", "(Monster-Teil...)"),
("(It's used for cooking.)", "(Zum Kochen.)"),
("(Looks like he's making his lunch.)", "(Macht Mittagessen.)"),
("(Looks like he's one of the leaders", "(Einer der Fuehrer"),
("(Looks like he's the owner of", "(Besitzer von"),
("(Machines are also on the desk.)", "(Maschinen, Tisch.)"),
("(More equipment?)", "(Mehr Ausruest.?)"),
("(Nice bed... but it's dirty.)", "(Schoenes Bett... schmutzig.)"),
("(No blood... a good sign.", "(Kein Blut... gut.)"),
("(Nuts have fallen to the ground.)", "(Nuesse gefallen.)"),
("(Records of Zoah.)", "(Zoah-Aufz.)"),
("(Right now, I have no choice", "(Keine Wahl"),
("(So that's the Guardian Fire...)", "(Waechterfeuer...)"),
("(Some items for traveling, but", "(Reisegegenst., aber"),
("(Some personal items, but there", "(Persoenl. Sachen, aber da"),
("(That pot is big!)", "(Grosser Topf!)"),
("(That pot is huge.)", "(Riesiger Topf.)"),
("(That stuff looks interesting.)", "(Interessantes Zeug.)"),
("(That table's seen a few bar fights.)", "(Kneipentisch.)"),
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