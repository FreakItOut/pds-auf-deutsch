# repair3.py - FINAL targeted TWN repair, author-direct German, ALL offsets,
# ALL discs, csv-sync. DRY=1 prints the plan without touching anything.
import csv
import os
import sys

sys.stdout.reconfigure(encoding='latin1')
SECT, DATA = 2352, 2048
STEMS = ('TWN_E022_PRG', 'TWN_JIRI_PRG', 'TWN_CAMP_PRG',
         'TWN_RUIN_PRG', 'TWN_SEEK_PRG')


def fs_index(disc):
    fs = ('_work/fs_records_all.csv' if disc == 1
          else '_work/fs_records_cd%d.csv' % disc)
    return {r['name']: (int(r['lba']), int(r['size']))
            for r in csv.DictReader(open(fs, encoding='latin1'),
                                    delimiter=';') if int(r['lba']) > 0}


def read_file(binp, lba, size):
    out = bytearray()
    need, s = size, lba
    with open(binp, 'rb') as f:
        while need > 0:
            f.seek(s * SECT + 16)
            c = f.read(min(DATA, need))
            if not c:
                break
            out += c
            need -= len(c)
            s += 1
    return bytes(out[:size])


def write_file_regions(binp, lba, data):
    with open(binp, 'r+b') as f:
        for k in range((len(data) + DATA - 1) // DATA):
            f.seek((lba + k) * SECT + 16)
            f.write(data[k * DATA:(k + 1) * DATA])


def actual(data, o):
    e = o
    while e < len(data) and data[e] not in (0x00, 0xFF):
        e += 1
    return data[o:e].decode('latin1')


# ---- authored final German (budget-checked, ASCII) -------------------------
AUTH = {
    'TWN_CAMP_PRG': {
        707: 'Ein Dreckjob,',
        708: 'der zahlte gut.',
        752: 'Wenn du Ueberlebende aus dem',
        753: 'Dorf Verato triffst,',
        754: 'koenntest du es ihnen geben?',
        45: '(Viele Monster haben Panzer.)',
        396: 'Keine Angst mehr vor der',
        397: 'Aussenwelt.',
        497: 'Verstehst du das, oder?',
        498: 'Keine Sorgen.',
        536: 'finden wir ein Zuhause.',
    },
    'TWN_RUIN_PRG': {
        100: 'Sie ging, ich war fort.',
        101: 'Ich haette jemand bei ihr',
        102: 'bleiben.',
        108: 'Ich weiss.',
        109: 'Glaubst du, sie tut Dummes?',
    },
    'TWN_SEEK_PRG': {
        1: 'Heil. Bezirk',
        5: 'Warte bis zur Nacht',
        52: '(Hier liegt ein Buch...',
        53: 'Einzige Person, die eine',
        54: 'Bibel verbrennen waere Paet...',
        487: 'Er folgt nur',
        488: 'dem Hohen Priester.',
        489: 'Warum wuerde er',
        492: 'Gehe zum Heiligen Bezirk,',
        493: 'er hat was zu erzaehlen.',
        997: 'Haeltst dus aus, bist du',
        998: 'ein Mann.',
        999: '(Mund ist taub.)',
        1067: 'Ich hab leuchtende Drinks.',
        1068: 'Hast du gehoert, Paets Vater',
        1069: 'wird Hoher Priester?',
        1126: '(Junge Frau wirkt gerade nicht',
        1127: 'beschaeftigt.)',
        113: '(Ueberall liegt Muell...',
        114: 'einiges teils bedeckt,',
        115: 'aber ein Durcheinander.)',
        596: 'etwas Gutes fanden?',
        701: 'Stadt zu verlassen. Warte',
        702: 'bis die Truppen gehn.',
        723: 'Komm morgen wieder.',
        743: 'eine Pflicht, nicht wahr?',
        769: 'Das Angebot ueberdacht?',
        827: 'Nie dachte ich, dass der Priester',
        828: 'die Regeln beugt.',
        871: 'gegangen, um zu suchen.',
        883: 'erledigt.',
        886: 'Was macht Vaiman?',
        887: 'Er kuendigt den Drachen an.',
        924: 'zustimmen, wenn er es seht.',
        953: 'Nicht stoppen.',
        955: 'Solange sie zahlen, klar.',
        961: '(Das leuchtende Getraenk',
        962: 'schmeckt... grausig.)',
        1044: 'zu bleiben.',
        1048: 'Die Truppen kaufen Getraenke.',
        1073: 'Ich gebe dir Rat, Junge.',
        1074: 'Freunde dich nicht mit den',
        1075: 'Suchern, nur im Geschaeft.',
        1131: 'Vorsichtig.',
        1167: 'Dorf fehlt mir.',
        1257: 'Ich wuenschte, jemand wie du',
        1258: 'waere. Beim Hinterhalt...',
        1347: 'Das Reich koennte kommen.',
        1362: 'Sieht wichtig aus.',
        1366: 'Lieber greift das Reich an?',
        1371: 'Er ekelt mich an.',
        1428: 'Schlachtschiffen draussen?',
        1506: 'Ich bin Quitor.',
        1552: '(Die Zaal-Nuesse.',
        1571: 'Hab was du willst.',
        1624: 'Siffle. Schoen, dich zu treffen.',
        1662: 'Erst geh durch den Durchgang.',
        1663: 'Eine Wand siehst du.',
        1710: 'Kennst ihn?',
        1723: 'Ruinen interessieren dich.',
        1732: 'Und?',
        1745: 'Okay, und nun?',
        1754: 'im Heil. Bezirk.',
        1781: 'Vom Grossvater gehoert.',
        1803: 'Hoer auf. Du schreckst sie!',
        1805: 'Lass sie los! Geh weg!',
        1810: 'Viele Artikel hier.',
        1822: 'Der alte Mann bat mich, seine',
        1823: 'Waffe zu fixen.',
        1870: 'Weshalb hier?',
    },
}

DRY = len(sys.argv) < 2 or sys.argv[1] == 'dry'
import re


def load_rows(stem):
    rows = {}
    order = {}
    with open('_work/subtitles/%s_de.csv' % stem, encoding='latin1') as f:
        n = -1
        for line in f:
            n += 1
            p = line.rstrip('\r\n').split(';')
            if len(p) >= 6 and p[0].isdigit():
                uid = int(p[0])
                rows[uid] = p
                order[uid] = n
    return rows, order


fix_uids = {}
# union of authored uids with all mismatch/len uids reported by verify_full
bau = open('_work/review_fixes/broken_all.txt', encoding='latin1').read()
for m in re.finditer(r"LEN (\S+) uid=(\d+)", bau):
    fix_uids.setdefault(m.group(1), set()).add(int(m.group(2)))
for m in re.finditer(r"MM (\S+) d(\d) uid=(\d+)", bau):
    fix_uids.setdefault(m.group(1), set()).add(int(m.group(3)))
for m in re.finditer(r"TR (\S+) uid=(\d+)", bau):
    fix_uids.setdefault(m.group(1), set()).add(int(m.group(2)))
for stem in STEMS:
    fix_uids.setdefault(stem, set()).update(AUTH.get(stem, {}))

total_write = 0
fails = []
for stem in STEMS:
    rows, order = load_rows(stem)
    name = stem.replace('_PRG', '.PRG')
    uids = sorted(fix_uids.get(stem, ()))
    if not uids:
        continue
    # csv sync FIRST (single branch per uid, no clobber)
    lines = None
    if not DRY:
        with open('_work/subtitles/%s_de.csv' % stem, encoding='latin1') as f:
            lines = f.read().split('\n')
        done = set()
    # per disc
    for d in (1, 2, 3, 4):
        idx = fs_index(d)
        if name not in idx:
            continue
        lba, size = idx[name]
        binp = '_work/patched_disc%d.bin' % d
        data = bytearray(read_file(binp, lba, size))
        touch = False
        for uid in uids:
            if uid not in rows:
                fails.append('%s uid=%d missing row' % (stem, uid))
                continue
            en = rows[uid][4]
            de = rows[uid][5]
            if uid in AUTH.get(stem, {}):
                de = AUTH[stem][uid]
            offs = [int(x) for x in rows[uid][3].split('|') if x]
            if not offs:
                offs = [int(rows[uid][2])]
            de_b = de.encode('latin1')
            en_b = en.encode('latin1')
            if len(de_b) > len(en_b):
                fails.append('%s uid=%d BUDGET %d>%d de=%r en=%r'
                             % (stem, uid, len(de_b), len(en_b), de, en))
                continue
            bad = [c for c in de if ord(c) > 127]
            if bad:
                fails.append('%s uid=%d NONASCII %r' % (stem, uid, de))
                continue
            for o in offs:
                if o + max(len(en_b), 1) > len(data):
                    fails.append('%s uid=%d off=%d OOB' % (stem, uid, o))
                    continue
                old = actual(data, o)
                span = max(len(en_b), len(old))
                if old == de and (len(old) >= len(de_b)):
                    # verify expects exact match: keep terminator structure
                    pass
                end = o + span
                data[o:o + len(de_b)] = de_b
                fill = o + len(de_b)
                for k in range(fill, min(end, len(data))):
                    data[k] = 0x00 if k == fill else 0xFF
                total_write += 1
                touch = True
        if touch:
            if not DRY:
                write_file_regions(binp, lba, bytes(data))
            print('%s d%d: %d slot writes' % (name, d,
                  sum(len([int(x) for x in rows[u][3].split('|') if x] or
                      [int(rows[u][2])]) for u in uids if u in rows)))
    if not DRY:
        for uid in uids:
            if uid not in rows or uid not in AUTH.get(stem, {}):
                continue
            n = order[uid]
            q = lines[n].rstrip('\r\n').split(';')
            if len(q) >= 6 and int(q[0]) == uid:
                q[5] = AUTH[stem][uid]
                lines[n] = ';'.join(q)
        with open('_work/subtitles/%s_de.csv' % stem, 'w',
                  encoding='latin1', newline='') as f:
            f.write('\n'.join(lines))

print('dry=%s total_slots=%d fails=%d' % (DRY, total_write, len(fails)))
for x in fails[:30]:
    print('  FAIL', x)
