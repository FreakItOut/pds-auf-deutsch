p = '_work/evt_batch8_norm.csv'
data = open(p, 'rb').read().decode('latin1')
lines = data.splitlines()

FIX = {
    'The age started anew.': 'Neues Alter begann.',
    'Die Pflicht, die w\u00c3\u00a4hrte,': 'Die lange Pflicht,',
    'The monsters are deadlier': 'Monster sind toedlicher',
    'The survivors live in fear': 'Ueberlebende in Angst',
}
n = 0
for i, line in enumerate(lines):
    if not line or line.startswith('#') or ';' not in line:
        continue
    en, de = line.split(';', 1)
    en, de = en, de.strip()
    new = FIX.get(de) or FIX.get(en)
    if new is not None and len(new) <= len(en):
        lines[i] = f'{en};{new}'
        n += 1
open(p, 'wb').write(('\n'.join(lines) + '\n').encode('latin1'))
print(f'fixed: {n}')

disc = set()
for d in (1, 2, 3, 4):
    j = __import__('json').load(open('_work/evt_offsets_disc%d.json' % d, encoding='utf-8'))
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
print('batch8 problems:', bad)
