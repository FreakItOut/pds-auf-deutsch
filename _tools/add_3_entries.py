import os
os.chdir(r'C:\Users\FreakItOut\Documents\Panzer Dragoon Saga Übersetzung')
SRC = r'_work\menu_de\TWN_SEEK_PRG_d4_map.csv'
with open(SRC, 'a', encoding='latin1') as f:
    f.write("(All the pots are sealed.);(Alle Toepfe versiegelt.)\n")
    f.write("(This one is being repaired.);(Dieser wird repariert.)\n")
    f.write("No, no... not really.;Nein, nicht wirklich.\n")
print('done')