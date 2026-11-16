# -*- coding: utf-8 -*-
# E128 (Disc 3, TWN_E128.PRG) polish pass 3: abbreviations / grammar.
import io
import sys

FIX = {
    166: '(Haengematte abgenommen.)',
    167: '(Schmutzige Haengematte.',
    182: '(Ein grosser Stoffsack.)',
    212: '(Ein Regal voller Geschirr...)',
    214: '(Ein kleiner Ofen...',
    254: '(Der Sockel fuer die Waffe.)',
    259: '(Getraenke in Toepfen leuchten.)',
    309: '(Ein Teil eines Monsters.)',
    313: '(Uralte Maschine.)',
    335: 'Anmachholz des Waechterfeuers.',
    336: 'Kein Ort fuer Fremde.)',
    343: '(Viele Toepferwaren.)',
    347: '(Ein Altar.)',
    360: 'Scheint tagsueber auszusein.)',
    363: '(Raeucherwerk.)',
    365: '(Aus den Fluegeln eines Monsters.)',
    370: 'Vertrau der Aussenwelt...',
    386: '(Ein grosser Ofen.)',
    405: 'Wirkt zerbrechlich.)',
    408: '(Ein uraltes Geraet.',
    411: 'Laeuft sie die ganze Zeit?)',
    413: '(In gutem Zustand...',
    415: '(Mit schmutzigem Tuch bedeckt.)',
    419: '(Voller Buecher.)',
    423: '(Viele Technikbuecher...)',
    425: '(Ein Draht fuer Motor.)',
    429: '(Das Geraet ist kaputt.',
    437: 'Kaputtes Geraet, etwas Saft.)',
    444: '(Ein grosser Korb.)',
    450: '(Reiseartikel, aber',
    454: '(Persoenliche Sachen, aber da',
}


def validate():
    rows = {}
    for ln in io.open('_work/subtitles/TWN_E128_cd3_de.csv', encoding='latin1'):
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
        if any(ord(c) > 127 for c in de):
            print('NONASCII uid=%d DE=%r' % (uid, de))
            bad += 1
    print('checked=%d bad=%d' % (len(FIX), bad))
    return bad


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='latin1')
    sys.exit(1 if validate() else 0)
