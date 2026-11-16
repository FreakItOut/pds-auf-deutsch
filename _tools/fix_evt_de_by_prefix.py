import glob

# targeted replacements by EN prefix within *_norm.csv
TARGETS = {
    "...I hope you're right": '...Hoffe, du hast recht',
    "...I'm ...alive!?": 'Leb ich noch!?',
    "How is she?": 'Gings ihr?',
    "I am not...": 'Bin nicht',
}

for path in sorted(glob.glob('_work/evt_batch*_norm.csv')):
    lines = open(path, encoding='latin1').read().splitlines()
    n = 0
    for i, line in enumerate(lines):
        if not line or line.startswith('#') or ';' not in line:
            continue
        en, de = line.split(';', 1)
        en, de = en.strip(), de.strip()
        for pref, newde in TARGETS.items():
            if en.startswith(pref) and len(newde) <= len(en):
                lines[i] = f'{en};{newde}'
                n += 1
    open(path, 'w', encoding='latin1', newline='').write('\n'.join(lines) + '\n')
    print(f'{path}: {n} targeted replacements')

# validate
import json
disc = set()
for d in (1,2,3,4):
    try:
        j = json.load(open(f'_work/evt_offsets_disc{d}.json', encoding='utf-8'))
        disc |= {e['text'] for e in j['entries']}
    except FileNotFoundError:
        pass
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
