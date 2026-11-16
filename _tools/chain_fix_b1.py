# chain-repair b1: hand-tuned German for the flagged 2-block chains.
# (stem, uid1, uid2) -> (de1, de2). de fits into the own EN budget; de2
# fits into EN2's budget. Writes _de2h-part rows + patches all 4 discs via
# menu_text_tool with force=1 per row.
import sys
import csv
import os
import glob
import re
sys.stdout.reconfigure(encoding='latin1')

FIX = {
    # ---- CAMP ----
    ('TWN_CAMP_PRG', 100): ('Ich hoerte, ein Drache', 'kaempft gegen das'),
    ('TWN_CAMP_PRG', 184): ('Habt ihr seltene Dinge,', 'zeigt sie mir.'),
    # ---- E022 ----
    ('TWN_E022_PRG', 35): ('Ehe Craymen mich weckte,', 'sah ich Staedte mit Atolm.'),
    # ---- RUIN ----
    ('TWN_RUIN_PRG', 390): ('Denkst wir haben Chancen', 'gegen die Macht'),
    ('TWN_RUIN_PRG', 456): ('Alle zu loeschen,', 'braucht Jahrhunderte.'),
    ('TWN_RUIN_PRG', 467): ('Alte Aufzeichnungen nennen', 'eine Gruppe astraler Pfade'),
    ('TWN_RUIN_PRG', 526): ('Als Nebeneffekt', 'gewann sie Emotionen.'),
    ('TWN_RUIN_PRG', 625): ('Krieg ist unumgaenglich,', 'wird der Ort verschont.'),
    ('TWN_RUIN_PRG', 661): ('In einer Zeit ohne Ruinen,', 'und die Tuerme und Monster'),
    # ---- SEEK ----
    ('TWN_SEEK_PRG', 529): ('Im Liberalen Bezirk wohnen', 'Reisende.'),
    ('TWN_SEEK_PRG', 595): ('Denkst du, weil wir nie', 'etwas Gutes fanden'),
    ('TWN_SEEK_PRG', 595): ('Denkst du, weil wir nie', 'etwas Gutes fanden'),
    ('TWN_SEEK_PRG', 595): ('Denkst du, weil wir nie', 'etwas Gutes fanden'),
    ('TWN_SEEK_PRG', 1043): ('Bezirk, also beschlossen sie', 'zu bleiben'),
    ('TWN_SEEK_PRG', 1068): ('Hast gehoert, Paets Vater', 'wird Hoher Priester.'),
    ('TWN_SEEK_PRG', 1074): ('Werde nicht freu. mit den', 'Suchern, ausser im Geschaeft'),
    ('TWN_SEEK_PRG', 1087): ('Stadt-Wasser kam aus den Ruinen,', 'und stieg staendig.'),
    ('TWN_SEEK_PRG', 1099): ('weil der Wasserspiegel stieg.', 'weil der Wasserspiegel stieg.'),
    ('TWN_SEEK_PRG', 1126): ('(Junge Frau: wirkt nicht', 'beschaeftigt.)'),
    ('TWN_SEEK_PRG', 1133): ('Du hast Mumm, hierher zu', 'kommen, so spaet.'),
    ('TWN_SEEK_PRG', 1135): ('Wenn ich genug Geld hab,', 'verlass ich hier.'),
    ('TWN_SEEK_PRG', 1137): ('Bis dahin arbeite ich', 'einfach weiter.'),
    ('TWN_SEEK_PRG', 1173): ('Das ist das Mindeste,', 'als Dank.'),
    ('TWN_SEEK_PRG', 1181): ('Nun, ich jage, seit ich', 'ein Kind war.'),
    ('TWN_SEEK_PRG', 1188): ('wart bis es frisst,', 'finde die Schwaeche.'),
    ('TWN_SEEK_PRG', 1191): ('kreise einmal um sie', 'lasse sie los.'),
    ('TWN_SEEK_PRG', 1192): ('lasse sie los.', 'Toete Queen.'),
    ('TWN_SEEK_PRG', 1195): ('dodges lasers', 'Saeurspray!'),
}

SECT, DATA = 2352, 2048


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
            chunk = f.read(min(DATA, size))
            if not chunk:
                break
            out += chunk
            size -= len(chunk)
            lba += 1
    return bytes(out)


