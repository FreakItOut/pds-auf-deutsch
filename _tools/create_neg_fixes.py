import os
os.chdir(r'C:\Users\FreakItOut\Documents\Panzer Dragoon Saga Übersetzung')

# Read old DE values from the files (before our changes, we need the old values)
# Actually, we already changed them. Let me reconstruct the old values from the candidates file.
# The old values are the ones before our fix. Let me just create fixes with the known old/new pairs.

fixes = [
    ('TWN_CAMP_PRG_de.csv', "We really don't know", "Wir wissen wenig", "Wir wissen nicht"),
    ('TWN_CAMP_PRG_de.csv', "Don't you know the legend?", "Kennst du die Legende?", "Kennst die Legende nicht?"),
    ('TWN_CAMP_PRG_de.csv', "...Don't you want to meet her?", "...Willst du treffen?", "...Willst sie nicht treffen?"),
    ('TWN_CAMP_PRG_de.csv', "Hey, aren't you that hunter?", "Hey, bist du Jaeger?", "Hey, nicht der Jaeger?"),
    ('TWN_RUIN_PRG_de.csv', "Why don't YOU search the ruins?", "Warum suchst DU Ruinen?", "Warum suchst DU nicht Ruinen?"),
    ('TWN_RUIN_PRG_de.csv', "But, shouldn't you eat something?", "Aber, solltest essen?", "Aber, solltest nicht essen?"),
]

with open('_work/review_fixes/neg_clear_fixes.csv', 'w', encoding='latin1', newline='') as f:
    f.write('source_file;en;old_de;new_de;reason\n')
    for src, en, old, new in fixes:
        f.write('%s;%s;%s;%s;negation fix\n' % (src, en.replace(';', ','), old.replace(';', ','), new.replace(';', ',')))
print('fixes written')