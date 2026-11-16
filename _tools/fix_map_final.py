import os
os.chdir(r'C:\Users\FreakItOut\Documents\Panzer Dragoon Saga Übersetzung')
SRC = r'_work\menu_de\TWN_SEEK_PRG_d4_map.csv'
lines = open(SRC, encoding='latin1').read().splitlines()
new_lines = []
for line in lines:
    # Fix too-long entries
    if '(A windmill for ventilation.;' in line or line.startswith('(A windmill for ventilation.;'):
        line = line.replace('(Ein Windrad zur Belueftung.)', '(Windrad zur Belueft.)')
    if '(A wire for the engine.;' in line or line.startswith('(A wire for the engine.;'):
        line = line.replace('(Ein Draht f den Motor.)', '(Ein Draht f. Motor.)')
    if '(More equipment?;' in line or line.startswith('(More equipment?;'):
        line = line.replace('(Mehr Ausruest.?)', '(Mehr Ausruest?)')
    # Fix non-ASCII
    line = line.replace('Vorräte', 'Vorraete').replace('Vorräte', 'Vorraete')
    line = line.replace('Gläubigen', 'Glaeubigen')
    line = line.replace('legendäre', 'legendäre'.replace('ä','ae'))  # won't work, do below
    line = line.replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace('Ä', 'Ae').replace('Ö', 'Oe').replace('Ü', 'Ue')
    new_lines.append(line)
with open(SRC, 'w', encoding='latin1', newline='') as f:
    for line in new_lines:
        f.write(line + '\n')
print('done')