#!/usr/bin/env python3
"""One-shot DE shortening map over all *_norm.csv (ignores _norm_norm)."""
import json

OLD2NEW = {
    # batch 1
    '...Ein Traum?': '...Traum?',
    '...Aktivierung von D Typ 01...': '...Start von D Typ 01...',
    '...Hoffe, du hast recht,': '...Hoffe, du recht',
    '...Ich... lebe noch!?': 'Leb ich noch!?',
    '...Kraefte?': 'Kraefte?',
    '...So viele von ihnen.': 'So viele davon.',
    '...Das Deck jenes Schiffs': 'Das Deck des Schiffs',
    'Eine Bestie?': 'Bestie?',
    'Shelcoof aktivieren...': 'Shelcoof starten...',
    'Wieder schulde ich dir was.': 'Nun bin ich bei dir.',
    'Alles ist verloren.': 'Verloren.',
    'Einverstanden,': 'Gut, gut.',
    'Zwar zerstoerte er die Hauptstadt,': 'Er riss die Hauptstadt nieder,',
    'Unglaublich...': 'Wow...',
    'Eine kaiserliche Staffel!?': 'Kaiserstaffel!?',
    'Und nun wirst du sterben.': 'Und jetzt stirbst du.',
    'Bist du in Ordnung!?': 'Alles okay!?',
    'Bist du sicher, dass sie nicht': 'Sicher, dass sie nicht',
    'Bist du der Goettliche Besucher?': 'Bist du der Goettliche Gast?',
    'Was den Jaeger angeht,': 'Den Jaeger?',
    'Azel ist immer noch...': 'Azel bleibt...',
    # batch 2
    'Azel! Nein!!!!': 'Azel! Nein!',
    'Bett?': 'Bett',
    'Aber ich fand sie zuerst.': 'Doch ich fand sie an.',
    'Doch hier endet es.': 'Hier endet es.',
    'Aber das ist nicht alles.': 'Nur das nicht.',
    'Aber das ist...': 'Doch das...',
    'Aber warum jetzt...': 'Warum erst...',
    'Doch es ist niemand mehr da,': 'Doch da ist niemand mehr,',
    'Aber...': 'Aber',
    'Kannst du stehen?': 'Kannst du?',
    'Kapitaen!!': 'Chef!!',
    'Kapitaen!': 'Chef!',
    'Kapitaen?': 'Chef?',
    'Langsam herauskommen,': 'Langsam raus,',
    'Craymen fuehrte die Monster': 'Craymen fuehrt Monster',
    'Craymen zahlt dafuer...': 'Craymen zahlt.',
    'Verdammt!': 'Mist!',
    'Verfluchter...': 'Verdammt',
    'Goettlicher Besucher?': 'Goettlich?',
    'Spielkeine Spiele mit mir!': 'Spiel keine Spiele, eh?',
    'Nicht schiessen!!': 'Feuer ein!!',
    'Nicht schiessen!': 'Feuer ein!',
    # batch 3 (remaining)
    'Aus dem Alten Zeitalter?': 'Aus der Vorzeit?',
    'Folge Craymen nach.': 'Jag Craymen.',
    'Das tat er, um uns aufzuhalten,': 'Er hielt uns damit auf,',
    'Er ist ein lugender Moerder!': 'Lugender Moerder!',
    'Hey! Verliere nicht das Bewusstsein!': 'Hey! Bleib bei Sinnen!',
    'Hey! Nicht bewegen!!': 'Hey! Still!',
    'Wie geht es ihr?': 'Gings ihr?',
    'Ich bin nicht...': 'Bin nicht',
    # batch 4
    'Ich... nur ich allein...': 'Ich... nur ich hier...',
    'Ich kann helfen,': 'Kann helfen,',
    'Sestren erreich ich nicht.': 'Sestren geht nicht.',
    'Sie konnten sie wohl nicht halten.': 'Sie hielt sie nicht auf.',
    'Habe Merkwuerdiges zu erzaehlen...': 'Habe dir zu erzaehlen...',
    'Weil ich nicht verziehen hab.': 'Ich verziehe nicht.',
    'Ich weiss!': 'Weiss!',
    'Ich weiss.': 'Weiss.',
    'Ich liebe dich...': "Lieb' dich...",
    'Ich seh menschlich aus wie du,': 'Wie du, menschlich gefasst,',
    'Ich bereitete nur die Buehne.': 'Bereitete die Buehne.',
    'Ich muss hier bleiben.': 'Muss hier sein.',
    'Ich muss erst den Grund wissen.': 'Der Grund fehlt mir.',
    'Ich musste rucksichtslos sein.': 'Rucksichtslos war es.',
    'Dein Name mir nie kund war.': 'Dein Name blieb kundlos',
    'Ach... nur ein Traum...,': 'Ach, nur ein Traum,',
    'Ich denke...': 'Dein...',
    'Ich brauche Antworten.': 'Antworten!',
    'Ich will die Wahrsagung...': 'Die Wahrsagung...',
    'Ich muss wissen': 'Muss wissen',
    'Ich war an eurer Grabesstaette.': 'Ich war an der Grabstatt.',
    'Das Imperium schickte mich,': 'Das Reich schickt mich,',
    'Ich wurde gelehrt...,': 'Man lehrte es...',
    'Der hat sicher Angst gehabt!': 'Hat sicher Angst gehabt!',
    'Ich fuehle... er muss sein...,': 'Ich fuehle... er muss...',
}

import glob
for path in sorted(glob.glob('_work/evt_batch*_norm.csv')):
    if path.endswith('_norm_norm.csv'):
        continue
    lines = open(path, encoding='latin1').read().splitlines()
    n = 0
    for i, line in enumerate(lines):
        if not line or line.startswith('#') or ';' not in line:
            continue
        en, de = line.split(';', 1)
        en, de = en.strip(), de.strip()
        new = OLD2NEW.get(de)
        if new is not None and len(new) <= len(en):
            lines[i] = f'{en};{new}'
            n += 1
    open(path, 'w', encoding='latin1', newline='').write('\n'.join(lines) + '\n')
    print(f'{path}: {n} replacements')

# pre-fix reminders for prefix specials
print('\n(psst: run fix_evt_de_by_prefix.py next)')

disc = set()
for d in (1, 2, 3, 4):
    try:
        j = json.load(open(f'_work/evt_offsets_disc{d}.json', encoding='utf-8'))
        disc |= {e['text'] for e in j['entries']}
    except FileNotFoundError:
        pass
bad = 0
for path in sorted(glob.glob('_work/evt_batch*_norm.csv')):
    if path.endswith('_norm_norm.csv'):
        continue
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
