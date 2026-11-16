import os
os.chdir(r'C:\Users\FreakItOut\Documents\Panzer Dragoon Saga Übersetzung')
# Check which untranslated subtitle entries are NOT in menu_de
menu_en = set()
with open('_work/menu_de/TWN_SEEK_PRG_de_d4.csv', encoding='latin1') as f:
    for line in f:
        parts = line.rstrip('\r\n').split(';')
        if len(parts) >= 6:
            menu_en.add(parts[4])

with open('_work/subtitles/TWN_SEEK_PRG_de.csv', encoding='latin1') as f:
    for line in f:
        parts = line.rstrip('\r\n').split(';')
        if len(parts) >= 6:
            en, de = parts[4], parts[5]
            if en == de and len(en) > 3:
                in_menu = en in menu_en
                print('%s | in_menu=%s | %s' % ('YES' if in_menu else 'NO ', in_menu, en[:50]))