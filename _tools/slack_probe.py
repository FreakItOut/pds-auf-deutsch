# probe slack bytes between adjacent TWN slots and find MOVIE.DAT/fld slack,
# to quantify "can we expand German strings beyond the EN budget?"
# Reports per file: slots (off, EN-start, EN-end, next-slot-start, slack).
import csv
import glob
import io
import os
import re
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


for stem in ('TWN_CAMP.PRG', 'TWN_RUIN.PRG', 'TWN_SEEK.PRG',
             'TWN_E022.PRG', 'TWN_JIRI.PRG', 'FLD_A7.FNT',
             'BTL_A5.FNT'):  # representative files
    if stem not in fs_index(1):
        continue
    lba, size = fs_index(1)[stem]
    data = bytearray(read_file('_work/patched_disc1.bin', lba, size))
    path = ('_work/subtitles/%s_de.csv' % stem.replace('.', '_PRG' if stem.endswith('PRG') else ''))
    path = rip = None
    if '.PRG' in stem:
        path = '_work/subtitles/%s_de.csv' % stem.replace('.', '_PRG' if False else '_PRG')
    else:
        matches = glob.glob('_work/menu_de/%s_de.csv' % stem.replace('.', '_'))
        path = matches[0] if matches else None
    if not path or not os.path.exists(path):
        print('=== %s  skipped (no csv)' % stem)
        continue
    rows = []
    for ln in io.open(path, encoding='latin1'):
        q = ln.rstrip('\r\n').split(';')
        if len(q) < 6 or not q[0].isdigit():
            continue
        rows.append((int(q[2].split('|')[0]), en := q[4], de := q[5]))
    rows.sort()
    slack = 0
    exceed = 0
    for k in range(len(rows) - 1):
        off1, en1, de1 = rows[k]
        off2, en2, de2 = rows[k + 1]
        en_len = len(en1)
        gap = off2 - off1 - en_len   # bytes available beyond EN before next slot
        if gap > 0:
            slack += gap
    print('%-16s slots %4d   free bytes between EN and next slot (slack):'
          % (stem, len(rows)))
    print('                  %d bytes, avg %.1f/slot'
          % (slack, slack / max(1, len(rows))))
    # per-row big-slack preview
    bigs = [(off1, en1[:28], de1[:28], off2 - off1) for k in
            range(len(rows) - 1) for r in [(rows[k])] for o0, en1, de1 in r
            for off2 in [rows[k+1][0]]][0][:0]
    # only show the first 8 slack>0 rows
    n = 0
    for k in range(len(rows) - 1):
        off1, en1, de1 = rows[k]
        off2, en2, de2 = rows[k+1]
        gap = off2 - off1 - len(en1)
        if n < 8 and gap > 8:
            n += 1
            print('    %7d gap %4d  EN=%-30r  DE=%r' % (off1, gap, en1, de1))
