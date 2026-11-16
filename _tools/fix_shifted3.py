import os
os.chdir(r'C:\Users\FreakItOut\Documents\Panzer Dragoon Saga Übersetzung')

# Shortened fixes for shifted STANDALONE entries
camp_fixes = {
    "don't you think?": "findest du?",
    "don't want it.": "Will es nicht.",
    "Nice place, isn't it?": "Schoener Ort?",
    "Hey, aren't you that hunter?": "Nicht der Jaeger?",
}

ruin_fixes = {
    "Aren't they after your dragon?": "Hinter deinem Drachen?",
    "don't you think?": "findest du?",
    "Why don't you join the seekers?": "Schliesst dich nicht an?",
    "Don't talk like that. With all your": "Sprich nicht so.",
    "I never knew that the real world": "Wusste nicht, echte Welt",
    "You're not coming with us?": "Nicht mit uns?",
    "Don't worry.": "Keine Sorge.",
    "I'm sorry, I couldn't help more.": "Leid, nicht mehr helfen.",
    "I'm sorry, I couldn't be of your": "Leid, nicht helfen.",
    "don't you join us?": "Nicht mitmachen?",
    "into battle. Don't you think?": "Schlacht. Findest du?",
    "It wasn't until recently that we": "Erst kuerzlich wir",
}

# Check lengths
ok = 0; bad = 0
for en, de in list(camp_fixes.items()) + list(ruin_fixes.items()):
    if len(de.encode('latin1')) <= len(en.encode('latin1')):
        ok += 1
    else:
        bad += 1
        print('TOO LONG: %r (%d > %d)' % (de, len(de.encode('latin1')), len(en.encode('latin1'))))
print('ok:', ok, 'bad:', bad)

# Apply to subtitle CSVs
for fn, fixmap in [('TWN_CAMP_PRG_de.csv', camp_fixes), ('TWN_RUIN_PRG_de.csv', ruin_fixes)]:
    src = '_work/subtitles/' + fn
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
        if en in fixmap:
            new_de = fixmap[en]
            if len(new_de.encode('latin1')) <= len(en.encode('latin1')):
                parts[5] = new_de
                applied += 1
        new_lines.append(';'.join(parts))
    with open(src, 'w', encoding='latin1', newline='') as f:
        for line in new_lines:
            f.write(line + '\n')
    print(fn, 'applied:', applied)