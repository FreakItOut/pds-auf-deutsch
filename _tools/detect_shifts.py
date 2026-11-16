import os, re
os.chdir(r'C:\Users\FreakItOut\Documents\Panzer Dragoon Saga Übersetzung')

# Read the subtitles file
with open('_work/subtitles/TWN_SEEK_PRG_de.csv', encoding='latin1') as f:
    lines = f.readlines()

# Parse entries
entries = []
for i, line in enumerate(lines):
    parts = line.rstrip('\r\n').split(';')
    if len(parts) >= 6:
        entries.append({'idx': i, 'uid': parts[0], 'en': parts[4], 'de': parts[5], 'parts': parts, 'line': line})

# Function to compute word overlap between EN and DE
def word_overlap(en, de):
    en_words = set(re.findall(r'[a-zA-Z]{3,}', en.lower()))
    de_words = set(re.findall(r'[a-zA-Z]{3,}', de.lower()))
    # Remove common words
    common = {'the', 'and', 'for', 'with', 'that', 'this', 'from', 'have', 'has', 'had', 'are', 'was', 'were', 'been', 'not', 'but', 'can', 'will', 'just', 'all', 'more', 'some', 'there', 'what', 'when', 'where', 'who', 'how', 'why', 'which', 'their', 'them', 'they', 'been', 'were', 'was', 'had', 'has', 'have', 'der', 'die', 'das', 'und', 'ist', 'ich', 'du', 'er', 'sie', 'es', 'wir', 'nicht', 'ein', 'eine', 'mit', 'von', 'zu', 'auf', 'in', 'an', 'fuer', 'ueber', 'nach', 'bei', 'aus', 'um', 'am', 'im', 'zum', 'zur', 'den', 'dem', 'des', 'der', 'einen', 'einem', 'einer', 'eines'}
    en_specific = en_words - common
    de_specific = de_words - common
    if not en_specific or not de_specific:
        return 0
    return len(en_specific & de_specific)

# Find 1-position shifted pairs
# For consecutive entries where shifting DE by 1 improves overlap
shifts_to_fix = []
for i in range(len(entries) - 1):
    e1 = entries[i]
    e2 = entries[i+1]
    # Current overlap
    cur_overlap = word_overlap(e1['en'], e1['de']) + word_overlap(e2['en'], e2['de'])
    # Shifted overlap (e1 gets e2's DE, e2 gets e1's DE)
    shifted_overlap = word_overlap(e1['en'], e2['de']) + word_overlap(e2['en'], e1['de'])
    # Only consider if shifted is significantly better
    if shifted_overlap > cur_overlap + 1 and shifted_overlap >= 2:
        shifts_to_fix.append((i, i+1, cur_overlap, shifted_overlap))

print('Found %d adjacent pairs that would benefit from 1-position shift' % len(shifts_to_fix))

# Group consecutive shifts into blocks
blocks = []
current = []
for idx, (i, j, co, so) in enumerate(shifts_to_fix):
    if current and i == current[-1][1]:
        current.append((i, j, co, so))
    else:
        if current:
            blocks.append(current)
        current = [(i, j, co, so)]
if current:
    blocks.append(current)

print('Number of shift blocks:', len(blocks))
print('Total entries in blocks:', sum(len(b) for b in blocks))

# Show first few blocks
for i, block in enumerate(blocks[:5]):
    print('\nBlock %d: entries %s-%s' % (i+1, entries[block[0][0]]['uid'], entries[block[-1][1]]['uid']))
    for i_idx, j_idx, co, so in block[:3]:
        print('  %s: %r -> %r (overlap %d->%d)' % (
            entries[i_idx]['uid'], entries[i_idx]['en'][:40], entries[i_idx]['de'][:40], co, so))