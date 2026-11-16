import os
os.chdir(r'C:\Users\FreakItOut\Documents\Panzer Dragoon Saga Übersetzung')

camp_fixes = {
    "don't you think?": "findest du?",
    "don't want it.": "Will es nicht.",
    "Nice place, isn't it?": "Schoener Ort?",
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

# Read old values from the files (before changes) - but we already changed them
# The old values are the shifted ones. Let me reconstruct from the candidates file.
# Actually, the apply_review_fixes.py needs old_de. Since we changed the CSV,
# the old values are gone. But we can use the text-scan approach (old = current EN? No).
# 
# The problem: apply_review_fixes.py searches for old_b + NUL on the disc.
# The old text (shifted) is still on the disc. But we don't have the old_de values
# in the CSV anymore.
#
# Let me just note: the disc patching for these subtitle files is done via
# a different mechanism (subtitles_patch.js or similar). The apply_review_fixes.py
# approach works for TWN_CAMP/RUIN (they're in _work/subtitles/).
#
# But since the old_de values are lost, I'll need to reconstruct them.
# The old values were the shifted ones from the candidates file.

print('Need to reconstruct old_de values from candidates')
# Let me check the candidates file for old_de values
with open('_work/review_fixes/TWN_CAMP_PRG_candidates2.csv', encoding='latin1') as f:
    next(f)
    for line in f:
        parts = line.rstrip('\r\n').split(';')
        if len(parts) >= 3:
            en, old_de = parts[1], parts[2]
            if en in camp_fixes:
                print('CAMP uid=%s EN=%r old_DE=%r' % (parts[0], en[:30], old_de[:30]))