import json

SHORT = {
    'Bereite den Bericht vor': 'Bereite den Report',
    'Schnell, drauf druecken.': 'Schnell, druecken!',
    'Das Volk zu schuetzen,': 'Das Volk zu schuetzen',
    'Verfolge sofort...': 'Verfolge sofort',
    'Beeil dich, raus hier.': 'Los, hol mich raus.',
    'Lauf Edge!': 'Lauf!',
    'Lauf um dein Leben!': 'Rennt ums Leben!',
    'Sucher ziehen immer weiter,': 'Sucher ziehen fort,',
    'Lager aufschlagen.': 'Lager auf!',
    'Sie wird dich beenden.': 'Sie beendet dich.',
    'So habt ihr euch kennengelernt': 'So kamt ihr zusammen',
    'Auch hier haben sie angegriffen...': 'Auch hier griffen sie an...',
    'Also bist du es...': "So, du bist's...",
    'Sorry, mehr kann ich nicht sagen...': 'Sorry, mehr kann ich nicht sagen.',
    'Warte... halt!': 'Warte, halt!',
    'Seltsamer Name.': 'Fremder Name.',
    'Dickkoepfiger Bengel!': 'Dickkopf!',
    'UEberrascht?': 'Staunt?',
    'Synchronisiere es mit der Waffe.': 'Synchronisiere es mit Waffe.',
    'Dank fuer die Aktivierung,': 'Dank der Aktivierung,',
    'Jene Flotte, jener Turm,': 'Jene Flotte, jener Turm',
    'Deshalb verteidige ich ihn...': 'Deshalb schuetze ich ihn...',
    'Der Mann, den du Craymen nennt,': 'Der Mann namens Craymen,',
    'Ist das alles, was du sagst?': 'Ist das alles, du sagst?',
    'Das ist alles.': "Das war's.",
    'Das ist nicht fair...': 'Nicht fair, das...',
    'Das weiss ich nicht.': 'Das kenn ich nicht.',
    "Der 'Goettliche Besucher'...": "Der 'Goettliche'...",
    'Die Akademie meldete, dass die': 'Die Akademie meldete, die',
    'Die Hauptstadt des Imperiums.': 'Hauptstadt des Imperiums.',
}

p = '_work/evt_batch7_norm.csv'
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
print('batch7 problems:', bad)
