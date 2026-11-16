# -*- coding: utf-8 -*-
# TWN_RUIN_PRG second-pass corrections.
import io
import sys

FIX = {
    332: 'Nicht deine Schuld.',
    337: 'Ich will die Ausbildung bald',
    338: 'beenden, um sie zu nutzen.',
    339: 'Wie laeuft die Ausbildung?',
    340: 'Bald vorbei.',
    359: 'Dein Posten ist wichtig.',
}


def main():
    rows = {}
    for ln in io.open('_work/subtitles/TWN_RUIN_PRG_de.csv', encoding='latin1'):
        q = ln.rstrip('\r\n').split(';')
        if len(q) >= 6 and q[0].isdigit():
            rows[int(q[0])] = q
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
