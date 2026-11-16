import json

SHORT = {
    'Das Flaggschiff Grig Orig.': 'Flaggschiff Grig Orig.',
    'Der Turm, die Monster,, hat': 'Turm, Monster, beides,',
    'Das Zeitalter neu erstanden.': 'Neues Zeitalter begann.',
    'Die Pflicht, die w\u00e4hrte,': 'Die lange Pflicht,',
    'Die Monster sind toedlicher': 'Monster sind da toedlicher',
    'Der Einzige, der uns befreit,': 'Der Einzige, uns befreit,',
    'Der Pfad nach Uru.': 'Pfad nach Uru.',
    'Der Ort, an dem ich': 'Ort, an dem ich',
    'Die Ueberlebenden leben in Angst': 'Ueberlebende leben in Angst',
    'Die Reise, die begann,,': 'Die Reise, die begann,',
    'Dann stieg das Reich zur Macht,': 'Dann kam das Reich zur Macht,',
    'Du musst der Goettliche sein...': 'Du bist wohl der Goettliche...',
    'Weniger Monster gibt es hier,,': 'Es gibt weniger Monster,',
    'Es war ein Maedchen.': 'Ein Maedchen.',
    'Diese Kreaturen sind blind.': 'Die Kreaturen sind blind.',
    'Sie ziehen nach Norden,,': 'Sie fahren nach Norden,',
    'Sie sind keine Kreaturen,': 'Sie sind keine Wesen',
    'Sie halten Drachen fuer Daemonen': 'Drachen sind Daemonen fuer sie',
    'Sie koennen nicht mal b. einer': 'Sie schaffen das nicht',
    'Sie haben einen Zweck.': 'Sie haben ein Ziel.',
    'Sie streifen nie weit ab,': 'Sie streifen nie weit ab',
    'Sie schuetzen uns!?': 'Sie schuetzen uns',
    'Sie waren alle gute Menschen...': 'Alle waren gute Menschen...',
    'Sie werden nie imstande sein,': 'Nie koennen sie das,',
}

p = '_work/evt_batch8_norm.csv'
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
print('batch8 problems:', bad)
