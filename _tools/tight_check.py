# ribbon report for the KUERZUNGEN in the CD1 cover area
# detect every remaining German slot where the budget is tight (~<6 chars)
# budget fit, yet the game graphics allow longer German strings because the
# display is actually wide.  We print the candidate slots and the true budget
# from the EN column, so the user can see which ones have room.
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


tight_rows = []
for path in sorted(glob.glob('_work/subtitles/TWN_*_de.csv')):
    base = os.path.basename(path)[:-7]
    if base.startswith('TWN_E128'):
        continue
    f = 1
    for ln in io.open(path, encoding='latin1'):
        q = ln.rstrip('\r\n').split(';')
        if len(q) < 6 or not q[0].isdigit():
            continue
        en, de = q[4], q[5]
        if not en.strip() or not de.strip():
            continue
        if en.strip() == de.strip():
            continue
        # tighten budget check
        tightness = len(de) / max(1, len(en))
        if tightness > 0.93:   # de uses >93 % of EN budget = tight
            tight_rows.append((base, int(q[0]), len(en), len(de),
                               round(tightness * 100), en, de))
print('tight budget rows:', len(tight_rows))
print('%-18s %4s %4s %4s %5s  EN / DE' % ('file', 'uid', 'en', 'de', '%'))
for b, u, le, ld, p, en, de in tight_rows[:60]:
    print('%-18s %4d %4d %4d %4d%%  %r / %r'
          % (b[:18], u, le, ld, p, en[:40], de[:40]))
with open('_work/review_fixes/tight_rows.txt', 'w', encoding='latin1',
          newline='\n') as f:
    for b, u, le, ld, p, en, de in tight_rows:
        f.write('%s uid=%d en=%d de=%d pct=%d%% %r -> %r\n'
                % (b, u, le, ld, p, en, de))
print('written _work/review_fixes/tight_rows.txt')
