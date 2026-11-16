# Verify FLD_A5.MCB state on all 4 discs after the repair patch:
# - the force-repaired chunk at 56791 must be NUL-terminated
# - banner frames: leading spaces must be intact
import csv
import os

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SECT = 2352
DATA = 2048


def read_file(d, lba, size):
    out = bytearray()
    need = size
    s = lba
    with open(f'_work/patched_disc{d}.bin', 'rb') as f:
        while need > 0:
            f.seek(s * SECT + 16)
            c = f.read(min(DATA, need))
            if not c:
                break  # EOF guard
            out += c
            need -= len(c)
            s += 1
    return bytes(out[:size])


def fs_index(d):
    fs = ('_work/fs_records_all.csv' if d == 1
          else f'_work/fs_records_cd{d}.csv')
    return {r['name']: (int(r['lba']), int(r['size']))
            for r in csv.DictReader(open(fs, encoding='latin1'),
                                    delimiter=';')
            if int(r['lba']) > 0 and int(r['size']) > 0}


for d in (1, 2, 3, 4):
    idx = fs_index(d)
    if 'FLD_A5.MCB' not in idx:
        print('disc %d: FLD_A5.MCB not present' % d)
        continue
    lba, size = idx['FLD_A5.MCB']
    data = read_file(d, lba, size)
    print('disc %d off 56791: %r' % (d, data[56791:56812]))
    with open('_work/menu_de/FLD_A5_MCB_en.csv', encoding='latin1') as fh:
        rd = csv.reader(fh, delimiter=';')
        next(rd)
        for r in rd:
            t = r[4].strip()
            if t in ('Rolling Start', 'o for the %c1Record%c0!!') \
                    and r[4].startswith(' '):
                off = int(r[1])
                print('   banner off=%-6d %r' % (off, data[off:off + 44]))
    print()
