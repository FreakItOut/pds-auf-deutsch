# Extract TODO strings for disc-specific files that only exist (or differ)
# on discs 2-4. Same logic as extract_menu_strings_perdisc.py but for a
# whole list, reporting per file/disc.
import csv
import os
import re
import sys

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SECT = 2352
DATA = 2048

ORIG_BINS = {
    1: 'Original_CD1/Panzer Dragoon Saga (Europe) (Disc 1) (Track 1).bin',
    2: 'Original_CD2/Panzer Dragoon Saga (Europe) (Disc 2) (Track 1).bin',
    3: 'Original_CD3/Panzer Dragoon Saga (Europe) (Disc 3) (Track 1).bin',
    4: 'Original_CD4/Panzer Dragoon Saga (Europe) (Disc 4) (Track 1).bin',
}

sys.path.insert(0, '_tools')
from extract_menu_strings import (ASCII_OK, FILENAME_RE, ascii_tail,  # noqa
                                  is_english, split_chunks)


def read_file(binpath, lba, size):
    with open(binpath, 'rb') as fh:
        out = bytearray()
        need = size
        s = lba
        while need > 0:
            fh.seek(s * SECT + 16)
            chunk = fh.read(min(DATA, need))
            if len(chunk) < min(DATA, need):
                break
            out += chunk
            need -= len(chunk)
            s += 1
    return bytes(out[:size])


def fs_index(disc):
    fs = ('_work/fs_records_all.csv' if disc == 1
          else f'_work/fs_records_cd{disc}.csv')
    idx = {}
    for r in csv.DictReader(open(fs, encoding='latin1'), delimiter=';'):
        if int(r['lba']) > 0 and int(r['size']) > 0:
            idx[r['name']] = (int(r['lba']), int(r['size']))
    return idx


# interesting per-disc leftovers from the english_remaining scans
FILES = [
    (2, 'TWN_E059.PRG'), (2, 'E034.EPK'), (2, 'BTL_T0.FNT'),
    (2, 'BTL_C2.FNT'), (2, 'BTL_C52.FNT'), (2, 'BTL_X0.FNT'),
    (2, 'BTL_B5.FNT'), (2, 'SNB.MCB'),
    (3, 'TWN_E128.PRG'), (3, 'E074.EPK'), (3, 'E078.EPK'),
    (3, 'BTL_T0.FNT'), (3, 'BTL_C52.FNT'),
    (4, 'TWN_SEEK.PRG'), (4, 'TWN_CARA.PRG'), (4, 'BTL_T0.FNT'),
    (4, 'BTL_C52.FNT'), (4, 'BTL_C2.FNT'),
]

for d, fsname in FILES:
    idx = fs_index(d)
    if fsname not in idx:
        print('disc %d %-12s NOT PRESENT' % (d, fsname))
        continue
    lba, size = idx[fsname]
    orig = read_file(ORIG_BINS[d], lba, size)
    patch = read_file(f'_work/patched_disc{d}.bin', lba, size)
    rows = []
    for off, chunk in split_chunks(orig):
        if len(chunk) < 3 or len(chunk) > 400:
            continue
        prefix, text = ascii_tail(chunk)
        if len(text) < 3 or not ASCII_OK.match(text):
            continue
        if not re.search(rb'[A-Za-z]{2}', text):
            continue
        t = text.decode('ascii')
        if FILENAME_RE.match(t.strip()):
            continue
        if re.search(r'(MODE|DISP|DEBUG|CAM |BTL DATA| map[0-9]|x[0-9])', t):
            continue
        if not is_english(t):
            continue
        if patch[off:off + len(chunk)] != chunk:
            continue
        rows.append((off, prefix.hex(), len(text), t))
    uniq = sorted({r[3] for r in rows})
    tag = fsname.replace('.', '_')
    out = f'_work/menu_de/{tag}_d{d}_en.csv'
    with open(out, 'w', encoding='latin1', newline='') as fh:
        fh.write('file;off;prefix;len;en\n')
        for off, pre, ln, t in rows:
            fh.write('%s;%d;%s;%d;%s\n' % (
                fsname, off, pre, ln, t.replace('\n', '\\n').replace(';', ',')))
    tmpl = f'_work/menu_de/{tag}_d{d}_map_todo.csv'
    with open(tmpl, 'w', encoding='latin1', newline='') as fh:
        for t in uniq:
            fh.write('%s;\n' % t.replace('\n', '\\n').replace(';', ','))
    print('disc %d %-12s todo=%d unique=%d -> %s' % (d, fsname, len(rows),
                                                     len(uniq), tmpl))
