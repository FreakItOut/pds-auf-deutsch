# slack probe (clean rewrite)
import csv
import glob
import io
import os
import sys
sys.stdout.reconfigure(encoding='latin1')
SECT, DATA = 2352, 2048


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


CHECKS = [('TWN_CAMP.PRG', '_work/subtitles/TWN_CAMP_PRG_de.csv'),
          ('TWN_RUIN.PRG', '_work/subtitles/TWN_RUIN_PRG_de.csv'),
          ('TWN_SEEK.PRG', '_work/subtitles/TWN_SEEK_PRG_de.csv'),
          ('TWN_E022.PRG', '_work/subtitles/TWN_E022_PRG_de.csv'),
          ('FLD_A7.FNT', '_work/menu_de/FLD_A7_FNT_de.csv')]
idx = fs_index(1)
for stem, path in CHECKS:
    if stem not in idx:
        continue
    lba, size = idx[stem]
    data = bytearray(read_file('_work/patched_disc1.bin', lba, size))
    if not os.path.exists(path):
        print('=== %s no csv' % stem)
        continue
    rows = []
    for ln in io.open(path, encoding='latin1'):
        q = ln.rstrip('\r\n').split(';')
        if len(q) < 6 or not q[0].isdigit():
            continue
        try:
            o = int(q[2].split('|')[0])
        except Exception:
            continue
        rows.append((o, q[4], q[5]))
    rows.sort()
    slack = 0
    bigs = []
    for k in range(len(rows) - 1):
        off1, en1, de1 = rows[k]
        off2, _, _ = rows[k + 1]
        gap = off2 - off1 - len(en1)
        if gap > 0:
            slack += gap
            if len(bigs) < 8 and gap > 16:
                bigs.append((off1, gap, en1[:30], de1[:30]))
    print('%-16s slots=%4d total-slack=%6d (avg %.1f/slot)'
          % (stem, len(rows), slack, slack / max(1, len(rows))))
    for b in bigs:
        print('   %7d slack %4d  EN=%r  DE=%r' % (b[0], b[1], b[2], b[3]))
