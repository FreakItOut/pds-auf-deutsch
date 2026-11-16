fixes = {
    "We really don't know": "Wir wissen nicht",
    "Don't you know the legend?": "Kennst die Legende nicht?",
    "...Don't you want to meet her?": "...Willst sie nicht treffen?",
    "Hey, aren't you that hunter?": "Hey, nicht der Jaeger?",
    "Why don't YOU search the ruins?": "Warum suchst DU nicht Ruinen?",
    "But, shouldn't you eat something?": "Aber, solltest nicht essen?",
}

ok = 0; bad = 0
for en, de in fixes.items():
    if len(de.encode('latin1')) <= len(en.encode('latin1')):
        ok += 1
    else:
        bad += 1
        print('STILL TOO LONG: %s (%d > %d)' % (de, len(de.encode('latin1')), len(en.encode('latin1'))))
print('ok:', ok, 'bad:', bad)

import os
os.chdir(r'C:\Users\FreakItOut\Documents\Panzer Dragoon Saga Übersetzung')
for fn, fixmap_subset in [('TWN_CAMP_PRG_de.csv', {k:v for k,v in fixes.items() if k in ("We really don't know", "Don't you know the legend?", "...Don't you want to meet her?", "Hey, aren't you that hunter?")}),
                          ('TWN_RUIN_PRG_de.csv', {k:v for k,v in fixes.items() if k in ("Why don't YOU search the ruins?", "But, shouldn't you eat something?")})]:
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
        if en in fixmap_subset:
            new_de = fixmap_subset[en]
            if len(new_de.encode('latin1')) <= len(en.encode('latin1')):
                parts[5] = new_de
                applied += 1
        new_lines.append(';'.join(parts))
    with open(src, 'w', encoding='latin1', newline='') as f:
        for line in new_lines:
            f.write(line + '\n')
    print(fn, 'applied:', applied)