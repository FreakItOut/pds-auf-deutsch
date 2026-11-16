import os
os.chdir(r'C:\Users\FreakItOut\Documents\Panzer Dragoon Saga Übersetzung')
for fn in ['TWN_CAMP_PRG_de.csv', 'TWN_RUIN_PRG_de.csv']:
    print('===', fn)
    with open('_work/subtitles/'+fn, encoding='latin1') as f:
        for line in f:
            parts = line.rstrip('\r\n').split(';')
            if len(parts) < 6: continue
            en, de = parts[4], parts[5]
            en_low = en.lower(); de_low = de.lower()
            en_neg = any(n in en_low for n in ("not ", "n't", "never ", "no ", "don't", "doesn't", "can't", "won't", "without"))
            de_neg = any(n in de_low for n in ('nicht', 'kein', 'keine', 'nie ', 'ohne', 'niemals', 'keinen', 'keiner'))
            if en_neg and not de_neg:
                print('  uid=%s EN=%r DE=%r' % (parts[0], en[:60], de[:60]))