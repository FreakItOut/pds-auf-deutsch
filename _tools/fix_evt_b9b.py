import json

FIX = {
    'Zur Bewahrung der Vorherrschaft,': 'Fuer die Vorherrschaft,,',
    'Schaut auf den Bildschirm.': 'Auf den Schirm.',
    'Wir sind stets einen Schritt': 'Immer einen voraus,',
    'Wir holen uns die Welt zurueck.': 'Wir holen die Welt zurueck',
    'Wir sind nicht sein Level!': 'Zu stark fuer uns!',
    'Wir, die Sucher, sind...,:': 'Wir, die Sucher, sind,,',
    'Wir, die Sucher, sind...,': 'Wir, die Sucher, sind,',
}

p = '_work/evt_batch9_norm.csv'
lines = open(p, encoding='latin1').read().splitlines()
n = 0
for i, line in enumerate(lines):
    if not line or line.startswith('#') or ';' not in line:
        continue
    en, de = line.split(';', 1)
    en, de = en, de.strip()
    new = FIX.get(de)
    if new is not None and len(new) <= len(en):
        lines[i] = f'{en};{new}'
        n += 1
open(p, 'w', encoding='latin1', newline='').write('\n'.join(lines) + '\n')
print(f'shortened: {n}')

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
print('batch9 problems:', bad)
