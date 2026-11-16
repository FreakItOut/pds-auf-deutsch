import json
path = '_work/evt_batch5_norm.csv'
lines = open(path, encoding='latin1').read().splitlines()
FIX = {
    11: (',Ich bin... Edge.', 'Ich... Edge.'),
    19: (',Ich... hab getoetet...,', 'Getoetet habe ich...'),
}
disc = set()
for d in (1, 2, 3, 4):
    j = json.load(open('_work/evt_offsets_disc%d.json' % d, encoding='utf-8'))
    disc |= {e['text'] for e in j['entries']}

for i, line in enumerate(lines):
    if ';' not in line or not line or line.startswith('#'):
        continue
    en, de = line.split(';', 1)
    en_e, de_e = en.strip(), de.strip()
    target = None
    if en_e.startswith("I've got to find my Captain."):
        target = ("I've got to find my Captain. ", 'Mein Kapitaen ist dort.')
    elif en_e.startswith("It's a distress signal."):
        target = ("It's a distress signal. ", 'Ein Notsignal.')
    elif de_e == 'Ich bin... Edge.':
        if len('Ich... Edge.') <= len(en_e):
            target = (en_e, 'Ich... Edge.')
    elif de_e == 'Ich... hab getoetet...,':
        if len('Getoetet habe ich...') <= len(en_e):
            target = (en_e, 'Getoetet habe ich...')
    if target is not None:
        lines[i] = f'{target[0]};{target[1]}'
open(path, 'w', encoding='latin1', newline='').write('\n'.join(lines) + '\n')

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
