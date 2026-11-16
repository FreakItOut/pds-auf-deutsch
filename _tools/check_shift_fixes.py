import os
os.chdir(r'C:\Users\FreakItOut\Documents\Panzer Dragoon Saga Übersetzung')

# Fix clearly shifted STANDALONE entries in TWN_CAMP and TWN_RUIN
# These are entries where DE is completely unrelated to EN
fixes = {
    'TWN_CAMP_PRG_de.csv': {
        24: "aus. Zu hart fuer die Coolias.)",  # keep as-is (multi-line fragment, actually correct)
        # These are clearly shifted - provide correct translations
    },
}

# Actually, let me focus on the entries that are clearly wrong single-line entries
# and can be fixed with reasonable translations
camp_fixes = {
    "Not a good food for the Coolia...)": None,  # multi-line, skip
    "don't you think?": "findest du nicht?",
    "don't want it.": "Ich will es nicht.",
    "Nice place, isn't it?": "Schoener Ort, nicht wahr?",
    "Hey, aren't you that hunter?": "Hey, bist du nicht der Jaeger?",  # already fixed
}

ruin_fixes = {
    "Aren't they after your dragon?": "Sind sie hinter deinem Drachen her?",
    "don't you think?": "findest du nicht?",
    "Why don't you join the seekers?": "Warum schliesst du dich nicht den Suchern an?",
    "Don't talk like that. With all your": "Sprich nicht so. Mit all deinen",
    "I never knew that the real world": "Ich wusste nicht, dass die echte Welt",
    "You're not coming with us?": "Kommst du nicht mit uns?",
    "Don't worry.": "Keine Sorge.",
    "I'm sorry, I couldn't help more.": "Es tut mir leid, ich konnte nicht mehr helfen.",
    "I'm sorry, I couldn't be of your": "Es tut mir leid, ich konnte nicht",
    "don't you join us?": "Schliesst du dich uns nicht an?",
    "into battle. Don't you think?": "in die Schlacht. Findest du nicht?",
    "It wasn't until recently that we": "Erst kuerzlich haben wir",
}

# Check lengths
for en, de in list(camp_fixes.items()) + list(ruin_fixes.items()):
    if de is None: continue
    if len(de.encode('latin1')) > len(en.encode('latin1')):
        print('TOO LONG: %r (%d > %d)' % (de, len(de.encode('latin1')), len(en.encode('latin1'))))
        del (camp_fixes if en in camp_fixes else ruin_fixes)[en]

print('CAMP fixes:', len(camp_fixes))
print('RUIN fixes:', len(ruin_fixes))