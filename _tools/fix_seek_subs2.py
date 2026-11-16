import os
os.chdir(r'C:\Users\FreakItOut\Documents\Panzer Dragoon Saga Übersetzung')

fixes = {
    "Identify yourself...": "Identifiziere dich.",
    "(Incense sticks.)": "(Raeucherst.)",
    "(They've been there for a while.)": "(Sie waren dort.)",
    "There's a passage on the other side.)": "Dort Durchgang.)",
    "(Someone's talking behind this door.)": "(Jemand hinter Tuer.)",
    "Besides, he is just a boy.": "Ausserdem nur ein Junge.",
    "(It is beautifully decorated,": "(Schoen dekoriert,",
    "but it looks extremely fragile.)": "aber sehr zerbrechlich.)",
}

src = '_work/subtitles/TWN_SEEK_PRG_de.csv'
lines = open(src, encoding='latin1').read().splitlines()
new_lines = []
applied = 0
for line in lines:
    if not line:
        new_lines.append(line); continue
    parts = line.split(';')
    if len(parts) < 6:
        new_lines.append(line); continue
    en = parts[4]
    if en in fixes:
        new_de = fixes[en]
        if len(new_de.encode('latin1')) <= len(en.encode('latin1')):
            parts[5] = new_de
            applied += 1
        else:
            print('TOO LONG:', en, len(new_de), '>', len(en))
    new_lines.append(';'.join(parts))
with open(src, 'w', encoding='latin1', newline='') as f:
    for line in new_lines:
        f.write(line + '\n')
print('applied:', applied)