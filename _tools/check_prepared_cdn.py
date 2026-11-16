# Compare: original disc file vs current patched_discN.bin file vs the
# prepared _work/patched_cdN/<name> file. Status per file:
#   MISSING  - no prepared file
#   SAME-ORIG - prepared file equals the original (nothing translated)
#   DE-DIFF  - prepared differs from original (has German), NOT yet in disc
#   IN-DISC  - disc already equals the prepared file
#   IN-DISC-SAME-ORIG - prepared == original and disc == original
import csv
import hashlib
import os

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SECT = 2352
DATA = 2048

ORIG_BINS = {
    2: 'Original_CD2/Panzer Dragoon Saga (Europe) (Disc 2) (Track 1).bin',
    3: 'Original_CD3/Panzer Dragoon Saga (Europe) (Disc 3) (Track 1).bin',
    4: 'Original_CD4/Panzer Dragoon Saga (Europe) (Disc 4) (Track 1).bin',
}


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
    fs = f'_work/fs_records_cd{disc}.csv'
    idx = {}
    for r in csv.DictReader(open(fs, encoding='latin1'), delimiter=';'):
        if int(r['lba']) > 0 and int(r['size']) > 0:
            idx[r['name']] = (int(r['lba']), int(r['size']))
    return idx


for d in (2, 3, 4):
    idx = fs_index(d)
    prep_dir = f'_work/patched_cd{d}'
    if not os.path.isdir(prep_dir):
        continue
    print('=== disc %d ===' % d)
    stats = {}
    for name in sorted(os.listdir(prep_dir)):
        if name not in idx:
            print('  %-14s NOT IN FS RECORDS!' % name)
            continue
        lba, size = idx[name]
        prep = open(f'{prep_dir}/{name}', 'rb').read()
        orig = read_file(ORIG_BINS[d], lba, size)
        disc = read_file(f'_work/patched_disc{d}.bin', lba, size)
        if len(prep) != size:
            st = 'SIZE-MISMATCH(%d!=%d)' % (len(prep), size)
        elif prep == orig:
            st = 'SAME-ORIG'
        elif prep == disc:
            st = 'IN-DISC'
        elif disc == orig:
            st = 'DE-DIFF-NOT-IN-DISC'
        else:
            st = 'DISC-DIFFERS-BOTH'  # disc patched by today's work
        stats[name] = st
    for n, st in sorted(stats.items()):
        if st != 'SAME-ORIG':
            print('  %-14s %s' % (n, st))
    n_same = sum(1 for s in stats.values() if s == 'SAME-ORIG')
    print('  (%d files SAME-ORIG, %d interesting)'
          % (n_same, len(stats) - n_same))
