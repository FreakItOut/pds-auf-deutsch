# Probe the string storage format of the remaining-text files:
# are the English strings NUL-terminated plaintext (in-place patchable)?
import csv
import os
import re

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SECT = 2352
DATA = 2048


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


idx1 = fs_index(1)

PROBES = {
    'MENU.SCB': [b'Diary of the Dragon Rider', b'was plenty of food'],
    'MENUEN.FNT': [b'Display Data on Defeated', b'Nanyds inhabit'],
    'TUTORIAL.CGB': [b'About the Oasis', b'The desert is very dangerous'],
    'CHILDMP.MCB': [b'Replenishes HP by', b'Increases laser power'],
    'FLD_A5.MCB': [b'Edge, look down there', b'Why did you save that baby'],
    'FLD_A7.FNT': [b'abilities of your dragon', b'Effects of Type Select'],
    '1ST_READ.PRG': [b'Press', b'Save', b'Item'],
}

for name, probes in PROBES.items():
    lba, size = idx1[name]
    data = read_file('_work/patched_disc1.bin', lba, size)
    print('=== %s (size %d) ===' % (name, size))
    for p in probes:
        off = data.find(p)
        if off < 0:
            print('  probe %r NOT FOUND' % p)
            continue
        lo = max(0, off - 24)
        hi = min(len(data), off + len(p) + 24)
        ctx = data[lo:hi]
        print('  probe %r @0x%X' % (p, off))
        print('    hex  : %s' % ' '.join('%02x' % b for b in ctx))
        print('    ascii: %r' % ctx)
    print()
