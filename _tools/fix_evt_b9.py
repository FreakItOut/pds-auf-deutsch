import json

SHORT = {
    'Das ist schlecht...': 'Das wird Uebel.',
    'Diese Stimme... der Drache!?,:': 'Die Stimme... Drache!?,:',
    'Diese Stimme... der Drache!?,': 'Die Stimme... Drache!?,',
    'Hier entlang.': 'Folg mir.',
    'Diese Bastarde...,': 'Dieses Pack..., ',
    'Diese Narren...,': 'Narren..., ',
    'Um ehrlich zu sein,,': 'Aufrichtig,,',
    'Zur Bewahrung der Vorherrschaft,': 'Zum Erhalt der Herrschaft,,',
    'Um den Turm abzuschalten,,': 'Den Turm ausschalten,,',
    'Bis heute sind wir geschuetzt': 'Noch heute sind wir behuetet',
    'Ausser du rettest das Maedchen...': 'Ausser, du holst das Maedchen',
    'Einsatz: Flaggschiff Grig Orig.': 'Das Schiff Grig Orig. nutzen',
    'Warte mal kurz.': 'Warte kurz.',
    'Warte... schau mal hier.': 'Moment... schau hier.',
    'Schaut auf den Bildschirm.': 'Achtet auf den Schirm.',
    'Wasser?': 'Wasser',
    'Wir sind stets einen Schritt': 'Wir sind immer einen Schritt',
    'Hilfe koennen wir immer gebrauchen': 'Hilfe ist stets willkommen.',
    'Das Imperium hat uns bezahlt,': 'Das Reich engagierte uns,',
    'Wir holen uns die Welt zurueck.': 'Wir holen uns die Welt zurueck',
    'Wir sehen ihm an, was er weiss.': 'Mal sehen, was er weiss.',
    'Wir sind nicht sein Level!': 'Wir sind viel zu schwach!',
    'Wir sind jetzt sicher,,': 'Wir sind sicher',
    'Wir sind jetzt sicher.': 'Alles sicher.',
    'Wir muessen die Basis aufgeben,,': 'Basis muessen wir aufgeben,,',
    'Diesmal haben wir verloren,,': 'Diesmal verloren,,',
    'Wir, die Sucher, sind...,:': 'Wir, die Sucher, hier...,:',
    'Wir, die Sucher, sind...,:': 'Wir, die Sucher, hier...,:',
    'Woran Craymen glaubte,,': 'Woran Craymen glaubt,,',
    'Was ist mit den Monstern?': 'Und die Monster?',
}

p = '_work/evt_batch9_norm.csv'
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
print('batch9 problems:', bad)
