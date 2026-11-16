import csv, os
os.chdir(r'C:\Users\FreakItOut\Documents\Panzer Dragoon Saga Übersetzung')
for fn in ['TWN_CAMP_PRG_de.csv', 'TWN_RUIN_PRG_de.csv']:
    rows = []
    with open('_work/subtitles/'+fn, encoding='latin1') as f:
        for line in f:
            line = line.rstrip('\r\n')
            if not line: continue
            parts = line.split(';')
            if len(parts) < 6: continue
            rows.append((parts[0], parts[4], parts[5]))
    gloss = 0
    for uid, en, de in rows:
        low = de.lower()
        if 'imperium' in low or 'altertum' in low or 'kapit' in low:
            gloss += 1
    neg = 0
    for uid, en, de in rows:
        en_low = en.lower(); de_low = de.lower()
        en_neg = any(n in en_low for n in ("not ", "n't", "never ", "no ", "don't", "doesn't", "can't", "won't", "without"))
        de_neg = any(n in de_low for n in ('nicht', 'kein', 'keine', 'nie ', 'ohne', 'niemals', 'keinen', 'keiner'))
        if en_neg and not de_neg:
            neg += 1
    print(fn, 'rows:', len(rows), 'glossary:', gloss, 'negation-lost:', neg)