# restore chain slots from verified b3 values to roll back v2/v3
import sys
import csv
sys.stdout.reconfigure(encoding='latin1')
SECT, DATA = 2352, 2048

B3 = {
    ('TWN_CAMP_PRG', 100): 'Ich hoerte: Ein Drache',
    ('TWN_CAMP_PRG', 101): 'kaempft gegen das',
    ('TWN_CAMP_PRG', 184): 'Habt ihr seltene Dinge,',
    ('TWN_CAMP_PRG', 185): 'zeigt sie mir.',
    ('TWN_E022_PRG', 35): 'Ehe Craymen mich weckte',
    ('TWN_E022_PRG', 36): 'sah ich Orte mit Atolm.',
    ('TWN_RUIN_PRG', 390): 'Denkst wir standen Chancen',
    ('TWN_RUIN_PRG', 391): 'gegen die Macht',
    ('TWN_RUIN_PRG', 456): 'Alle zu loeschen,',
    ('TWN_RUIN_PRG', 457): 'braucht Jahrhunderte.',
    ('TWN_RUIN_PRG', 467): 'Alte Aufzeichnungen nennen',
    ('TWN_RUIN_PRG', 468): 'eine Gruppe astraler Pfade',
    ('TWN_RUIN_PRG', 526): 'Als Nebeneffekt',
    ('TWN_RUIN_PRG', 527): 'menschliche Emotionen.',
    ('TWN_RUIN_PRG', 625): 'Krieg ist unumgaenglich,',
    ('TWN_RUIN_PRG', 626): 'wird der Ort verschont.',
    ('TWN_RUIN_PRG', 661): 'In einer Zeit ohne Ruinen,',
    ('TWN_SEEK_PRG', 529): 'Im Liberalen Bezirk wohnen',
    ('TWN_SEEK_PRG', 530): 'Reisende.',
    ('TWN_SEEK_PRG', 595): 'Denkst du, weil wir nie',
    ('TWN_SEEK_PRG', 596): 'etwas Gutes fanden',
    ('TWN_SEEK_PRG', 1043): 'Bezirk, also beschlossen sie',
    ('TWN_SEEK_PRG', 1044): 'zu bleiben',
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
    ('TWN_SEEK_PRG', 1137): 'Bis dahin arbeite ich',
    ('TWN_SEEK_PRG', 1138): 'weiter hin.',
    ('TWN_SEEK_PRG', 1173): 'Das ist das Mindeste,',
    ('TWN_SEEK_PRG', 1174): 'als Dank.',
    ('TWN_SEEK_PRG', 1181): 'Nun, ich jage, seit ich',
    ('TWN_SEEK_PRG', 1182): 'ein Kind war.',
    ('TWN_SEEK_PRG', 1187): 'Waffe nutzen',
    ('TWN_SEEK_PRG', 1188): 'wart bis es frisst',
    ('TWN_SEEK_PRG', 1189): 'finde die Schwaeche.',
    ('TWN_SEEK_PRG', 1191): 'kreise einmal um sie',
    ('TWN_SEEK_PRG', 1192): 'lasse sie los.',
    ('TWN_SEEK_PRG', 1193): 'Toete Queen.',
    ('TWN_SEEK_PRG', 1195): 'dodges lasers',
    ('TWN_SEEK_PRG', 1196): 'Saeurspray!',
    ('TWN_SEEK_PRG', 1197): 'sie erholen sich',
    # new ones (intentional-b3 additions since b3 round)
    ('TWN_CAMP_PRG', 108): 'Er wirkt beschaeftigt,',
    ('TWN_CAMP_PRG', 109): 'erschlaegt Monster.)',
    ('TWN_CAMP_PRG', 215): 'werdet ihr weggerissen',
    ('TWN_CAMP_PRG', 216): 'vom Gravitationssturm.',
    ('TWN_CAMP_PRG', 296): 'waere er hilflos...',     # original was 'keine'
    ('TWN_SEEK_PRG', 998): 'echter Mann.',
    ('TWN_CAMP_PRG', 475): 'Wenn sie Nahrung nehmen,',
    ('TWN_CAMP_PRG', 476): 'verhungern wir voellig.',
    ('TWN_CAMP_PRG', 477): '',                          # (third block none)
    ('TWN_CAMP_PRG', 499): 'Wenn die Zeit kommt,',
    ('TWN_CAMP_PRG', 500): 'gruendest du',
    ('TWN_CAMP_PRG', 501): 'eine eigene Familie.',
    ('TWN_CAMP_PRG', 535): 'Keine Sorge. Eines Tages,',
    ('TWN_CAMP_PRG', 536): 'finden wir',
    ('TWN_CAMP_PRG', 537): 'ein Zuhause fuer uns.',
    ('TWN_CAMP_PRG', 649): 'Ich zeige selten Gefuehle,',
    ('TWN_CAMP_PRG', 650): 'aber der Junge war mir wer.',
    ('TWN_CAMP_PRG', 657): 'Kurz nach Rueckkehr,',
    ('TWN_CAMP_PRG', 658): 'starb sein Sohn.',
    ('TWN_CAMP_PRG', 660): 'Sie zerstoerten Zoah',
    ('TWN_CAMP_PRG', 661): 'und meine Heimat.',
    ('TWN_CAMP_PRG', 685): 'Wenn Anjou nicht zurueck,',
    ('TWN_CAMP_PRG', 686): 'haben wir ein Problem.',
    ('TWN_CAMP_PRG', 707): 'Ein Dreckjob,',
    ('TWN_CAMP_PRG', 708): 'der sich auszahlt.',
    ('TWN_CAMP_PRG', 752): 'Wenn du das Dorf Verato',
    ('TWN_CAMP_PRG', 753): 'findest, gib ihnen das.',
    ('TWN_CAMP_PRG', 483): 'Der Wald: ein knapper Ort.',
    ('TWN_CAMP_PRG', 484): 'Er wird geschuetzt',
    ('TWN_CAMP_PRG', 485): 'durch die Goetter-Kraft.',
    ('TWN_CAMP_PRG', 486): 'Von einer grossen Stadt',
    ('TWN_CAMP_PRG', 487): 'gehoerte ich.',
    ('TWN_CAMP_PRG', 435): 'Er ist nicht heilbar,',
    ('TWN_CAMP_PRG', 436): 'ausser mit Spezialgegenmittel.',
    ('TWN_E022_PRG', 435): 'Er ist nicht heilbar,',
    ('TWN_E022_PRG', 436): 'ausser mit Spezialgegenmittel.',
    ('TWN_E022_PRG', 397): 'Hier bin.',
    ('TWN_CAMP_PRG', 397): 'Hier bin.',
    ('TWN_CAMP_PRG', 491): 'wenn du gehst.',
    ('TWN_CAMP_PRG', 397): 'Aussenwelt.',
    ('TWN_CAMP_PRG', 658): 'starb sein Sohn.',
    ('TWN_CAMP_PRG', 491): 'wenn du gehst.',
    ('TWN_CAMP_PRG', 657): 'Kurz nach Rueckkehr,',
    ('TWN_CAMP_PRG', 658): 'starb sein Sohn.',
    ('TWN_CAMP_PRG', 397): 'Aussenwelt',
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


# dedup
clean = {}
for (s, u), v in B3.items():
    clean[(s, u)] = v
by_stem = {}
for (s, u), v in clean.items():
    by_stem.setdefault(s, {})[u] = v

writes, errs = 0, []
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
        for u, de in by_stem[stem].items():
            ea = rmap.get(u)
            if not ea:
                errs.append('csv miss uid %d' % u)
                continue
            offs = [int(x) for x in ea[3].split('|') if x] or [int(ea[2])]
            o1 = offs[0]
            en_b = ea[4].encode('latin1')
            de_b = de.encode('latin1')
            if len(de_b) > len(en_b):
                errs.append('%s uid %d %d>%d %r' % (stem, u,
                            len(de_b), len(en_b), ea[4]))
                continue
            end = min(o1 + len(en_b), len(data))
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
# sync CSV
for stem, umap in by_stem.items():
    p = '_work/subtitles/%s_de.csv' % stem
    lines = open(p, encoding='latin1').read().split('\n')
    out = []
    for line in lines:
        q = line.rstrip('\r\n').split(';')
        if len(q) >= 6 and q[0].isdigit() and int(q[0]) in umap:
            de = umap[int(q[0])]
            if q[5] != de:
                q[5] = de
                line = ';'.join(q)
        out.append(line)
    open(p, 'w', encoding='latin1', newline='\n').write('\n'.join(out))
print('csv synced')
