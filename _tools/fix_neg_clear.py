fixes = [
# CAMP
("We really don't know", "Wir wissen wirklich nicht"),
("Don't you know the legend?", "Kennst du die Legende nicht?"),
("...Don't you want to meet her?", "...Willst du sie nicht treffen?"),
("Hey, aren't you that hunter?", "Hey, bist du nicht der Jaeger?"),
# RUIN
("Why don't YOU search the ruins?", "Warum suchst DU nicht die Ruinen?"),
("But, shouldn't you eat something?", "Aber, solltest du nicht essen?"),
]

ok = 0; bad = 0
for en, de in fixes:
    # Find the matching row to check length
    pass

# Apply to subtitles CSVs
import os
os.chdir(r'C:\Users\FreakItOut\Documents\Panzer Dragoon Saga Übersetzung')

# CAMP fixes
camp_fixes = {
    "We really don't know": "Wir wissen wirklich nicht",
    "Don't you know the legend?": "Kennst du die Legende nicht?",
    "...Don't you want to meet her?": "...Willst du sie nicht treffen?",
    "Hey, aren't you that hunter?": "Hey, bist du nicht der Jaeger?",
}
ruin_fixes = {
    "Why don't YOU search the ruins?": "Warum suchst DU nicht die Ruinen?",
    "But, shouldn't you eat something?": "Aber, solltest du nicht essen?",
}

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
            # Validate length
            if len(new_de.encode('latin1')) <= len(en.encode('latin1')):
                parts[5] = new_de
                applied += 1
            else:
                print('TOO LONG:', fn, en, len(new_de), '>', len(en))
        new_lines.append(';'.join(parts))
    with open(src, 'w', encoding='latin1', newline='') as f:
        for line in new_lines:
            f.write(line + '\n')
    print(fn, 'applied:', applied)