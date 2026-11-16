import os, re
os.chdir(r'C:\Users\FreakItOut\Documents\Panzer Dragoon Saga Übersetzung')

# Find consecutive shifted entries (blocks)
# A shifted entry is one where DE doesn't share meaningful words with EN
# and the DE is from a different EN string

with open('_work/subtitles/TWN_SEEK_PRG_de.csv', encoding='latin1') as f:
    entries = []
    for line in f:
        parts = line.rstrip('\r\n').split(';')
        if len(parts) >= 6:
            entries.append((parts[0], parts[4], parts[5]))

# Find blocks of 3+ consecutive shifted entries
# Heuristic: DE is a substring of another EN entry's DE, or DE shares no words with EN
def is_shifted(en, de):
    # Check if DE is clearly from a different EN
    # Look for DE that is a prefix of another entry's DE
    en_lower = en.lower()
    de_lower = de.lower()
    # Remove punctuation
    en_clean = re.sub(r'[^a-zäöüA-ZÄÖÜ ]', '', en_lower)
    de_clean = re.sub(r'[^a-zäöüA-ZÄÖÜ ]', '', de_lower)
    # If DE contains a complete English word that's not in EN, it's likely shifted
    en_words = set(en_clean.split())
    de_words = set(de_clean.split())
    # Check for English words in DE
    en_in_de = de_words & en_words
    # If no shared words and DE is substantial, likely shifted
    if len(en_words) >= 2 and len(en_in_de) == 0 and len(de_clean) > 10:
        return True
    return False

# Find consecutive shifted blocks
blocks = []
current_block = []
for uid, en, de in entries:
    if is_shifted(en, de):
        current_block.append((uid, en, de))
    else:
        if len(current_block) >= 2:
            blocks.append(current_block)
        current_block = []
if len(current_block) >= 2:
    blocks.append(current_block)

print('Number of shifted blocks (2+ consecutive):', len(blocks))
print('Total shifted entries in blocks:', sum(len(b) for b in blocks))
for i, block in enumerate(blocks[:10]):
    print('\nBlock %d (%d entries, uid %s-%s):' % (i+1, len(block), block[0][0], block[-1][0]))
    for uid, en, de in block[:3]:
        print('  %s: %r -> %r' % (uid, en[:40], de[:40]))