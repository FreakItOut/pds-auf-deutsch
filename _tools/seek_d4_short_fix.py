# Re-translate the over-short d4-map rows (examine/shop texts, sentence fragments)
path = '_work/menu_de/TWN_SEEK_PRG_d4_map.csv'
FIX = {
    '(A bookshelf full of valuable books.)': '(Regal voller wertvoller Buecher.)',
    "(He looks as if he's already won.)": '(Als haette er schon gewonnen.)',
    "(Is this the book I shouldn't see?)": '(Soll ich das Buch nicht sehen?)',
    "(It's a passage to another room.)": '(Durchgang zu anderem Raum.)',
    "(It's a room for the bar's owner.)": '(Raum vom Besitzer der Bar.)',
    "(It's locked... I can't open it.)": '(Verschlossen... geht nicht auf.)',
    "(Looks like he's one of the leaders": '(Er ist wohl einer der Fuehrer',
    '(Nuts have fallen to the ground.)': '(Nuesse gefallen zu Boden.)',
    "(That table's seen a few bar fights.)": '(Der Tisch sah manche Keilerei.)',
    '(The door is blocked by the tables.)': '(Tuer: von Tischen blockiert.)',
    'A blessed gun for a good hunt?)': 'Eine gesegnete Waffe',
    'Are you sure we can trust him?': 'Kann man ihm wirklich trauen?',
    "Do you think it's because we never": 'Liegts daran, dass wir nie',
    "Forget it... it's no big deal...": 'Vergiss es... nicht so wichtig.',
    "I don't think that will happen.": 'Das wird wohl nicht passieren.',
    'I hope we can help each other,': 'Hoffentlich helfen wir uns,',
    'If there is an emergency, I must': 'Wenn Not herrscht, muss ich',
    'this town I would be forced to ': 'Stadt zu verlassen, muesste',
}
lines = open(path, encoding='latin1').read().split('\n')
out, applied, bad = [], 0, []
for line in lines:
    if ';' in line and line.strip():
        en, de = line.split(';', 1)
        if en in FIX:
            new = FIX[en]
            if len(new.encode('latin1')) <= len(en.encode('latin1')):
                if de != new:
                    line = en + ';' + new
                    applied += 1
            else:
                bad.append((en, len(new), len(en)))
    out.append(line)
open(path, 'w', encoding='latin1', newline='\n').write('\n'.join(out))
print('applied', applied)
for b in bad:
    print('TOO LONG %d>%d %r' % b)
