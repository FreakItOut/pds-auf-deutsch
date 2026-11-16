import os
os.chdir(r'C:\Users\FreakItOut\Documents\Panzer Dragoon Saga Übersetzung')
SRC = r'_work\menu_de\TWN_SEEK_PRG_d4_map.csv'
# Read as bytes
with open(SRC, 'rb') as f:
    data = f.read()
# Replace latin1 umlauts with ASCII
data = data.replace(b'\xe4', b'ae')  # ä
data = data.replace(b'\xf6', b'oe')  # ö
data = data.replace(b'\xfc', b'ue')  # ü
data = data.replace(b'\xc4', b'Ae')  # Ä
data = data.replace(b'\xd6', b'Oe')  # Ö
data = data.replace(b'\xdc', b'Ue')  # Ü
# Fix too-long entry
data = data.replace(b'Rede ue. das Reich, hoertest du', b'Rede u. das Reich, hoertest du')
with open(SRC, 'wb') as f:
    f.write(data)
print('done')