import os, re
os.chdir(r'C:\Users\FreakItOut\Documents\Panzer Dragoon Saga Übersetzung')

# Find truncated words in TWN_SEEK subtitles
# A truncated word is when DE ends with a partial word (not a complete word + punctuation)
with open('_work/subtitles/TWN_SEEK_PRG_de.csv', encoding='latin1') as f:
    lines = f.readlines()

truncated = []
for line in lines:
    parts = line.rstrip('\r\n').split(';')
    if len(parts) < 6: continue
    uid, en, de = parts[0], parts[4], parts[5]
    # Check if DE ends with a partial word (letter followed by nothing)
    if de and de[-1].isalpha() and not de.endswith('...'):
        # Check if the last "word" is incomplete
        last_word = de.split()[-1] if de.split() else ''
        # A word is truncated if it doesn't end with a common German suffix
        # or if it's clearly cut off
        truncated.append((uid, en, de))

print('Total truncated-looking entries:', len(truncated))
# Show first 30
for uid, en, de in truncated[:30]:
    print('uid=%s EN=%r DE=%r' % (uid, en[:40], de[:40]))