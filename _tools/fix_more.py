import os
os.chdir(r'C:\Users\FreakItOut\Documents\Panzer Dragoon Saga Übersetzung')
SRC = r'_work\menu_de\TWN_SEEK_PRG_de_d4.csv'
lines = open(SRC, encoding='latin1').read().splitlines()
new_lines = []
for line in lines:
    if '(More equipment?;' in line or line.startswith('(More equipment?;'):
        line = line.replace('(Mehr Ausruest.?)', '(Mehr Ausruest?)')
    new_lines.append(line)
with open(SRC, 'w', encoding='latin1', newline='') as f:
    for line in new_lines:
        f.write(line + '\n')
print('done')