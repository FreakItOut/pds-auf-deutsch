import os
os.chdir(r'C:\Users\FreakItOut\Documents\Panzer Dragoon Saga Übersetzung')
SRC = r'_work\menu_de\TWN_SEEK_PRG_d4_map.csv'
# Read as UTF-8 (current encoding)
with open(SRC, 'r', encoding='utf-8') as f:
    text = f.read()
# Replace umlauts
text = text.replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue')
text = text.replace('Ä', 'Ae').replace('Ö', 'Oe').replace('Ü', 'Ue')
# Also fix the too-long entry
text = text.replace('Rede ue. das Reich, hoertest du', 'Rede u. das Reich, hoertest du')
# Write as latin1
with open(SRC, 'w', encoding='latin1', newline='') as f:
    f.write(text)
print('done')