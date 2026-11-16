import json

SHORT = {
    'Was ist los, Edge?': "Was gibts, Edge?",
    'Wenn ich fort bin...,:': 'Wenn ich fort bin...,',
    'Wenn ich fort bin...,': 'Bin ich fort...,',
    'Wenn du nach Sestren gehst,,': 'Wenn du Sestren suchst,,',
    'Wer... was ist er!?,': 'Wer... wer ist er!?,',
    'Warum fragen?': 'Warum frag',
    'Warum grifft ihr mich an?': 'Warum griffen sie an?',
    'Warum kommst du nicht mit?,:': 'Warum kommst du nicht mit,',
    'Warum kommst du nicht mit?,': 'Warum kommst du her?,',
    'Warum?': 'Wiso',
    'Wacht sie je wieder auf?': 'Wacht sie noch mal auf?',
    'Du solltest dich entschuldigen': 'Du hast dich zu entschuldigen',
    'Du kannst den Drachen lenken,,': 'Kannst den Drachen lenken,,',
    'Allein schaffst du sie nicht.': 'Allein geht das nicht.',
    'Kuemmere dich um die Monster.': 'Deine Sache sind Monster.',
    'In unsere Falle getappt.': 'In der Falle gefangen.',
    'Du hast alle ermordet!!, ja': 'Du ermordetest alle!!, ja',
    'Du brauchst Azel... was?,:': 'Du brauchst Azel... was?',
    'Du brauchst Azel... was?,': 'Womit Azel prudent... was?,',
    'Du hast sie gesehen?': 'Sahst sie du?',
    'Du stehst ihm im Weg...,:': 'Im Weg du ihm stehst...,',
    'Du stehst ihm im Weg...,:': 'Im Weg du ihm stehst...,',
    'Du stehst ihm im Weg...,': 'Du weckst einen Gegner...,',
    'Du sagtest mir das': 'Du sagtest mir das das',
    'Du bist hier.': 'Hier bist du.',
    'Du hast mich erkoren?': 'Ich wurde auserwählt?',
    'Diese Krieg hast du ueberlebt...,:': 'Den Krieg ueberlebtst du...,:',
    'Diese Krieg hast du ueberlebt...,': 'Den Krieg ueberlebt du...,',
    'Du... bist unsere einzige Hoffnung.': 'Du, unsere Hoffnung.',
    'Dein Schicksal...,:': 'Dein Schicksal...,',
    'Dein Schicksal...,': 'Schicksal deiner...,:',
}

p = '_work/evt_batch10_norm.csv'
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
print('batch10 problems:', bad)
