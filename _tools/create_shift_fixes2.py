import os
os.chdir(r'C:\Users\FreakItOut\Documents\Panzer Dragoon Saga Übersetzung')

# CAMP fixes
camp = [
    ("TWN_CAMP_PRG_de.csv", "don't you think?", "findest?", "findest du?"),
    ("TWN_CAMP_PRG_de.csv", "don't want it.", "Fuehl frei.", "Will es nicht."),
    ("TWN_CAMP_PRG_de.csv", "Nice place, isn't it?", "Ja, sogar Quelle.", "Schoener Ort?"),
]

# RUIN fixes
ruin = [
    ("TWN_RUIN_PRG_de.csv", "Aren't they after your dragon?", "Hinter deinem Drachen?", "Hinter deinem Drachen?"),
    ("TWN_RUIN_PRG_de.csv", "don't you think?", "findest?", "findest du?"),
    ("TWN_RUIN_PRG_de.csv", "Why don't you join the seekers?", "ausserhalb von Zoah.", "Schliesst dich nicht an?"),
    ("TWN_RUIN_PRG_de.csv", "Don't talk like that. With all your", "Ehrlich, nuetzlich?", "Sprich nicht so."),
    ("TWN_RUIN_PRG_de.csv", "I never knew that the real world", "Berzer tot.", "Wusste nicht, echte Welt"),
    ("TWN_RUIN_PRG_de.csv", "You're not coming with us?", "wiedersehen, wenn Sucher.", "Nicht mit uns?"),
    ("TWN_RUIN_PRG_de.csv", "Don't worry.", "Leid.", "Keine Sorge."),
    ("TWN_RUIN_PRG_de.csv", "I'm sorry, I couldn't help more.", "Es tut mir leid.", "Leid, nicht mehr helfen."),
    ("TWN_RUIN_PRG_de.csv", "I'm sorry, I couldn't be of your", "Es tut mir leid.", "Leid, nicht helfen."),
    ("TWN_RUIN_PRG_de.csv", "don't you join us?", "schliesst dich an?", "Nicht mitmachen?"),
    ("TWN_RUIN_PRG_de.csv", "into battle. Don't you think?", "in Schlacht fuehren.", "Schlacht. Findest du?"),
    ("TWN_RUIN_PRG_de.csv", "It wasn't until recently that we", "Erst kuerzlich haben wir", "Erst kuerzlich wir"),
]

all_fixes = camp + ruin
with open('_work/review_fixes/shift_fixes.csv', 'w', encoding='latin1', newline='') as f:
    f.write('source_file;en;old_de;new_de;reason\n')
    for src, en, old, new in all_fixes:
        f.write('%s;%s;%s;%s;shift fix\n' % (src, en.replace(';', ','), old.replace(';', ','), new.replace(';', ',')))
print('written', len(all_fixes), 'fixes')