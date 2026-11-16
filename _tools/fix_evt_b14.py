import json

FIX = {
    'we must destroy the Tower...': 'muessen den Turm zerstoeren',
    'we must go.': 'Muessen wir',
    'we need Azel.': 'brauchen Azel',
    'we were betrayed.': 'Man verraet uns.',
    'what can we do?': 'Was tun wir?',
    'what could we do!?': 'Was zur Hoelle!?',
    'what you did!!': 'was du tatst',
    'where I awoke.': 'mein Aufwachen',
    'where we met for the first time?': 'wo wir uns zuerst trafen?',
    'who leads the Black Fleet...': 'Fuehrer der Schwarzflotte...',
    'who the real enemy is.': 'wer der Feind ist.',
    'wield such power...': 'solche Macht',
    'with the Empire,': 'mit dem Imperium',
    'world, the humans will just,': 'Welt, da werden Menschen',
    'you must have learned': 'musst gelernt haben',
    'you worthless hunter!': 'Verdammter Jaeger!',
    "you're as good as dead.": 'So gut wie tot.',
    "you've got Craymen": 'hast du Craymen',
    'your dragon...': 'dein Drache...',
}

p = '_work/evt_batch14_norm.csv'
lines = open(p, encoding='latin1').read().splitlines()
n = 0
for i, line in enumerate(lines):
    if not line or line.startswith('#') or ';' not in line:
        continue
    en, de = line.split(';', 1)
    en, de = en, de.strip()
    new = FIX.get(en)
    if new is not None and len(new) <= len(en):
        lines[i] = f'{en};{new}'
        n += 1
open(p, 'w', encoding='latin1', newline='').write('\n'.join(lines) + '\n')
print(f'fixed: {n}')

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
print('batch14 problems:', bad)
