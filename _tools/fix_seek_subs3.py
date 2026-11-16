import os
os.chdir(r'C:\Users\FreakItOut\Documents\Panzer Dragoon Saga Übersetzung')

fixes = {
    "Warning, accessing now...": "Warnung, Zugriff...",
    "That's what happened with Mel-Kava.)": "Das geschah mit Mel-Kava.)",
    "Life form of unknown construction.": "Lebensform unbekannter Art.",
    "(Didn't Paet hear it?)": "(Hoerte Paet es nicht?)",
    "(It's obviously an ancient device.": "(Offenbar uraltes Geraet.",
    "Looks like it's off during the day.)": "Scheint tagsueber aus.)",
    "(It's made out of monsters' wings.": "(Aus Fluegeln von Monstern.",
    "This is where the light comes from.)": "Von hier kommt das Licht.)",
    "Thank you very much.": "Vielen Dank.",
    "You need not thank me,": "Du brauchst mir nicht danken,",
    "(This lamp looks valuable.)": "(Wertvolle Lampe.)",
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