# Per-disc extraction for files that DIFFER across discs (CHILDMP.MCB,
# disc-specific TWN/FLD/E files). For each disc: EN from the ORIGINAL disc,
# TODO = patched disc still holds the EN.
# Usage: python extract_menu_strings_perdisc.py <FSNAME>
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


def main(fsname):
    tag = fsname.replace('.', '_')
    allrows = {}
    for d in (1, 2, 3, 4):
        idx = fs_index(d)
        if fsname not in idx:
            print('disc %d: %s not present' % (d, fsname))
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
                continue  # already translated on this disc
            rows.append((off, prefix.hex(), len(text), t))
        allrows[d] = rows
        uniq = len({r[3] for r in rows})
        print('disc %d %-12s todo=%d unique=%d'
              % (d, fsname, len(rows), uniq))
        with open(f'_work/menu_de/{tag}_d{d}_en.csv', 'w',
                  encoding='latin1', newline='') as fh:
            fh.write('file;off;prefix;len;en\n')
            for off, pre, ln, t in rows:
                fh.write('%s;%d;%s;%d;%s\n' % (
                    fsname, off, pre, ln,
                    t.replace('\n', '\\n').replace(';', ',')))
    # union unique EN across discs -> map template
    union = {}
    for d, rows in allrows.items():
        for off, pre, ln, t in rows:
            union.setdefault(t, ln)
    out = f'_work/menu_de/{tag}_map_todo.csv'
    with open(out, 'w', encoding='latin1', newline='') as fh:
        for t, ln in sorted(union.items()):
            fh.write('%s;\n' % t.replace('\n', '\\n').replace(';', ','))
    print('union unique EN: %d -> %s (map template)' % (len(union), out))


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'CHILDMP.MCB')
