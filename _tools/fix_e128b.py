# -*- coding: utf-8 -*-
# E128 second pass: grammar/meaning polish. Validated against EN length.
import io
import sys

FIX = {
    21: 'Da koennten Kreaturen sein.)',
    27: '(Beispiel fuer Zoahs Handwerk.)',
    30: '(Der Boden ist fruchtbar.)',
    40: '(Rauschendes Wasser.)',
    52: '(Holz sehr trocken.)',
    59: '(Verbrenner riecht nach Asche.)',
    62: 'Bibel verbrennen wuerde: Paet)',
    66: '(Riecht nach Obst.)',
    89: '(Es pumpt wohl Wasser',
    90: 'durch diese Rohre dort.)',
    95: '(Nuesse auf den Boden gefallen.)',
    98: '(Einige Nuesse auf dem Boden.)',
    113: 'Hab von Abner gehoert.',
    115: 'Nur zur Lagerung?',
    121: 'Vielleicht ist was Gutes',
    122: 'drin.',
    231: 'Gesegnete Waffe fuer die Jagd?)',
    302: 'Hier werden sie gefuellt.)',
    326: '(Verkauft er die auch?)',
    371: 'Ja, klar.',
    374: 'Er ist nur ein Junge.',
    426: 'Es kommt nicht vom Reich.',
}


def load():
    rows = {}
    for ln in io.open('_work/subtitles/TWN_E128_cd3_de.csv', encoding='latin1'):
        q = ln.rstrip('\r\n').split(';')
        if len(q) >= 6 and q[0].isdigit():
            rows[int(q[0])] = q
    return rows


def main():
    rows = load()
    bad = 0
    for uid, de in sorted(FIX.items()):
        if uid not in rows:
            print('MISSING uid=%d' % uid)
            bad += 1
            continue
        en = rows[uid][4]
        if len(de) > len(en):
            print('LEN uid=%d de=%d en=%d DE=%r EN=%r'
                  % (uid, len(de), len(en), de, en))
            bad += 1
    print('checked=%d bad=%d' % (len(FIX), bad))


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='latin1')
    main()
