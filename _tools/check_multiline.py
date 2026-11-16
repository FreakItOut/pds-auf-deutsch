import os
os.chdir(r'C:\Users\FreakItOut\Documents\Panzer Dragoon Saga Übersetzung')

# Check if negation-lost UIDs are part of multi-line entries
for fn in ['TWN_CAMP_PRG_de.csv']:
    with open('_work/subtitles/'+fn, encoding='latin1') as f:
        lines = f.readlines()
    # Find UIDs around uid=24
    for i, line in enumerate(lines):
        parts = line.rstrip('\r\n').split(';')
        if len(parts) >= 6 and parts[0] in ('23', '24', '25'):
            print('uid=%s EN=%r DE=%r' % (parts[0], parts[4][:50], parts[5][:50]))