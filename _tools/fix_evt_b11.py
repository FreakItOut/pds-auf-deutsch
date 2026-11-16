import json

SHORT = {
    'Deine Maenner?': 'Deine',
    'Zadoc der Compiler weiss,': 'Zadoc der Compiler weiss',
    'Alles falsch.': 'Falsch.',
    'all deiner Toten Freunde.': 'alle toten Freunde.',
    'entlang des Tals...,': 'durch das Tal...,',
    'eine endende Ressourcen-Versch.,,': 'endlose Verschwendung, alles,',
    'ein Auge auf dich.': 'Auge auf dich.',
    'und Ehrgeiz zum Krieg.': 'und Eifer zum Krieg',
    'und den Menschen zu geben': 'und den Menschen',
    'und was diese Maenner sagen...,': 'was diese Maenner sagen...',
    'als feinfuehliges Gleichmass.': 'als feine Balance.',
    'doch innen drin bin ich naecher': 'doch innerlich bin ich nah,',
    'doch was ist deine Bestimmung?,:': 'doch was ist deine Aufgabe?,:',
    'doch was ist deine Bestimmung?,': 'doch was ist deine Aufgabe?,',
    'doch wenn wir hier raus sind,,': 'doch wenn wir hier draussen,,',
    'von der eigenen Flotte...,': 'durch die Flotte...',
    'Zivilisation auf ihrer Seite.': 'Zivilisation an ihrer Seite.',
    'bestaetigt...,:': 'bestaetigt...',
    'bestaetigt...,': 'bestaetigt...',
    'Kontinente in einer Nacht...,': 'Kontinente in einer Nacht...',
    'die Welt kontrollieren.': 'Welt beherrschen.',
    'ueberseht mit Monstern.': 'von Monstern bedeckt.',
    'zerstoere diesen Turm.': 'zerstoer den Turm.',
    'Drachen sind angesehen als': 'Drachen gelten als',
    'entziehn unserem Griff.': 'uns zu entgleiten',
    'von MINSERTEN leicht. verwaltet': 'von normalen Maennern leicht',
    'die Herrung des Schicksals.': 'die Lenkung des Schicksals.',
    'durch Macht des Alten Alters.': 'durch die Macht des Altertums.',
}

p = '_work/evt_batch11_norm.csv'
lines = open(p, encoding='latin1').read().splitlines()
n = 0
for i, line in enumerate(lines):
    if not line or line.startswith('#') or ';' not in line:
        continue
    en, de = line.split(';', 1)
    en, de = en, de.strip()
    new = SHORT.get(de)
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
print('batch11 problems:', bad)
