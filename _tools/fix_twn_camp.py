# Fix TWN_CAMP quality issues (glossary + placeholder).
import csv
import os
import re

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SRC = '_work/subtitles/TWN_CAMP_PRG_de.csv'
FIXES = '_work/review_fixes/TWN_CAMP_fixes.csv'

rows = []
with open(SRC, encoding='latin1') as f:
    for line in f:
        line = line.rstrip('\r\n')
        if not line:
            continue
        parts = line.split(';')
        if len(parts) < 6:
            continue
        uid, length, offset, offsets, en, de = parts[0], parts[1], parts[2], parts[3], parts[4], parts[5]
        rows.append((uid, length, offset, offsets, en, de))

fixes = []
for uid, length, offset, offsets, en, de in rows:
    reasons = []
    new_de = None

    # 1. Placeholder 'de'
    if de.strip() == 'de':
        new_de = 'Holz knistert in den Flammen.'
        reasons.append('placeholder de')

    # 2. Glossary: Imperium -> Reich
    if 'Imperium' in de or 'imperium' in de.lower():
        if new_de is None:
            new_de = de
        new_de = new_de.replace('Imperium', 'Reich').replace('imperium', 'Reich')
        reasons.append('Glossar: Imperium->Reich')

    # 3. Glossary: Altertum -> Vorzeit
    if 'Altertum' in de or 'altertum' in de.lower():
        if new_de is None:
            new_de = de
        new_de = new_de.replace('Altertum', 'Vorzeit').replace('altertum', 'Vorzeit')
        reasons.append('Glossar: Altertum->Vorzeit')

    # 4. Glossary: Kapitaen -> Chef
    if 'Kapit' in de or 'kapit' in de.lower():
        if new_de is None:
            new_de = de
        new_de = re.sub(r'Kapit[aä]n', 'Chef', new_de, flags=re.IGNORECASE)
        reasons.append('Glossar: Kapitaen->Chef')

    if new_de is not None and new_de != de:
        if len(new_de.encode('latin1')) <= len(en.encode('latin1')):
            fixes.append((en, de, new_de, '; '.join(reasons)))

with open(FIXES, 'w', encoding='latin1', newline='') as f:
    f.write('source_file;en;old_de;new_de;reason\n')
    for en, de, new_de, reason in fixes:
        f.write('TWN_CAMP_PRG_de.csv;%s;%s;%s;%s\n' % (
            en.replace(';', ','), de.replace(';', ','), new_de.replace(';', ','), reason))

print('auto-fixes (glossary+placeholder):', len(fixes))
print('total rows:', len(rows))
print('output:', FIXES)
