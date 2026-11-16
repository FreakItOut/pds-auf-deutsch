import json, glob

disc = set()
for d in (1, 2, 3, 4):
    try:
        j = json.load(open('_work/evt_offsets_disc%d.json' % d, encoding='utf-8'))
        disc |= {e['text'] for e in j['entries']}
    except FileNotFoundError:
        pass
bad = 0
total = 0
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
        # NB: do NOT strip EN keys - trailing spaces are part of the disc key
        en, de = en, de.strip()
        if not de:
            continue
        total += 1
        if len(de) > len(en):
            print(f'  LONG {path}:{ln} ({len(de)}>{len(en)}) "{de}"')
            bad += 1
        if en not in disc:
            print(f'  NOEN {path}:{ln} {en[:50]!r}')
            bad += 1
print(f'validated={total}, problems={bad}')
