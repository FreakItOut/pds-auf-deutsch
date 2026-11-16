# -*- coding: utf-8 -*-
# FMV subtitle polish: index (0-based in evt_de_map order) -> new DE.
import io
import sys

FIX = {
    104: 'Komm zurueck... hier...',
    120: 'Schleift ihn ins Schiff.',
    168: 'Hey! Bleib wach!',
    197: 'Sie hielten sie nicht auf.',
    199: 'Ich hab dir was zu zeigen.',
    204: 'Ich wusste, sie planen Boeses.',
    244: 'Ich will niemanden toeten.',
    250: 'Du bist gewachsen',
    266: 'Ueberlebst du das,',
    285: 'Das war kein Zufall.',
    350: 'Tor auf, Azel!',
    366: 'Sofort verfolgen',
    399: 'Es mit deiner Waffe syncen.',
    440: 'Der Einzige, der uns befreit',
    497: 'Um die Welt zu retten.',
    587: 'Sahst sie?',
    621: 'einbrechen, es nehmen.',
    645: 'Kultur auf ihrer Seite.',
    647: 'verzehrt und zerstoert sie.',
    656: 'Kraft des Turms zu vernichten.',
    659: 'leicht von Maennern machbar.',
    665: 'Experimente warten.',
    677: 'wurden zerfetzt.',
    711: 'liessen Vorzeit in Truemmern.',
    713: 'Menschheit zu retten.',
    725: 'der biologischen Waffen',
    733: 'Ruinen, Tuerme.',
    748: 'die Waechter von Uru!!',
    752: 'schlafende Ruinen.',
    774: 'die Monster zu hassen.',
    777: 'ins Grenzland zu reisen...',
    787: 'das wir kurz nach unserm Treffen?',
    801: 'solche Macht...',
    803: 'bringt dich nur um.',
}


def load():
    lines = [l.rstrip('\r\n') for l in io.open('_work/evt_de_map.csv',
                                               encoding='latin1')]
    return [l for l in lines if l and not l.startswith('#') and ';' in l]


def main():
    rows = load()
    bad = 0
    for idx, de in sorted(FIX.items()):
        if idx >= len(rows):
            print('MISSING index %d' % idx)
            bad += 1
            continue
        en = rows[idx].split(';', 1)[0]
        if len(de) > len(en):
            print('LEN idx=%d de=%d en=%d DE=%r EN=%r'
                  % (idx, len(de), len(en), de, en))
            bad += 1
    print('rows=%d checked=%d bad=%d' % (len(rows), len(FIX), bad))


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='latin1')
    main()
