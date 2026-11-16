import os
os.chdir(r'C:\Users\FreakItOut\Documents\Panzer Dragoon Saga Übersetzung')
for fn in ['TWN_CAMP_PRG_de.csv']:
    print('===', fn)
    with open('_work/subtitles/'+fn, encoding='latin1') as f:
        for line in f:
            line=line.rstrip('\r\n')
            parts=line.split(';')
            if len(parts)<6: continue
            en=parts[4].lower(); de=parts[5].lower()
            en_neg = any(n in en for n in ("not ", "n't", "never ", "no ", "don't", "doesn't", "can't", "won't", "without"))
            de_neg = any(n in de for n in ('nicht', 'kein', 'keine', 'nie ', 'ohne', 'niemals', 'keinen', 'keiner'))
            if en_neg and not de_neg:
                print('uid=%s EN=%r DE=%r' % (parts[0], parts[4][:50], parts[5][:50]))