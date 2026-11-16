import os
os.chdir(r'C:\Users\FreakItOut\Documents\Panzer Dragoon Saga Übersetzung')
SRC = r'_work/subtitles/TWN_RUIN_PRG_de.csv'
with open(SRC, 'r', encoding='latin1') as f:
    text = f.read()
# Fix grammar: das Vorzeit -> die Vorzeit
text = text.replace('das Vorzeit', 'die Vorzeit')
text = text.replace('Das Vorzeit', 'Die Vorzeit')
with open(SRC, 'w', encoding='latin1', newline='') as f:
    f.write(text)
print('done')