# trim over-budget chains b2 (safe chains after heal): uid-level rebuild
import sys
import csv
sys.stdout.reconfigure(encoding='latin1')

SECT, DATA = 2352, 2048

DE = {
    # heal residual cut/bad chains  (over-budget-safe values)
    ('TWN_E022_PRG', 35): 'Ehe Craymen mich weckte',
    ('TWN_E022_PRG', 36): 'sah ich Orte mit Atolm.',
    ('TWN_CAMP_PRG', 100): 'Ich hoerte: Ein Drache',
    ('TWN_CAMP_PRG', 101): 'kaempft gegen das',
    ('TWN_SEEK_PRG', 1137): 'Bis dahin arbeite ich',
    ('TWN_SEEK_PRG', 1138): 'weiter hin.',
    ('TWN_SEEK_PRG', 1187): 'warte, bis es frisst',
    ('TWN_SEEK_PRG', 1188): 'wart bis es frisst',
    ('TWN_SEEK_PRG', 1189): 'finde die Schwaeche.',
    ('TWN_RUIN_PRG', 390): 'Denkst wir standen Chancen',
    ('TWN_SEEK_PRG', 529): 'Im Liberalen Bezirk wohnen',
    ('TWN_SEEK_PRG', 530): 'Reisende.',
    ('TWN_SEEK_PRG', 595): 'Denkst du, weil wir nie',
    ('TWN_SEEK_PRG', 596): 'etwas Gutes fanden',
    ('TWN_SEEK_PRG', 1068): 'Hast du gehoert?',
    ('TWN_SEEK_PRG', 1069): 'Paets Vater: Hoher Priest.',
    ('TWN_SEEK_PRG', 1074): 'Werde nicht freu. mit den',
    ('TWN_SEEK_PRG', 1075): 'Suchern, ausser im Schaeft.',
    ('TWN_SEEK_PRG', 1087): 'Stadt-Wasser: kam aus den Ruine',
    ('TWN_SEEK_PRG', 1088): 'und stieg staendig.',
    ('TWN_SEEK_PRG', 1099): 'weil der Wasserspiegel stieg.',
    ('TWN_SEEK_PRG', 1100): 'weil der Wasserspiegel stieg.',
    ('TWN_SEEK_PRG', 1126): '(Junge Frau: wirkt nicht',
    ('TWN_SEEK_PRG', 1127): 'beschaeftigt.)',
    ('TWN_SEEK_PRG', 1133): 'Du hast Mumm, hierher',
    ('TWN_SEEK_PRG', 1134): 'zu kommen, so spaet.',
    ('TWN_SEEK_PRG', 1135): 'Wenn ich genug Geld hab',
    ('TWN_SEEK_PRG', 1136): 'verlass ich hier.',
    ('TWN_SEEK_PRG', 1173): 'Das ist das Mindeste,',
    ('TWN_SEEK_PRG', 1174): 'als Dank.',
    ('TWN_SEEK_PRG', 1181): 'Nun, ich jage, seit ich',
    ('TWN_SEEK_PRG', 1182): 'ein Kind war.',
    ('TWN_SEEK_PRG', 1191): 'kreise einmal um sie',
    ('TWN_SEEK_PRG', 1192): 'lasse sie los.',
    ('TWN_SEEK_PRG', 1193): 'Toete Queen.',
    ('TWN_SEEK_PRG', 1195): 'dodges lasers',
    ('TWN_SEEK_PRG', 1196): 'Saeurspray!',
    ('TWN_SEEK_PRG', 1043): 'Bezirk, also beschlossen sie',
    ('TWN_SEEK_PRG', 1044): 'zu bleiben',
}


def fs_index(d):
    fs = ('_work/fs_records_all.csv' if d == 1
          else '_work/fs_records_cd%d.csv' % d)
    return {r['name']: (int(r['lba']), int(r['size']))
            for r in csv.DictReader(open(fs, encoding='latin1'), delimiter=';')
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
for (s, u), de in DE.items():
    by_stem.setdefault(s, []).append((u, de))
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
        for u, de in by_stem[stem]:
            entry = rmap.get(u)
            offs = [int(x) for x in entry[3].split('|') if x] or [int(entry[2])] if entry else []
            if not entry:
                errs.append('csv missing uid %d' % u)
                continue
            o1 = offs[0]
            en = entry[4]
            en_b = en.encode('latin1')
            de_b = de.encode('latin1')
            if len(de_b) > len(en_b):
                errs.append('%s uid=%d %d>%d %r' % (stem, u, len(de_b), len(en_b), en))
                continue
            end = o1 + len(en_b)
            data[o1:o1 + len(de_b)] = de_b
            fill = o1 + len(de_b)
            for k in range(fill, end):
                data[k] = 0x00 if k == fill else 0xFF
            writes += 1
            touch = True
        if touch:
            write_file_regions(binp, lba, bytes(data))
print('writes:', writes, 'errs:', len(errs))
for x in errs[:30]:
    print(' ', x)
