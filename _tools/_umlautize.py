# TEMP: wandelt GUI-Texte von ae/oe/ue zu echten Umlauten (nur Anzeige).
# entfernt sich nach Lauf selbst?  Nein: hier statisch fuer Nachrechnen.
import io

PATH = r'_tools\pds_deutsch_patcher_gui.py'

PAIRS = [
    # lange Worte zuerst
    ('Uebersetzung', '\u00dcbersetzung'),
    ('uebersprungen', '\u00fcbersprungen'),
    ('Oberflaech', 'Oberfl\u00e4ch'),
    ('ueberschreib', '\u00fcberschreib'),
    ('Groesse', 'Gr\u00f6\u00dfe'),
    ('aendern', '\u00e4ndern'),
    ('Aendern', '\u00c4ndern'),
    ('geaendert', 'ge\u00e4ndert'),
    ('pruef', 'pr\u00fcf'),
    ('Pruef', 'Pr\u00fcf'),
    ('oeffnen', '\u00f6ffnen'),
    ('Oeffnen', '\u00d6ffnen'),
    ('Waehlen', 'W\u00e4hlen'),
    ('gruen', 'gr\u00fcn'),
    ('fuer', 'f\u00fcr'),
    # zweite Welle
    ('waehlen', 'w\u00e4hlen'),
    ('druecken', 'dr\u00fccken'),
    ('Bloecke', 'Bl\u00f6cke'),
    ('gewaehlt', 'gew\u00e4hlt'),
    ('auswaehlen', 'ausw\u00e4hlen'),
    ('benoetig', 'ben\u00f6tig'),
    ('laeuft', 'l\u00e4uft'),
    ('veraendert', 'ver\u00e4ndert'),
    ('unvollstaendig', 'unvollst\u00e4ndig'),
    ('unvolstaendig', 'unvollst\u00e4ndig'),
    ('zurueck', 'zur\u00fcck'),
]

TITLE_OLD = "'Panzer Dragoon Saga - Deutsche Fassung (Fan-Uebersetzung)'"
TITLE_NEW = ("'Panzer Dragoon Saga - Deutsche Fassung "
             "(Fan-\u00dcbersetzung) von FreakItOut'")


def main():
    s = io.open(PATH, encoding='utf-8').read()
    s = s.replace('# -*- coding: ascii -*-',
                  '# -*- coding: utf-8 -*-')
    if TITLE_OLD in s:
        s = s.replace(TITLE_OLD, TITLE_NEW)
    for a, b in PAIRS:
        s = s.replace(a, b)
    io.open(PATH, 'w', encoding='utf-8', newline='').write(s)
    print('umlautize ok')


if __name__ == '__main__':
    main()
