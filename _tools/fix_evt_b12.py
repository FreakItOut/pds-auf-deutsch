import json

FIX = {
    'follow us?': 'folgt uns?',
    'forever.': 'immerfort',
    'from Site 4.': 'von Ort 4.',
    'from the past,': 'alter Zeiten,',
    'have been ripped to pieces,': 'zerfetzt bis aufs Stueck',
    "here than anything you've,": 'hier als alles bei euch, dass',
    'how to obtain such power.': 'wie man so Macht erlangt.',
    'humans could live without fear.': 'Menschen Angstfrei leben.',
    'if I was... able to...,': 'obs ich dazu faehig...,:',
    'if I was... able to...,': 'was ich... konnte...,',
    "their own kind,, and don't": 'Wissen fuer den Wald,,',
    'information for their own kind,,': 'Wissen fuers their,,',
    'is already sealed.': 'ist schon versiegelt',
    'is on its way.': 'ist unterwegs.',
    'is the dragon itself!': 'der Drache himself!',
    'is the dragon itself!': 'der Drache selbst!',
    'just beyond this desert.': 'gleich nach der Wueste.',
    'left the Ancient Age in ruins.': 'verliess das Alter in Schutt.',
    'lower the weapon or not.': 'Waffe gesenkt oder nicht.',
    'mankind from extinction.': 'die Menschheit davor.',
    'meet me there.': 'Treff mich dort.',
}

p = '_work/evt_batch12_norm.csv'
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
    if any(ord(c) > 126 for c in de):
        print(f'  NONASCII {ln} {de!r}')
        bad += 1
print('batch12 problems:', bad)
