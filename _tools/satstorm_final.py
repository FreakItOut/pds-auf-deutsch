# final satzbau filter: translate a curated broken chain-fix list to disc
# (all 4 discs), using the same budget/verify heuristics as chain_fix_b3.
import sys
import csv
sys.stdout.reconfigure(encoding='latin1')
SECT, DATA = 2352, 2048

FIX = {
    # CAMP: broken chains
    ('TWN_CAMP_PRG', 108): ('Er wirkt beschaeftigt,', 'erschlaegt Monster.)'),
    ('TWN_CAMP_PRG', 128): ('Reise allein, solange du', 'jung bist.'),
    ('TWN_CAMP_PRG', 215): ('werdet ihr weggerissen', 'vom Gravitationssturm.'),
    ('TWN_CAMP_PRG', 296): ('waere er hilflos...', 'Bringt daher Beides.'),
    ('TWN_CAMP_PRG', 397): ('der Aussenwelt.', 'Hier bin ich zurecht.'),
    ('TWN_CAMP_PRG', 452): ('Nicht viel zu fuettern,', 'aber'),
    ('TWN_CAMP_PRG', 453): ('tun wir unser Bestes...', ''),
    ('TWN_CAMP_PRG', 456): ('Muede von der Reise,', 'und'),
    ('TWN_CAMP_PRG', 457): ('er auch wahrscheinlich...', ''),
    ('TWN_CAMP_PRG', 475): ('Wenn sie Nahrung nehmen,', 'verhungern'),
    ('TWN_CAMP_PRG', 476): ('wir voellig.', ''),
    ('TWN_CAMP_PRG', 490): ('Du solltest es schaffen,', 'wenn du ostwaerts gehst.'),
    ('TWN_CAMP_PRG', 499): ('Wenn die Zeit kommt,', 'gruendest du'),
    ('TWN_CAMP_PRG', 500): ('eine eigene Familie.', ''),
    ('TWN_CAMP_PRG', 535): ('Keine Sorge. Eines Tages,', 'finden wir'),
    ('TWN_CAMP_PRG', 536): ('ein Zuhause fuer uns.', ''),
    ('TWN_CAMP_PRG', 649): ('Ich zeige selten Gefuehle,', 'aber'),
    ('TWN_CAMP_PRG', 650): ('der Junge war mir wer.', ''),
    ('TWN_CAMP_PRG', 657): ('Kurz nach Rueckkehr,', 'starb'),
    ('TWN_CAMP_PRG', 658): ('sein Sohn.', ''),
    ('TWN_CAMP_PRG', 660): ('Sie haben Zoah', 'zerstoert'),
    ('TWN_CAMP_PRG', 661): ('und meine Heimat.', ''),
    ('TWN_CAMP_PRG', 685): ('Wenn Anjou nicht zurueck,', 'haben'),
    ('TWN_CAMP_PRG', 686): ('wir ein Problem.', ''),
    ('TWN_CAMP_PRG', 707): ('Ein Dreckjob,', 'der'),
    ('TWN_CAMP_PRG', 708): ('sich ausgezahlt hat.', ''),
    ('TWN_CAMP_PRG', 752): ('Wenn du das Dorf Verato', 'findest,'),
    ('TWN_CAMP_PRG', 753): ('gib ihnen das hier.', ''),
    ('TWN_CAMP_PRG', 483): ('Der Wald: ein knapper', 'Ort.'),
    ('TWN_CAMP_PRG', 484): ('Er wird geschuetzt.', 'durch'),
    ('TWN_CAMP_PRG', 485): ('die Macht der Goetter.', ''),
    ('TWN_CAMP_PRG', 486): ('Von einer grossen Stadt', 'gehoerte ich.'),
    ('TWN_CAMP_PRG', 487): ('Gibt es sie wirklich?', ''),
    ('TWN_CAMP_PRG', 435): ('Er ist nicht heilbar,', 'ausser mit'),
    ('TWN_CAMP_PRG', 436): ('Spezialgegenmittel.', ''),
    # SEEK
    ('TWN_SEEK_PRG', 529): ('Der Liberale Bezirk ist', 'von Reisenden bewohnt.'),
    ('TWN_SEEK_PRG', 997): ('Wenn du es aushalten', 'kannst,'),
    ('TWN_SEEK_PRG', 998): ('bist du ein echter Mann.', ''),
    # RUIN
    ('TWN_RUIN_PRG', 390): ('Denkst wir stehen Chancen', 'gegen die Macht'),
    ('TWN_RUIN_PRG', 500): ('Bringt dein Drache Sestren', 'um, ist die Welt'),
    ('TWN_RUIN_PRG', 501): ('vom Fluch befreit.', ''),
    ('TWN_RUIN_PRG', 100): ('Sie ging, als ich fort war.', ''),
    ('TWN_RUIN_PRG', 101): ('Ich haette jemanden einsetzen', 'muessen, um'),
    ('TWN_RUIN_PRG', 102): ('auf sie aufzupassen.', ''),
    ('TWN_RUIN_PRG', 108): ('Ich weiss. Glaubst du,', ''),
    ('TWN_RUIN_PRG', 109): ('sie tut etwas Toerichtes?', ''),
    # JIRI
    ('TWN_JIRI_PRG', 482): ('Kennst du die Legende?', ''),
    ('TWN_JIRI_PRG', 483): ('Der Wald: ein besonderer Ort.', ''),
    ('TWN_JIRI_PRG', 484): ('Er wird geschuetzt.', 'durch'),
    ('TWN_JIRI_PRG', 485): ('die Macht der Goetter.', ''),
    ('TWN_JIRI_PRG', 486): ('Ich hoerte von einer grossen', ''),
    ('TWN_JIRI_PRG', 487): ('Stadt. Gibt es diese?', ''),
    # CAMP 435/436 (E022 copy)
    ('TWN_E022_PRG', 435): ('Er ist nicht heilbar,', 'ausser'),
    ('TWN_E022_PRG', 436): ('mit Spezialgegenmittel', ''),
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


# drop duplicates
clean = {}
for (s, u), v in FIX.items():
    if u == 102 and s == 'TWN_RUIN_PRG':
        continue  # malformed, chain finishes at 101
    clean[(s, u)] = v
# consolidate: only one entry per key
by_stem = {}
for (s, u), v in clean.items():
    by_stem.setdefault(s, {})[u] = v

errs, writes = [], 0
for stem, umap in by_stem.items():
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
        for u, (d1, d2) in umap.items():
            ea = rmap.get(u)
            eb = rmap.get(u + 1)
            if not ea:
                errs.append('miss uid %d csv' % u)
                continue
            if len(d1) > len(ea[4]):
                errs.append('%s uid %d de %d>en %d %r' %
                            (stem, u, len(d1), len(ea[4]), d1))
                continue
            offs = [int(x) for x in ea[3].split('|') if x] or \
                   [int(ea[2])]
            o1 = offs[0]
            # slot A
            en_b = ea[4].encode('latin1')
            de_b = d1.encode('latin1')
            end = o1 + len(en_b)
            end = min(end, len(data))
            data[o1:o1 + len(de_b)] = de_b
            fill = o1 + len(de_b)
            for k in range(fill, end):
                data[k] = 0x00 if k == fill else 0xFF
            writes += 1
            # slot B (uid+1)
            if d2 and eb:
                offs2 = [int(x) for x in eb[3].split('|') if x] or \
                       [int(eb[2])]
                o2 = offs2[0]
                en2_b = eb[4].encode('latin1')
                de2_b = d2.encode('latin1')
                if len(de2_b) <= len(en2_b):
                    end2 = o2 + len(en2_b)
                    end2 = min(end2, len(data))
                    data[o2:o2 + len(de2_b)] = de2_b
                    fill2 = o2 + len(de2_b)
                    for k in range(fill2, end2):
                        data[k] = 0x00 if k == fill2 else 0xFF
                    writes += 1
        if touch:
            pass
        if writes:
            touch = writes
        if touch:
            write_file_regions(binp, lba, bytes(data))
# sync csv de column
for stem, umap in by_stem.items():
    p = '_work/subtitles/%s_de.csv' % stem
    lines = open(p, encoding='latin1').read().split('\n')
    out = []
    for line in lines:
        q = line.rstrip('\r\n').split(';')
        if len(q) >= 6 and q[0].isdigit() and int(q[0]) in umap:
            d1, d2 = umap[int(q[0])]
            if int(q[0]) in umap:
                q[5] = d1
                line = ';'.join(q)
        if len(q) >= 6 and q[0].isdigit() and int(q[0]) - 1 in umap and int(q[0]) != 1:
            d2 = umap[int(q[0]) - 1][1]
            if d2:
                q[5] = d2
                line = ';'.join(q)
        out.append(line)
    open(p, 'w', encoding='latin1', newline='\n').write('\n'.join(out))
print('writes:', writes, 'errs:', len(errs))
for e in errs[:40]:
    print(' ', e)
