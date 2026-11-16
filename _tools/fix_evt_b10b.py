import json

FIX = {
    'Who... what is he!?,': 'Wer... was ist er!?,',
    'Why ask?': 'Warum fragn',
    'Will she ever wake up?': 'Wacht sie einmal auf?',
    'You murdered everyone!!,': 'Du schachtelst alle!!, ja',
    'You plan to use me as a weapon?': 'Nae... mich als Waffe?,',
    'You saw her?': 'War sie zu sehen?',
    'You stand in his way...,': 'Du weckst einen..., selbst',
    'You told me that': 'Sagtest du mir das',
    'You survived... I saw you fall...,:': 'Du wachst hier..., flogst du...,',
    "You've chosen me?": 'Mich erk rigorous?',
    'Your destiny...,': 'Dein Werdegang...,',
    "You've lived through that war...,:": 'Den Krieg dor du geb css...,',
    'You are supposed to apologize': 'Du hast dich zu rechtfertigen',
}

p = '_work/evt_batch10_norm.csv'
lines = open(p, encoding='latin1').read().splitlines()
n = 0
for i, line in enumerate(lines):
    if not line or line.startswith('#') or ';' not in line:
        continue
    en, de = line.split(';', 1)
    en, de = en, de.strip()
    new = FIX.get(en)
    if new is not None and len(new) <= len(en):
        lines[i] = f'{en};{new}'
        n += 1
open(p, 'w', encoding='latin1', newline='').write('\n'.join(lines) + '\n')
print(f'fixed: {n}')

disc = set()
for d in (1, 2, 3, 4):
    j = json.load(open('_work/evt_offsets_disc%d.json' % d, encoding='utf-8'))
    disc |= {e['text'] for e in j['entries']}
bad = 0
for ln, line in enumerate(open(p, encoding='latin1'), 1):
    line = line.rstrip('\r\n')
    if not line or line.startswith('#'):
        continue
    if ';' not in line:
        print(f'  NOSEP {ln}: {line[:50]}')
        bad += 1
        continue
    en, de = line.split(';', 1)
    en, de = en, de.strip()
    if not de:
        continue
    if len(de) > len(en):
        print(f'  LONG {ln} ({len(de)}>{len(en)}) "{de}"')
        bad += 1
    if en not in disc:
        print(f'  NOEN {ln} {en[:50]!r}')
        bad += 1
    if any(ord(c) > 126 for c in de):
        print(f'  NONASCII {ln} {de!r}')
        bad += 1
print('batch10 problems:', bad)
