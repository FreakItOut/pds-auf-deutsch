import os
os.chdir(r'C:\Users\FreakItOut\Documents\Panzer Dragoon Saga Übersetzung')

# Build menu translations
menu_translations = {}
with open('_work/menu_de/TWN_SEEK_PRG_de_d4.csv', encoding='latin1') as f:
    for line in f:
        parts = line.rstrip('\r\n').split(';')
        if len(parts) >= 6:
            menu_translations[parts[4]] = parts[5]

# Manual translations for entries without menu_de match
manual = {
    "it smells like monster fluid.": "(Riecht nach Monsterfluess.)",
    "(Decorated with a monster's eyes.)": "(Dekoriert mit Monster-Augen.)",
    "at a time like this?": "zu so einer Zeit?",
    "a citizen of the Holy District!": "Buerger des Heiligen Bezirks!",
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
    if en in manual:
        new_de = manual[en]
    elif en in menu_translations:
        new_de = menu_translations[en]
    else:
        new_lines.append(line); continue
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