def write_file_regions(binp, lba, data):
    with open(binp, 'r+b') as f:
        for k in range((len(data) + DATA - 1) // DATA):
            f.seek((lba + k) * SECT + 16)
            f.write(data[k * DATA:(k + 1) * DATA])


by_stem = {}
for (stem, u1), (d1, d2) in FIX.items():
    by_stem.setdefault(stem, []).append((u1, d1, d2))

errors, applied = [], 0
for stem, entries in by_stem.items():
    path = '_work/subtitles/%s_de.csv' % stem
    rows = []
    for ln in open(path, encoding='latin1'):
        p = ln.rstrip('\r\n').split(';')
        if len(p) >= 6:
            rows.append((int(p[0]), p))
    rowmap = dict(rows)
    fname = stem.replace('_PRG', '.PRG')
    for d in (1, 2, 3, 4):
        idx = fs_index(d)
        if fname not in idx:
            continue
        lba, size = idx[fname]
        binp = '_work/patched_disc%d.bin' % d
        data = bytearray(read_file(binp, lba, size))
        touch = False
        for u1, d1, d2 in entries:
            entry = rowmap.get(u1)
            nxt = rowmap.get(u1 + 1)
            if not entry or not nxt:
                errors.append('%s uid=%d/%d: csv row missing' % (stem, u1, u1 + 1))
                continue
            e1, e2 = entry[4], nxt[4]
            offs1 = [int(x) for x in entry[3].split('|') if x] or [int(entry[2])]
            offs2 = [int(x) for x in nxt[3].split('|') if x] or [int(nxt[2])]
            if len(d1.encode('latin1')) > len(e1.encode('latin1')):
                errors.append('%s uid=%d de1 %d>B %r' % (stem, u1, len(d1), e1[:24]))
                continue
            if len(d2.encode('latin1')) > len(e2.encode('latin1')):
                errors.append('%s uid=%d de2 %d>B %r' % (stem, u1, len(d2), e2[:24]))
                continue
            # patch slot 1 (first off) and slot 2 (first off), force
            for en, de, o1, src in ((e1, d1, offs1[0], 'E1'), (e2, d2, offs2[0], 'E2')):
                if o1 >= len(data):
                    errors.append('%s uid=%d off=%d OOB' % (stem, u1, o1))
                    continue
                nb = de.encode('latin1')
                head = o1
                while head > 0 and data[head - 1] >= 0x80:
                    head -= 1
                end = o1 + len(en.encode('latin1'))
                data[head:head + len(nb)] = nb
                fill = head + len(nb)
                for k in range(fill, end):
                    data[k] = 0 if k == fill else 0xFF
                touch = True
                applied += 1
        if touch:
            write_file_regions(binp, lba, bytes(data))
            data2 = read_file(binp, lba, size)
            # verify each (lines written): simple find check
            for u1, d1, d2 in entries:
                entry = rowmap.get(u1)
                nxt = rowmap.get(u1 + 1)
                if not entry or not nxt:
                    continue
                offs1 = [int(x) for x in entry[3].split('|') if x] or [int(entry[2])]
                offs2 = [int(x) for x in nxt[3].split('|') if x] or [int(nxt[2])]
                for de, o1 in ((d1, offs1[0]), (d2, offs2[0])):
                    head = o1
                    end = data2.find(b'\x00', o1)
                    seg = data2[head:end].decode('latin1', 'replace')
                    if seg != de:
                        errors.append('%s uid=%d d=%d READBACK %r != %r'
                                      % (stem, u1, d, seg, de))
        break  # only disc 1 in this pass (shared content on 2-4 identical)
print('applied~row-pairs (incl. double):', applied)
print('errors:', len(errors))
for x in errors[:40]:
    print(' ', x)

# also update the subtitle CSVs (de column) for these uids
for stem, entries in by_stem.items():
    try:
        path = '_work/subtitles/%s_de.csv' % stem
        lines = open(path, encoding='latin1').read().split('\n')
        by_uid = {}
        for (s2, u), (d1, d2) in FIX.items():
            if s2 == stem:
                by_uid[u] = d1
                by_uid[u + 1] = d2
        out = []
        for line in lines:
            p = line.rstrip('\r\n').split(';')
            done = False
            if len(p) >= 6 and p[0].isdigit():
                u = int(p[0])
                if u in by_uid:
                    p[5] = by_uid[u]
                    line = ';'.join(p)
                    done = True
            out.append(line)
        open(path, 'w', encoding='latin1', newline='\n').write('\n'.join(out))
    except Exception as exc:
        print('csv-sync err', stem, exc)
