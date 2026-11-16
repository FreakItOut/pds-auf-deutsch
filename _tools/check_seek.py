import os
os.chdir(r'C:\Users\FreakItOut\Documents\Panzer Dragoon Saga Übersetzung')
targets = ['Warning, accessing now...', 'Identify yourself...', 'Life form of unknown construction.', '(Incense sticks.)', "Thank you very much.", 'Besides, he is just a boy.']
with open('_work/menu_de/TWN_SEEK_PRG_de_d4.csv', encoding='latin1') as f:
    for line in f:
        parts = line.rstrip('\r\n').split(';')
        if len(parts) >= 6:
            en, de = parts[4], parts[5]
            if en in targets:
                print(repr(en), '->', repr(de))