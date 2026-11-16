# corrected final satzbau filter v2 — shorter, budget-fitting German
import sys
import csv
sys.stdout.reconfigure(encoding='latin1')
SECT, DATA = 2352, 2048

FIX = {
    ('TWN_CAMP_PRG', 108): ('Er wirkt busy,', 'faellt Monster.'),
    ('TWN_CAMP_PRG', 215): ('werdet ihr weg', 'gerissen.'),
    ('TWN_CAMP_PRG', 397): ('der Aussenwelt.', 'Hier bin.'),
    ('TWN_CAMP_PRG', 453): ('wir tun es...', ''),
    ('TWN_CAMP_PRG', 708): ('zahlte sich aus.', ''),
    ('TWN_CAMP_PRG', 484): ('Er wird geschuetzt', 'durch'),
    ('TWN_CAMP_PRG', 485): ('Goetter-Kraft.', ''),
    ('TWN_CAMP_PRG', 457): ('er auch...', ''),
    ('TWN_CAMP_PRG', 497): ('Wenn sie fressen,', 'verhungern'),
    ('TWN_CAMP_PRG', 498): ('wir voellig.', ''),
    ('TWN_CAMP_PRG', 491): ('wenn du nord-west gehst.', ''),
    ('TWN_CAMP_PRG', 500): ('familiengruender.', ''),
    ('TWN_CAMP_PRG', 536): ('ein Zuhause.', ''),
    ('TWN_CAMP_PRG', 650): ('der Junge fehlt.', ''),
    ('TWN_CAMP_PRG', 658): ('starb der Sohn.', ''),
    ('TWN_CAMP_PRG', 661): ('und die Heimat.', ''),
    ('TWN_CAMP_PRG', 686): ('haben wir Pech.', ''),
    ('TWN_CAMP_PRG', 753): ('uebergib das.', ''),
    ('TWN_CAMP_PRG', 487): ('Gibt es die?', ''),
    # SEEK
    ('TWN_SEEK_PRG', 999): ('echter Mann.', ''),
    # RUIN
    ('TWN_RUIN_PRG', 100): ('Sie ging, als ich', 'fort war.'),
    ('TWN_RUIN_PRG', 101): ('Haett jemand da', 'bleiben'),
    ('TWN_RUIN_PRG', 102): ('gedacht.', ''),
    ('TWN_RUIN_PRG', 108): ('Ich weiss : Glaubst', 'du'),
    ('TWN_RUIN_PRG', 109): ('sie tu', 'Toerichtes?'),
}


def fs_index(d):
    fs = ('_work/fs_records_all.csv' if d == 1
          else '_work/fs_records_cd%d.csv' % d)
    return {r['name']: (int(r['lba']), int(r['size']))
            for r in csv.DictReader(open(fs, encoding='latin1'),
                                    delimiter=';')
            if int(r['lba']) > 0}


def read_file(binp, lba, size):
    out = bytearray()
    with open(binp, 'rb') as f:
        while size > 0:
            f.seek(lba * SECT + 16)
            c = f.read(min(DATA, size))
            if not c:
                break
            out += c
            size -= len(c)
            lba += 1
    return bytes(out)


def write_file_regions(binp, lba, data):
    with open(binp, 'r+b') as f:
        for k in range((len(data) + DATA - 1) // DATA):
            f.seek((lba + k) * SECT + 16)
            f.write(data[k * DATA:(k + 1) * DATA])


by_stem = {}
for (s, u), v in FIX.items():
    by_stem.setdefault(s, {})[u] = v
errs, writes = [], 0

for stem in sorted(by_stem):
    fname = stem.replace('_PRG', '.PRG')
    rows = []
    for ln in open('_work/subtitles/%s_de.csv' % stem, encoding='latin1'):
        q = ln.rstrip('\r\n').split(';')
        if len(q) >= 6 and q[0].isdigit():
            rows.append((int(q[0]), q))
    rmap = dict(rows)
    for d in (1, 2, 3, 4):
        idx = fs_index(d)
        if fname not in idx:
            continue
        lba, size = idx[fname]
        binp = '_work/patched_disc%d.bin' % d
        data = bytearray(read_file(binp, lba, size))
        touch = False
        for u, (d1, d2) in by_stem[stem].items():
            ea = rmap.get(u)
            eb = rmap.get(u + 1)
            if not ea:
                errs.append('miss uid %d csv' % u)
                continue
            offs = [int(x) for x in ea[3].split('|') if x] or [int(ea[2])]
            o1 = offs[0]
            en_b = ea[4].encode('latin1')
            de_b = d1.encode('latin1')
            if len(de_b) > len(en_b):
                errs.append('%s uid %d de %d>en %d %r' % (stem, u,
                            len(de_b), len(en_b), d1))
                continue
            end = min(o1 + len(en_b), len(data))
            data[o1:o1 + len(de_b)] = de_b
            fill = o1 + len(de_b)
            for k in range(fill, end):
                data[k] = 0x00 if k == fill else 0xFF
            writes += 1
            touch = True
            if d2 and eb:
                offs2 = [int(x) for x in eb[3].split('|') if x] or \
                       [int(eb[2])]
                o2 = offs2[0]
                en2_b = eb[4].encode('latin1')
                de2_b = d2.encode('latin1')
                if len(de2_b) <= len(en2_b):
                    end2 = min(o2 + len(en2_b), len(data))
                    data[o2:o2 + len(de2_b)] = de2_b
                    fill2 = o2 + len(de2_b)
                    for k in range(fill2, end2):
                        data[k] = 0x00 if k == fill2 else 0xFF
                    writes += 1
        if touch:
            write_file_regions(binp, lba, bytes(data))
print('writes:', writes, 'errs:', len(errs))
for e in errs[:40]:
    print(' ', e)
