import json

FIX = {
    'since the fall of,': 'seit dem Fall von,',
    'such power...,:': 'solche Macht',
    'such power...,': 'solche Macht',
    'that food is near.': 'dass Futter naht.',
    'that rose from hell and,': 'die aus der Hoelle kam',
    'the Empire intensified their,': 'das Reich forcierte seine,',
    'the dormant ruins.': 'schlafende Ruinen.',
    'the fine details.': 'die Einzelheiten.',
    'the hard way.': 'harter Weg.',
    'the utopian civilization.': 'die utopische Kultur.',
    "they'll swarm you.": 'sie stuerzen heran',
    'thousands of years,,': 'tausende Jahre,,',
    'to defend the workers.': 'Arbeiter zu behueten,',
    'to destroy ourselves,': 'uns auszuloeschen,,',
    'to loathe the monsters.': 'Monster verabscheuen.',
    'to stop them.': 'zu stoppen.',
    'to the creatures we’ve,': 'Zu den Kreaturen, die',
    'to the creatures we\'ve,': 'Zu den Kreaturen, die',
    # quality fixes (already fit, but improve German)
    'that can destroy the Tower.': 'der Turm zerstoeren kann.',
    'that dragons have another origin.': 'Dass Drachen anders entstanden.',
    'to destroy the world with the,': 'die Welt mit ihr zu zerstoeren',
    'people into fearing their saviors?': 'Menschen ihre Retter fuerchten,',
    'ruins and towers.': 'Ruinen und Tuerme',
}

p = '_work/evt_batch13_norm.csv'
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
print('batch13 problems:', bad)
