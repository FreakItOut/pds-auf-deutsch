import os
os.chdir(r'C:\Users\FreakItOut\Documents\Panzer Dragoon Saga Übersetzung')

fixes = [
    ('TWN_CAMP_PRG_de.csv', '(Wood crackles in the flames.)', 'de', 'Holz knistert in den Flammen.'),
    ('TWN_CAMP_PRG_de.csv', 'Disp Collision', 'Disp Collision', 'Disp Kollision'),
    ('TWN_CAMP_PRG_de.csv', 'Buy Gun Part', 'Buy Gun Part', 'Teil kaufen'),
    ('TWN_CAMP_PRG_de.csv', 'Sell Gun Part', 'Sell Gun Part', 'Verk. Teil'),
    ('TWN_CAMP_PRG_de.csv', 'Switch Sell/Buy', 'Switch Sell/Buy', 'Kauf/Verkauf'),
    ('TWN_RUIN_PRG_de.csv', 'Disp Collision', 'Disp Collision', 'Disp Kollision'),
    ('TWN_RUIN_PRG_de.csv', 'Buy Gun Part', 'Buy Gun Part', 'Teil kaufen'),
    ('TWN_RUIN_PRG_de.csv', 'Sell Gun Part', 'Sell Gun Part', 'Verk. Teil'),
    ('TWN_RUIN_PRG_de.csv', 'Switch Sell/Buy', 'Switch Sell/Buy', 'Kauf/Verkauf'),
    ('TWN_RUIN_PRG_de.csv', 'Defense is as', 'Defense is as', 'Vert. ist wie'),
]

with open('_work/review_fixes/label_fixes.csv', 'w', encoding='latin1', newline='') as f:
    f.write('source_file;en;old_de;new_de;reason\n')
    for src, en, old, new in fixes:
        f.write('%s;%s;%s;%s;label fix\n' % (src, en.replace(';', ','), old.replace(';', ','), new.replace(';', ',')))
print('done')