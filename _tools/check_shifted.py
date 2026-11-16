import os
os.chdir(r'C:\Users\FreakItOut\Documents\Panzer Dragoon Saga Übersetzung')

# Check if menu_de has better translations for shifted entries
menu_translations = {}
with open('_work/menu_de/TWN_SEEK_PRG_de_d4.csv', encoding='latin1') as f:
    for line in f:
        parts = line.rstrip('\r\n').split(';')
        if len(parts) >= 6:
            menu_translations[parts[4]] = parts[5]

# Count how many shifted subtitle entries have a menu_de translation
shifted_count = 0
fixed_count = 0
with open('_work/subtitles/TWN_SEEK_PRG_de.csv', encoding='latin1') as f:
    for line in f:
        parts = line.rstrip('\r\n').split(';')
        if len(parts) < 6: continue
        en, de = parts[4], parts[5]
        # Check if this is a shifted entry (DE unrelated to EN)
        # Simple heuristic: if EN and DE share no common meaningful words
        en_words = set(w.lower() for w in en.split() if len(w) > 3)
        de_words = set(w.lower() for w in de.split() if len(w) > 3)
        # Remove punctuation
        en_words = set(w.strip('.,!?()') for w in en_words)
        de_words = set(w.strip('.,!?()') for w in de_words)
        common = en_words & de_words
        if len(en_words) >= 2 and len(common) == 0 and len(en) > 15:
            shifted_count += 1
            if en in menu_translations:
                fixed_count += 1

print('Shifted entries:', shifted_count)
print('Have menu_de translation:', fixed_count)