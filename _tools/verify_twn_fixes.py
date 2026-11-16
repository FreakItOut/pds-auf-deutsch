# Independent verification of the applied TWN fixes:
# for every fix, check on each disc's file whether the NEW text exists and
# whether the OLD (broken) text is still present. Old-present = problem.
import csv
import os

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SECT = 2352
DATA = 2048


def read_file(binpath, lba, size):
    out = bytearray()
    need = size
    s = lba
    with open(binpath, 'rb') as f:
        while need > 0:
            f.seek(s * SECT + 16)
            c = f.read(min(DATA, need))
            if not c:
                break
            out += c
            need -= len(c)
            s += 1
    return bytes(out[:size])


def fs_index(disc):
    fs = ('_work/fs_records_all.csv' if disc == 1
          else f'_work/fs_records_cd{disc}.csv')
    return {r['name']: (int(r['lba']), int(r['size']))
            for r in csv.DictReader(open(fs, encoding='latin1'),
                                    delimiter=';')
            if int(r['lba']) > 0 and int(r['size']) > 0}


fixes = []
with open('_work/review_fixes/TWN_SEEK_small_fixes.csv',
          encoding='latin1') as fh:
    rd = csv.reader(fh, delimiter=';')
    for r in rd:
        if len(r) >= 5 and r[3] and r[3] != r[2] and r[2].strip().lower() != 'de':
            fixes.append((r[0], r[1], r[2], r[3]))

groups = {}
for src, en, old, new in fixes:
    groups.setdefault(src, []).append((old, new))

for src, items in sorted(groups.items()):
    name = src.replace('_PRG_de.csv', '.PRG')
    for d in (1, 2, 3, 4):
        idx = fs_index(d)
        if name not in idx:
            continue
        lba, size = idx[name]
        data = read_file(f'_work/patched_disc{d}.bin', lba, size)
        old_left = new_ok = 0
        for old, new in items:
            ob = old.encode('latin1') + b'\x00'
            nb = new.encode('latin1')
            if data.find(ob) >= 0:
                old_left += 1
            elif data.find(nb) >= 0:
                new_ok += 1
        if old_left or new_ok:
            print('disc %d %-12s fixed_ok=%4d old_still=%3d'
                  % (d, name, new_ok, old_left))
print('verification done')
