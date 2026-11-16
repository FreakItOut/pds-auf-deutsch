import os
os.chdir(r'C:\Users\FreakItOut\Documents\Panzer Dragoon Saga Übersetzung')
ruin_targets = ["Aren't they after your dragon?", "don't you think?", "Why don't you join the seekers?", "Don't talk like that. With all your", "I never knew that the real world", "You're not coming with us?", "Don't worry.", "I'm sorry, I couldn't help more.", "I'm sorry, I couldn't be of your", "don't you join us?", "into battle. Don't you think?", "It wasn't until recently that we"]
with open('_work/review_fixes/TWN_RUIN_PRG_candidates2.csv', encoding='latin1') as f:
    next(f)
    for line in f:
        parts = line.rstrip('\r\n').split(';')
        if len(parts) >= 3:
            en, old_de = parts[1], parts[2]
            if en in ruin_targets:
                print('RUIN EN=%r old_DE=%r' % (en[:40], old_de[:40]))