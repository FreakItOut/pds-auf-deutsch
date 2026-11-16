# -*- coding: utf-8 -*-
# Third polish pass: broken grammar / dropped meaning in TWN CAMP/RUIN/SEEK.
import io
import sys

STEMS = {
    'TWN_CAMP_PRG': {
        13: '(Bettzeug fuer die lange Reise.)',
        26: '(Kiste verschlossen.)',
        39: '(Zwei gepflegte Gewehre.)',
        63: '(Hier lagert Bettzeug.)',
        308: '(Er fuerchtet mich nicht mehr...)',
        361: 'Sehr gut, mein Sohn... machen wir.',
        483: 'Der Wald: ein besondrer Ort.',
        486: 'Auch von einer grossen Stadt.',
        487: 'Gibt es den Ort wirklich?',
        730: 'Du willst ihn ans Reich',
        731: 'verraten?',
        771: 'Ort steht auf der Karte.',
        778: '(Warum schickt Gash Boten?',
    },
    'TWN_RUIN_PRG': {
        17: '(Diese Buecher wirken echt.',
        55: '(Sieht aus wie Kleidung.)',
        82: 'Darum konnte Gash es nutzen?',
        89: 'Niemand wuerde das kaufen...)',
        135: '(Ladha, die Waechterin...)',
        147: 'Sie fort...',
        198: 'Ich bin Jared, Schmied.',
        206: 'Ich verstehe dich nicht.',
        228: 'Ich bin Bezer, Damons Enkel.',
        232: '...Stadt verliessest!',
        242: 'Haben Sucher dir was erzaehlt?',
        301: 'und gehe mit ihnen.',
        384: 'Wir brachten sie zum Heiler.',
        401: 'Art, uns fuer Rettung zu danken.',
        308: 'fortsetzen, wird mein',
        309: 'Lebenswerk sie besser machen.',
        433: 'Endlich treffen wir...',
        436: 'Ich bin Zadoc, Sammler.',
        446: 'Hat Gash von Tuermen erzaehlt?',
        472: 'Also will Gash Sestren toeten.',
        511: 'Er sollte die Tuerme',
        512: 'zerstoeren. Azel verschwand',
        513: 'im Kampf. Sie geht nach Uru.',
        574: 'Bleiben ist gefaehrlich.',
        602: 'gegen ein Kampfschiff',
        634: 'Ihre Kraefte: Katastrophe.',
        658: 'Ich... weiss nicht.',
        667: 'Achso... Danke.',
        671: "Mir geht's gut. Nur unvorsichtig.",
        676: 'Kein Essen noetig',
        683: 'Dennoch hab ich Kraefte...',
    },
    'TWN_SEEK_PRG': {
        58: '(Riecht nach Obst.)',
        164: '(Lampe auf dem Boden.)',
        414: '(Draht fuer den Motor.',
        425: '(Mehr Geraet?',
        448: '(Der Stoff ist duenn.',
        901: 'Fehler machen...',
        1275: 'hol meine Teile... klar?',
    },
}


def validate(stems):
    bad = 0
    for stem, fixes in stems.items():
        rows = {}
        for ln in io.open('_work/subtitles/%s_de.csv' % stem,
                          encoding='latin1'):
            q = ln.rstrip('\r\n').split(';')
            if len(q) >= 6 and q[0].isdigit():
                rows[int(q[0])] = q
        for uid, de in sorted(fixes.items()):
            if uid not in rows:
                print('MISSING %s uid=%d' % (stem, uid))
                bad += 1
                continue
            en = rows[uid][4]
            if len(de) > len(en):
                print('LEN %s uid=%d de=%d en=%d DE=%r EN=%r'
                      % (stem, uid, len(de), len(en), de, en))
                bad += 1
            if any(ord(c) > 127 for c in de):
                print('NONASCII %s uid=%d DE=%r' % (stem, uid, de))
                bad += 1
    print('checked=%d bad=%d'
          % (sum(len(v) for v in stems.values()), bad))
    return bad


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='latin1')
    sys.exit(1 if validate(STEMS) else 0)
