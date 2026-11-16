# Check cross-disc identity of the remaining-text files and whether their
# strings are NUL-terminated plaintext (patchable in place like TWN/BTL).
import csv
import hashlib
import os

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SECT = 2352
DATA = 2048

FILES = ['MENU.SCB', 'MENUEN.FNT', 'TUTORIAL.CGB', 'CHILDMP.MCB',
         'FLD_A5.MCB', 'FLD_A7.FNT', 'MENU.FNT', 'ITEM.FNT', 'SAVE.FNT',
         'SHOP.FNT', 'WORLDMAP.FNT', 'MENUBK.FNT', '1ST_READ.PRG']


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


idxs = {d: fs_index(d) for d in (1, 2, 3, 4)}

for name in FILES:
    hashes = {}
    for d in (1, 2, 3, 4):
        if name not in idxs[d]:
            hashes[d] = None
            continue
        lba, size = idxs[d][name]
        data = read_file(f'_work/patched_disc{d}.bin', lba, size)
        hashes[d] = hashlib.md5(data).hexdigest()
    vals = set(h for h in hashes.values() if h)
    print('%-14s sizes=%s identical=%s' % (
        name,
        {d: (idxs[d][name][1] if name in idxs[d] else None) for d in (1, 2, 3, 4)},
        len(vals) == 1 and len(vals) > 0))
