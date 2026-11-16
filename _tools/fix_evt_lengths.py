#!/usr/bin/env python3
"""Apply shortened DE replacements to *_norm.csv files by line number."""
import re

FIXES = {
    '_work/evt_batch1_norm.csv': {
        5: '...Traum?',
        6: '...Start von D Typ 01...',
        14: '...Hoffe, recht zu haben,',
        15: '...Lebe ich noch!?',
        17: 'Kraefte?',
        18: 'So viele davon.',
        22: 'Das Deck des Schiffs',
        33: 'Bestie?',
        37: 'Shelcoof starten...',
        39: 'Nun bin ich bei dir.',
        40: 'Verloren.',
        41: 'Gut, gut.',
        43: 'Er riss die Hauptstadt nieder,',
        44: 'Wow...',
        45: 'Kaiserstaffel!?',
        48: 'Und jetzt stirbst du.',
        52: 'Alles okay!?',
        56: 'Sicher, dass sie nicht',
        57: 'Bist du der Goettliche Gast?',
        59: 'Den Jaeger?',
        63: 'Azel bleibt...',
    },
    '_work/evt_batch2_norm.csv': {
        2: 'Azel! Nein!',
        8: 'Bett',
        9: 'Doch ich fand sie an.',
        12: 'Hier endet es.',
        16: 'Nur das nicht.',
        17: 'Doch das...',
        20: 'Warum erst...',
        21: 'Doch da ist niemand mehr,',
        22: 'Aber...',
        23: 'Kannst du?',
        24: 'Chef!!',
        25: 'Chef!',
        27: 'Chef?',
        28: 'Langsam raus,',
        30: 'Craymen fuehrt Monster',
        33: 'Craymen zahlt.',
        42: 'Mist!',
        43: 'Verdammt',
        51: 'Goettlich?',
        55: 'Spiel keine Spiele, eh?',
        56: 'Feuer ein!!',
        57: 'Feuer ein!',
    },
    '_work/evt_batch3_norm.csv': {
        2: 'Edge, kannst auf dich:',
        3: 'Edge, das Dorf, erinnerst du,',
        4: 'Mein Junge,',
        5: 'Das ist Krieg.',
        6: 'Wir brauchen dich.',
        10: 'Das Imperium macht es gut.',
        12: 'Bei einem Eindringling',
        14: 'Hatten wir ihn auch,',
        15: 'Bei deinem kurzen Einsatz,',
        17: 'Super.',
        19: 'Wenige versuchen,',
        22: 'Fuer neues Leben.',
        25: 'Nach Erfahrung,',
        26: 'Aus der Vorzeit?',
        30: 'Jag Craymen.',
        32: 'Auf den Boden!',
        33: 'Sprich.',
        34: 'Los!',
        38: 'Er hielt uns damit auf,',
        41: 'Er toetete Freunde.',
        44: 'Wahnsinniger mit Plan,',
        45: 'Lugender Moerder!',
        46: 'Er ist tot',
        47: 'Da ist es.',
        48: 'Hey! Bleib bei Sinnen!',
        49: 'Hey! Still!',
        53: 'Ehrlich.',
        54: 'Wie ihr?',
        56: 'Die Befehlsflotte!',
        58: 'Los!',
        61: 'Nicht...',
    },
}

for path, fx in FIXES.items():
    lines = open(path, encoding='latin1').read().splitlines()
    for ln, de in fx.items():
        if 1 <= ln <= len(lines):
            line = lines[ln - 1]
            if not line or line.startswith('#'):
                print(f'  SKIP line {ln} in {path} (comment/blank)')
                continue
            parts = line.split(';', 1)
            if len(parts) < 2:
                # try splitting at final comma (my earlier comma typo)
                idx = line.rfind(',')
                en_raw, de_raw = line[:idx], line[idx+1:].strip()
                sfx = ';' + de
                lines[ln - 1] = en_raw + sfx
                print(f'  fixed sep line {ln} in {path}: {en_raw[:40]};{de[:30]}')
                continue
            en = parts[0]
            if len(de) > len(en):
                print(f'  STILL LONG line {ln} in {path} ({len(de)}>{len(en)}): {de}')
                continue
            lines[ln - 1] = f'{en};{de}'
    open(path, 'w', encoding='latin1', newline='').write('\n'.join(lines) + '\n')
    print(f'{path}: updated')

# final re-validate through the norm tool (inlined quick check)
print('\nQuick length check:')
import json, glob
disc = set()
for d in (1, 2, 3, 4):
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
            print(f'  NOSEP {path}:{ln} {line[:50]}')
            bad += 1
            continue
        en, de = line.split(';', 1)
        en, de = en.strip(), de.strip()
        if de and len(de) > len(en):
            print(f'  LONG {path}:{ln} ({len(de)}>{len(en)}) "{de}"')
            bad += 1
        if de and en not in disc:
            print(f'  NOEN {path}:{ln} "{en[:50]}"')
            bad += 1
print('remaining problems:', bad)
