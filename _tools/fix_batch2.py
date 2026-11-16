# -*- coding: utf-8 -*-
# Batch 2: grammar/meaning fixes.
import io
import sys

STEMS = {
    'TWN_E022_PRG': {
        1: '(Mein Kapitaen!!!)',
        4: 'Verlasse Ausgrabung',
        24: 'Gerne wuerde ich sie',
        43: '(Radgams lebloser Koerper',
        44: 'liegt gekruemmt da.',
        45: 'Sein Ruecken ist gebrochen,',
        46: 'das Blut ist entleert.',
        47: '(Er wollte, dass ein',
        48: 'Jaeger es bekommt.)',
    },
    'TWN_JIRI_PRG': {
        0: 'Ruinen, unten',
        15: '(Da ist etwas an dem Wappen.',
    },
    'TWN_SEEK_PRG': {
        735: 'Du wirst als einer der',
        736: 'Auserwaehlten anerkannt.',
        778: 'Im Notfall muss ich dich',
        779: 'um Gehorsam bitten.',
        800: 'Sag dem Mann, der dich rief,',
        801: 'dass Handel mit draussen nur',
        802: 'Aerger bringt.',
        805: 'Sie ist nicht wie die',
        806: 'Kinder draussen.',
        872: 'Es scheint unwahrscheinlich,',
        873: 'dass noch welche kommen.',
        879: 'Vaiman gab dir wohl',
        880: 'den Pass.',
        900: 'Nie wieder denselben',
        901: 'Fehler machen..',
        902: 'Mit der Zeit verblassen',
        903: 'Erinnerungen an dich, sowie',
        904: 'auch die Feinde...',
        923: 'Der Hohe Priester wuerde nicht',
        924: 'zustimmen, wenn er es sieht.',
        927: 'Ich hoerte, der Enkel des',
        928: 'Hohen Priesters kam nie heim.',
        1032: 'Nie glaubte ich an die',
        1033: 'Prophezeiung vom Vater.',
        1057: 'Die Kunden bleiben weg.',
        1058: 'Der Bezirk ist fuer Heilige.',
        1064: 'Nur der Hohe Priester',
        1065: 'sieht es wohl.',
        1068: 'Paets Vater wird der',
        1069: 'neue Priester?',
        1074: 'Freunde dich nicht mit den',
        1075: 'Suchern an, nur im Geschaeft,',
        1076: 'weisst du.',
        1087: 'Stadtwasser kam aus den',
        1088: 'Ruinen und stieg staendig.',
        1097: 'waerst leichte Beute fuer sie.',
        1098: 'Ich hoere, die Tobitamas',
        1099: 'sind zum See zurueck, weil',
        1100: 'der Wasserspiegel stieg.',
        1118: 'Ueber Hohen Priester',
        1126: '(Eine junge Frau... sie wirkt',
        1127: 'recht frei.)',
        1135: 'Wenn ich genug Geld habe,',
        1136: 'verlass ich den Ort.',
        1137: 'Bis dahin arbeit ich',
        1138: 'weiter.',
        1139: 'Am Ende kann nicht mal das',
        1140: 'Reich sie besiegen.',
        1229: 'Die Leute sind sicher, solange sie',
        1230: 'in der Stadt sind',
        1257: 'Ich wuenschte, jemand wie du',
        1258: 'waere beim Hinterhalt.',
        1261: 'Ich will im Kampf sterben, wie',
        1262: 'echte Jaeger tun.',
        1283: 'Denkst du, du kannst mich',
        1284: 'mit Schrott taeuschen!?',
        1307: 'Opa weiss nicht,',
        1308: 'wo ich bin.',
        1340: 'Wirst du mir das wirklich',
        1341: 'geben? Ich lerne ihn.',
        1342: 'Genau deshalb habe ich',
        1343: 'es gebaut.',
        1445: 'Hey, die Waffe... Ist das nicht',
        1446: 'die, die ich reparierte?',
        1458: 'Dich um Ausrottung der',
        1459: 'Truppen zu bitten, bringt ihm',
        1460: 'nur Ansehen beim Rat.',
        1461: 'Indem er den Drachen',
        1462: 'gegen das Reich schickt, wirkt',
        1463: 'er wie ein Fuehrer. Tatsaechlich,',
        1464: 'in Gefahr, wuerde er die Stadt',
        1465: 'sofort verlassen, sicher.',
        1469: 'Reich nicht stoppen. Sie',
        1479: 'Job gesucht?',
        1480: 'Such woanders.',
        1486: 'Kennst du die Geruechte',
        1487: 'dieser Stadt?',
        1496: 'Ich haette nie gedacht,',
        1497: 'dass du Diebesgut verkaufst.',
        1502: 'Sag, warst du nicht',
        1503: 'im Bezirk?',
        1510: 'kannst du fuer dich behalten,',
        1511: 'dass du mich sahst?',
        1514: 'Das ist Essen aus dem',
        1515: 'Wald. Bringt guten Preis.',
        1521: 'Den Hohen Priester so',
        1522: 'beleidigen!',
        1528: 'Wir werden die Kontrolle ueber',
        1529: 'Handel hier kriegen!',
        1546: 'In letzter Zeit haelt der',
        1547: 'Rat mich genau im Auge.',
        1563: 'Du wagst es, eine Anfrage',
        1564: 'von einem Buerger abzulehnen?',
        1579: 'Nicht',
        1580: 'Hast du gehoert? Vaiman sagt,',
        1581: 'dass ein Drache kommt!',
        1583: 'auch wenn das Reich kommt.',
        1586: 'Wie wagst du es, mit einem',
        1587: 'Buerger des Bezirks feilschen!',
        1634: 'Sieh die Segnungen der',
        1635: 'Goetter mit eigenen Augen.',
        1642: 'Es dauert noch lange, bis ich',
        1643: 'ein Buerger des Bezirks bin.',
        1644: 'Der Hohe Priester will',
        1645: 'unsern Lohn kuerzen.',
        1674: 'Geh zum Heiligen Bezirk und du',
        1675: 'wirst ein Lager sehen. Die',
        1676: 'Kirche ist links. Such die zwei',
        1677: 'Saeulen.',
        1822: 'Der Alte bat mich, seine',
        1823: 'Waffe zu richten.',
        1860: 'Wegen einem Relikt reisst das',
        1861: 'Reich ganze Stadt ab.',
        1864: 'vom Rat gehoert',
        1871: 'Du willst wohl was',
        1872: 'Essen holen?',
    },
}


def read_rows(stem):
    rows = {}
    fn = '_work/subtitles/%s_de.csv' % stem
    for ln in io.open(fn, encoding='latin1'):
        q = ln.rstrip('\r\n').split(';')
        if len(q) >= 6 and q[0].isdigit():
            rows[int(q[0])] = q[4]
    return rows


def main():
    bad = 0
    total = 0
    for stem, fixes in STEMS.items():
        en = read_rows(stem)
        for uid, de in fixes.items():
            total += 1
            if uid not in en:
                print('MISSING UID %s %d' % (stem, uid))
                bad += 1
                continue
            if len(de) > len(en[uid]):
                print('LEN %s %d  de=%d en=%d  DE=%r  EN=%r'
                      % (stem, uid, len(de), len(en[uid]), de, en[uid]))
                bad += 1
    print('checked=%d bad=%d' % (total, bad))


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='latin1')
    main()
