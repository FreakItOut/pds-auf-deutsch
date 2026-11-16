import json, os

# --- 1) fix separator lines in evt_batch6.csv (EN ends with comma, joined by comma) ---
SEP_FIX = [
    ('Kid, don\'t interfere,Junge, misch dich nicht ein', 'Kid, don\'t interfere;Junge, misch dich nicht ein'),
    ('My legs are pinned, so,Meine Beine stecken fest,', 'My legs are pinned, so;Meine Beine stecken fest,'),
    ('No man should wield,Kein Mensch sollte tragen', 'No man should wield;Kein Mensch sollte tragen'),
    ('No one would suspect a man like me to,Niemand wage bei mir davon', 'No one would suspect a man like me to;Niemand wage bei mir davon'),
    ('Now, Divine One,,Nun, Goettlicher,', 'Now, Divine One,,Nun, Goettlicher,'.replace('One,,Nun', 'One,;Nun')),
    ('Now, on to the next phase...,Weiter zur naechsten Phase...', 'Now, on to the next phase...;Weiter zur naechsten Phase...'),
    ('Now... press the button,,Jetzt den Knopf druecken,', 'Now... press the button,,Jetzt den Knopf druecken,'.replace('n,,Jetzt', 'n,;Jetzt')),
    ('Of course, if there were,Natuerlich, wenn es', 'Of course, if there were;Natuerlich, wenn es'),
    ('Our only purpose is to,Unser einziger Zweck ist,', 'Our only purpose is to;Unser einziger Zweck ist,'),
    ('Perhaps, but he woke me,Vieleicht, doch er weckte mich', 'Perhaps, but he woke me;Vielleicht, doch er weckte mich'),
    ('Please, try to be on time.,Sei bitte puenktlich,', 'Please, try to be on time.;Sei bitte puenktlich,'),
]
p = '_work/evt_batch6.csv'
txt = open(p, encoding='latin1').read()
n = 0
for old, new in SEP_FIX:
    if old in txt:
        txt = txt.replace(old, new)
        n += 1
open(p, 'w', encoding='latin1', newline='').write(txt)
print(f'batch6.csv separators fixed: {n}/11')

# --- 2) regenerate batch6_norm.csv fresh ---
if os.path.exists('_work/evt_batch6_norm.csv'):
    os.remove('_work/evt_batch6_norm.csv')

disc = set()
for d in (1, 2, 3, 4):
    j = json.load(open('_work/evt_offsets_disc%d.json' % d, encoding='utf-8'))
    disc |= {e['text'] for e in j['entries']}

def norm(en):
    if en in disc:
        return en
    for cand in (en.rstrip(','), en + ','):
        if cand in disc:
            return cand
    key = en.replace(',', '').replace('  ', ' ')
    hits = [t for t in disc if t.replace(',', '').replace('  ', ' ') == key]
    if len(hits) == 1:
        return hits[0]
    hits = [t for t in disc if t.startswith(en[:min(20, len(en))])]
    if len(hits) == 1:
        return hits[0]
    return None

out = []
for line in open('_work/evt_batch6.csv', encoding='latin1').read().splitlines():
    if not line or line.startswith('#'):
        out.append(line)
        continue
    en, de = line.split(';', 1)
    en, de = en.strip(), de.strip()
    real = norm(en)
    out.append(f'{real};{de}' if real else f'{en};{de}')
open('_work/evt_batch6_norm.csv', 'w', encoding='latin1', newline='').write('\n'.join(out) + '\n')
print('norm regenerated')

# --- 3) shorten the too-long DE values (by DE text match) ---
SHORT = {
    'Frag ich mal,': 'Frag mal,',
    'Hoer seine Geschichte.': 'Hoer seine Story.',
    'Ich?': 'Ich',
    'Botschaft': 'Meldung',
    'Ein Freund schrieb mir das': 'Ein Freund schrieb es',
    'Meine Maenner stehen bereit.': 'Maenner stehen bereit.',
    'Unmoeglich.': 'Nein.',
    'Nicht viel... gar nicht.': 'Nicht mehr viel.',
    'Ueberhaupt nichts...': 'Gar nichts...',
    'Ich halt die Zukunft der Menschheit!': 'Nun halt ich die Menschheit!',
    'Und jetzt?': 'Was nun?',
    'Das Imperium hat natuerlich nicht': 'Das Reich hat es nicht mehr',
    'Nur meine Kraefte sind anders.': 'Nur die Kraefte sind anders.',
    'Oeffne das Tor, Azel!': 'Oeffne das Tor!',
    'Unsere Seite?': 'Wir auch?',
    'Bitte hilft uns.': 'Hilf uns bitte.',
    'Bitte warte auf mich!!': 'Warte auf mich!!',
}
lines = open('_work/evt_batch6_norm.csv', encoding='latin1').read().splitlines()
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
open('_work/evt_batch6_norm.csv', 'w', encoding='latin1', newline='').write('\n'.join(lines) + '\n')
print(f'shortened: {n}')

# --- 4) final validation of batch6_norm only ---
bad = 0
for ln, line in enumerate(open('_work/evt_batch6_norm.csv', encoding='latin1'), 1):
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
print('batch6 problems:', bad)
