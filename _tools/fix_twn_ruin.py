# Fix TWN_RUIN glossary + EN-words-left + negation issues.
import csv
import os
import re

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SRC = '_work/subtitles/TWN_RUIN_PRG_de.csv'
FIXES = '_work/review_fixes/TWN_RUIN_fixes.csv'

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
    new_de = None
    reasons = []

    low = de.lower()

    # Glossary: Imperium -> Reich
    if 'imperium' in low:
        if new_de is None:
            new_de = de
        new_de = new_de.replace('Imperium', 'Reich').replace('imperium', 'Reich')
        reasons.append('Glossar: Imperium->Reich')

    # Glossary: Altertum -> Vorzeit
    if 'altertum' in low:
        if new_de is None:
            new_de = de
        new_de = new_de.replace('Altertum', 'Vorzeit').replace('altertum', 'Vorzeit')
        reasons.append('Glossar: Altertum->Vorzeit')

    # Glossary: Kapitän -> Chef
    if 'kapit' in low:
        if new_de is None:
            new_de = de
        new_de = re.sub(r'Kapit[aä]n', 'Chef', new_de, flags=re.IGNORECASE)
        reasons.append('Glossar: Kapitaen->Chef')

    # EN words left: fix untranslated shop labels
    if en == 'Buy Gun Part' and de == 'Buy Gun Part':
        new_de = 'Teil kaufen'
        reasons.append('untranslated: Buy Gun Part')
    if en == 'Sell Gun Part' and de == 'Sell Gun Part':
        new_de = 'Verkauf Teil'
        reasons.append('untranslated: Sell Gun Part')
    if en == 'Switch Sell/Buy' and de == 'Switch Sell/Buy':
        new_de = 'Kauf/Verkauf'
        reasons.append('untranslated: Switch Sell/Buy')

    # Negation lost: fix clear cases
    en_low = en.lower()
    de_low = de.lower()
    en_neg = any(n in en_low for n in ('not ', "n't", 'never ', 'no ', "don't", "doesn't", "can't", "won't", 'without', 'never'))
    de_neg = any(n in de_low for n in ('nicht', 'kein', 'keine', 'nie ', 'ohne', 'niemals', 'keinen', 'keiner', 'keinerlei'))
    if en_neg and not de_neg:
        # These need manual review - mark but don't auto-fix
        reasons.append('NEGATION LOST (manual)')

    if new_de is not None and new_de != de:
        if len(new_de.encode('latin1')) <= len(en.encode('latin1')):
            fixes.append((en, de, new_de, '; '.join(reasons)))

with open(FIXES, 'w', encoding='latin1', newline='') as f:
    f.write('source_file;en;old_de;new_de;reason\n')
    for en, de, new_de, reason in fixes:
        f.write('TWN_RUIN_PRG_de.csv;%s;%s;%s;%s\n' % (
            en.replace(';', ','), de.replace(';', ','), new_de.replace(';', ','), reason))

print('auto-fixes (glossary+labels):', len(fixes))
print('output:', FIXES)
# also print negation-lost cases for manual review
print('\nNegation-lost cases (need manual fix):')
for uid, length, offset, offsets, en, de in rows:
    en_low = en.lower()
    de_low = de.lower()
    en_neg = any(n in en_low for n in ('not ', "n't", 'never ', 'no ', "don't", "doesn't", "can't", "won't", 'without', 'never'))
    de_neg = any(n in de_low for n in ('nicht', 'kein', 'keine', 'nie ', 'ohne', 'niemals', 'keinen', 'keiner', 'keinerlei'))
    if en_neg and not de_neg:
        print('  uid=%s EN=%r DE=%r' % (uid, en[:50], de[:50]))
