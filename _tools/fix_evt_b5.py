#!/usr/bin/env python3
"""Batch-5 DE shortening fixes (DE-text based)."""
import json

OLD2NEW = {
    'Du strafst sie nicht mehr.': 'Keine Strafe mehr.',
    'Bin nicht wirklich sicher...': 'Nicht so sicher...',
    'Es tut mir leid...': 'Verzeih...',
    'Gewachsen bist du wahrlich': 'Du bist gewachsen wovh',
    'Ich bin... Edge.': 'Ich bin Edge.',
    'Ich... hab getoetet...': 'Ich hab toetet.',
    'Ich...,': 'Ich.',
    "Wenn's gut laeuft.": "Wenn's laeuft.",
    'Erinnerst du dich an mich,': 'Erinnerst du mich,',
    'Denk mal ein Kind wie du vor': 'Denk mal wie du vor',
    'Unreinheit entdeckt...': 'Unreinheit hier...',
    'Unreinheit gefunden...': 'Unreinheit dort...',
    'Unreinheit wiedergefunden...': 'Unreinheit abermals...',
    'In... der Tasche...,': 'In der Tasche...',
    'Unglaublich...,': 'Gewaltig...',
    'Jetzt ist es bei mir...,': 'Jetzt habe ich es...',
    'Das leichtete die Arbeit.': 'Das leicht Abstand.',
    'Das war Craymen!': 'Craymen!',
    'Es stand am Bett eingraviert,': 'Am Bett dies steht,',
    'Es ist Azel.': 'Azel!',
    'Es ist Craymen...': 'Craymen...',
    'Das ist die Falle!': 'Falle!',
    'Es ist zurueck!': 'Zurueck!',
    'Das ist sie!': 'Sie!',
    'Es ist aus der Kontrolle,': 'Aus der Kontrolle,',
    'Es ist so weit.': 'Es ist Zeit.',
    'Es ist so weit...': 'Es ist Zeit...',
    'Das bist du!': 'Du!',
    'Nur am Leben sei man gehalten.': 'Man hieN urda am Leben.',
}

disc = set()
for d in (1, 2, 3, 4):
    try:
        j = json.load(open('_work/evt_offsets_disc%d.json' % d, encoding='utf-8'))
        disc |= {e['text'] for e in j['entries']}
    except FileNotFoundError:
        pass

path = '_work/evt_batch5_norm.csv'
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
print(f'{path}: {n} applied')

bad = 0
for ln, line in enumerate(open(path, encoding='latin1'), 1):
    line = line.rstrip('\r\n')
    if not line or line.startswith('#'):
        continue
    if ';' not in line:
        print(f'  NOSEP {ln}: {line[:50]}')
        bad += 1
        continue
    en, de = line.split(';', 1)
    en, de = en.strip(), de.strip()
    if not de:
        continue
    if len(de) > len(en):
        print(f'  LONG {ln} ({len(de)}>{len(en)}) "{de}"')
        bad += 1
    if en not in disc:
        print(f'  NOEN {ln} {en[:50]!r}')
        bad += 1
print('problems:', bad)
