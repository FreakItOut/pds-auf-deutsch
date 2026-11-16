#!/usr/bin/env python3
"""Replace DE values by exact DE string match (line-number independent)."""
import glob, json

OLD2NEW = {
    '...Hoffe, du hast recht,': '...Hoffe, recht zu haben,',
    '...Ich... lebe noch!?': '...Lebe ich noch!?',
    'Aber...': 'Aber',
    'Edge, das ist Krieg.': 'Das ist Krieg.',
    'Edge, wir brauchen dich.': 'Wir brauchen dich.',
    'Vor allem wenn der Eindringling': 'Wenn der Eindringling',
    'Selbst auch wir ihn fingen,': 'Wenn wir ihn fangen,',
    'Selbst in deinem kurzen Einsatz': 'Selbst bei deinem Einsatz',
    'Ausgezeichnet.': 'Prima.',
    'Nur wenige versuchen es,': 'Wenige versuchen,',
    'Fuer einen Neubeginn.': 'Fuer neuen Anfang.',
    'Nach meiner Erfahrung,': 'Nach Erfahrung,',
    'Runter auf den Boden!': 'Auf den Boden!',
    'Sprich...': 'Sprich.',
    'Los! Schnell!': 'Los!',
    'Er toetete meine Freunde.': 'Er toetete Freunde.',
    'Er ist verrucht und ein Wahnsinniger,': 'Wahnsinniger mit Plan,',
    'Er ist tot.': 'Er ist tot',
    'Hier ist es.': 'Hier ist es',
    'Ehrlich gesagt,': 'Ehrlich,',
    'Wie geht es ihr?': 'Wie gehts ihr?',
    'Schnell! Die Befehlsflotte': 'Die Befehlsflotte',
    'Schnell!': 'Los!',
    'Ich bin nicht...': 'Bin nicht...',
}

disc = set()
for d in (1, 2, 3, 4):
    try:
        j = json.load(open(f'_work/evt_offsets_disc{d}.json', encoding='utf-8'))
        disc |= {e['text'] for e in j['entries']}
    except FileNotFoundError:
        pass

for path in sorted(glob.glob('_work/evt_batch*_norm.csv')):
    lines = open(path, encoding='latin1').read().splitlines()
    n = 0
    for i, line in enumerate(lines):
        if not line or line.startswith('#') or ';' not in line:
            continue
        en, de = line.split(';', 1)
        en, de = en.strip(), de.strip()
        new = OLD2NEW.get(de)
        if new is not None and len(new) <= len(en):
            lines[i] = f'{en};{new}'
            n += 1
    open(path, 'w', encoding='latin1', newline='').write('\n'.join(lines) + '\n')
    print(f'{path}: {n} replacements applied')

# final check
bad = 0
for path in sorted(glob.glob('_work/evt_batch*_norm.csv')):
    for ln, line in enumerate(open(path, encoding='latin1'), 1):
        line = line.rstrip('\r\n')
        if not line or line.startswith('#'):
            continue
        if ';' not in line:
            print(f'  NOSEP {path}:{ln}: {line[:50]}')
            bad += 1
            continue
        en, de = line.split(';', 1)
        en, de = en.strip(), de.strip()
        if not de:
            continue
        if len(de) > len(en):
            print(f'  LONG {path}:{ln} ({len(de)}>{len(en)}) "{de}"')
            bad += 1
        if en not in disc:
            print(f'  NOEN {path}:{ln} {en[:50]!r}')
            bad += 1
print('remaining problems:', bad)
