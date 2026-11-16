import json, io, glob

path = '_work/evt_batch5_norm.csv'
lines = open(path, encoding='latin1').read().splitlines()
FIX = {
    11: 'Ich... Edge.',
    14: None,  # handled by key fix below
    19: 'Getoetet habe ich...',
}
for i, line in enumerate(lines):
    if not line or line.startswith('#') or ';' not in line:
        continue
    en, de = line.split(';', 1)
    en_e, de_e = en.strip(), de.strip()
    # key corrections (add trailing spaces where disc requires)
    if en_e == "I've got to find my Captain.":
        lines[i] = "I've got to find my Captain. ;Mein Kapitaen ist dort."
        continue
    if en_e == "It's a distress signal.":
        lines[i] = "It's a distress signal. ;Ein Notsignal."
        continue
    for ln in (10, 11, 19, 50, 51, 52, 57, 58, 60, 61):
        pass
    new = None
    if de_e == 'Gewachsen bist du wahrlich':
        new = 'Du bist gewachsen,'
    elif de_e == 'Ich... Edge.':
        new = de_e
    elif de_e == 'Ich... hab getoetet...,':
        new = 'Getoetet habe ich...'
    elif de_e == 'Das ist die Falle!,':
        new = 'Die Falle!'
    elif de_e == 'Es ist zurueck!,':
        new = 'Zurueck!'
    elif de_e == 'Das ist sie!,':
        new = 'Sie!'
    elif de_e == 'Es ist so weit.':
        new = 'So weit.'
    elif de_e == 'Es ist so weit...,':
        new = 'So weit...'
    elif de_e == 'Das bist du!,':
        new = 'Bist du!'
    elif de_e == 'Nur am Leben sei man gehalten.':
        new = 'Nur am Leben zu sein.'
    if new is not None and len(new) <= len(en_e):
        lines[i] = f'{en_e};{new}'
open(path, 'w', encoding='latin1', newline='').write('\n'.join(lines) + '\n')

disc = set()
for d in (1, 2, 3, 4):
    j = json.load(open('_work/evt_offsets_disc%d.json' % d, encoding='utf-8'))
    disc |= {e['text'] for e in j['entries']}
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
