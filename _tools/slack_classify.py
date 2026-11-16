# check whether the slack region between two slots is filler
# classification: all-0x00 / all-0xFF / mixed-content (dangerous)
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
          ('TWN_E022.PRG', '_work/subtitles/TWN_E022_PRG_de.csv')]
idx = fs_index(1)
SAFE_SLOTS = 0
UNSAFE_SLOTS = 0
SAFE_BYTES = 0
UNSAFE_BYTES = 0
for stem, path in CHECKS:
    if stem not in idx:
        continue
    lba, size = idx[stem]
    data = bytearray(read_file('_work/patched_disc1.bin', lba, size))
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
    per = {'safe': 0, 'unsafe': 0, 'slack_safe': 0, 'slack_unsafe': 0}
    for k in range(len(rows) - 1):
        off1, en1, de1 = rows[k]
        off2, en2, de2 = rows[k + 1]
        gap = off2 - off1 - len(en1)
        if gap <= 8:
            continue
        # ignore the trailing EN-stamp area (from off1+len(en1) to off2)
        region = data[off1 + len(en1):off2]
        all_00 = region.count(0) == len(region)
        all_FF = region.count(0xFF) == len(region)
        filler = region.count(0) + region.count(0xFF) == len(region)
        if all_00 or all_FF:
            per['safe'] += 1
            per['slack_safe'] += gap
            SAFE_SLOTS += 1
            SAFE_BYTES += gap
        elif filler:
            per['safe'] += 1
            per['slack_safe'] += gap
            SAFE_SLOTS += 1
            SAFE_BYTES += gap
        else:
            per['unsafe'] += 1
            per['slack_unsafe'] += gap
            UNSAFE_SLOTS += 1
            UNSAFE_BYTES += gap
    print('%-16s safe-slots=%5d  slack=%7d  unsafe-slots=%5d  slack=%7d'
          % (stem, per['safe'], per['slack_safe'], per['unsafe'],
             per['slack_unsafe']))
print('--- over all files ---')
print('SAFE  slots=%d  slack=%d bytes' % (SAFE_SLOTS, SAFE_BYTES))
print('UNSAFE slots=%d  slack=%d bytes' % (UNSAFE_SLOTS, UNSAFE_BYTES))
