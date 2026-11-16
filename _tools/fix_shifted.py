import os
os.chdir(r'C:\Users\FreakItOut\Documents\Panzer Dragoon Saga Übersetzung')

# For each shifted entry, try to find the correct DE from the menu_de map
menu_translations = {}
with open('_work/menu_de/TWN_SEEK_PRG_de_d4.csv', encoding='latin1') as f:
    for line in f:
        parts = line.rstrip('\r\n').split(';')
        if len(parts) >= 6:
            menu_translations[parts[4]] = parts[5]

shifted_uids = [101, 146, 213, 240, 290, 319, 328, 698, 892, 1587]
with open('_work/subtitles/TWN_SEEK_PRG_de.csv', encoding='latin1') as f:
    for line in f:
        parts = line.rstrip('\r\n').split(';')
        if len(parts) >= 6 and parts[0] in [str(u) for u in shifted_uids]:
            en = parts[4]
            if en in menu_translations:
                print('uid=%s EN=%r -> menu_de=%r' % (parts[0], en[:40], menu_translations[en][:40]))
            else:
                print('uid=%s EN=%r -> NO menu_de match' % (parts[0], en[:40]))