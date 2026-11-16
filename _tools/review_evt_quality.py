import json

de_map = {}
for line in open('_work/evt_de_map.csv', encoding='latin1'):
    line = line.rstrip('\r\n')
    if not line or line.startswith('#'):
        continue
    en, de = line.split(';', 1)
    de_map[en] = de.strip()

pairs = sorted(de_map.items())

# 1) DE == EN (potentially untranslated, ignoring pure punctuation/proper nouns)
same = [(en, de) for en, de in pairs if de == en]

# 2) heavy compression: DE <= 55% of EN length (min 6 chars EN)
heavy = [(en, de) for en, de in pairs if len(en) >= 8 and len(de) <= 0.55 * len(en)]

# 3) odd artifacts: lowercase start where EN capitalized, double commas, odd words
import re
lower = [(en, de) for en, de in pairs if de and en[0].isupper() and de[0].islower()]

odd = [(en, de) for en, de in pairs if de.count(',,') > 1 or ' wovh' in de or 'MINSERTEN' in de or 'glenau' in de or 'tuerme und ruin' in de or 'x0a' in de]
print('total pairs:', len(pairs))
print('DE==EN pair count', len(same))
print('heavy compressed (<=55%)', len(heavy))
print('lowercase starts', len(lower))
print('odd artifacts', len(odd))

with open('_work/evt_review_heavy.csv', 'w', encoding='latin1', newline='') as f:
    for en, de in sorted(heavy):
        f.write(f'{en};{de}\n')
with open('_work/evt_review_same.csv', 'w', encoding='latin1', newline='') as f:
    for en, de in sorted(same):
        f.write(f'{en};{de}\n')
with open('_work/evt_review_odd.csv', 'w', encoding='latin1', newline='') as f:
    for en, de in odd:
        f.write(f'{en};{de}\n')
print('review files written')
