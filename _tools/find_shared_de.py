import os, re
os.chdir(r'C:\Users\FreakItOut\Documents\Panzer Dragoon Saga Übersetzung')

# Build a map of all DE texts to their EN texts
de_to_en = {}
with open('_work/subtitles/TWN_SEEK_PRG_de.csv', encoding='latin1') as f:
    for line in f:
        parts = line.rstrip('\r\n').split(';')
        if len(parts) >= 6:
            de_to_en[parts[5]] = parts[4]

# For each entry, check if its DE text is the DE text of a different EN entry
# (which would indicate a shift)
shifted = []
with open('_work/subtitles/TWN_SEEK_PRG_de.csv', encoding='latin1') as f:
    for line in f:
        parts = line.rstrip('\r\n').split(';')
        if len(parts) < 6: continue
        uid, en, de = parts[0], parts[4], parts[5]
        # Check if de appears as the DE for a different EN
        for other_de, other_en in de_to_en.items():
            if other_de == de and other_en != en:
                shifted.append((uid, en, de, other_en))
                break

print('Entries where DE is shared with a different EN:', len(shifted))
# Show unique shifted patterns
seen = set()
for uid, en, de, other_en in shifted[:20]:
    key = (en[:30], de[:30])
    if key not in seen:
        seen.add(key)
        print('uid=%s EN=%r DE=%r (shared with EN=%r)' % (uid, en[:40], de[:40], other_en[:40]))