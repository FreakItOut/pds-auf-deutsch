# Find ASCII patterns in a disc image and map them to files via the LBA index.
# usage: python find_disc.py <disc> <pattern> [<pattern> ...]
import csv
import re
import sys

SECT, DATA = 2352, 2048
DISC = int(sys.argv[1])
PATS = [p.encode('latin1') for p in sys.argv[2:]]
BIN = '_work/patched_disc%d.bin' % DISC
FS = ('_work/fs_records_all.csv' if DISC == 1
      else '_work/fs_records_cd%d.csv' % DISC)

recs = []
with open(FS, encoding='latin1') as f:
    for r in csv.DictReader(f, delimiter=';'):
        lba, size = int(r['lba']), int(r['size'])
        if lba > 0 and size > 0:
            recs.append((lba, size, r['name']))
recs.sort()

data = open(BIN, 'rb').read()


def owner(off):
    sec = off // SECT
    if off % SECT < 16:
        return None
    for lba, size, name in recs:
        if lba <= sec < lba + (size + DATA - 1) // DATA:
            return name, (sec - lba) * DATA + (off % SECT - 16)
    return None


for pat in PATS:
    print('=== %r ===' % pat)
    idx = 0
    n = 0
    while True:
        idx = data.find(pat, idx)
        if idx < 0:
            break
        own = owner(idx)
        lo = max(0, idx - 40)
        hi = min(len(data), idx + len(pat) + 60)
        ctx = data[lo:hi]
        ctx = ''.join(chr(b) if 32 <= b < 127 else '.' for b in ctx)
        print('off=%d sec=%d %s' % (idx, idx // SECT, own))
        print('   %s' % ctx)
        idx += 1
        n += 1
        if n >= 40:
            print('   ... more')
            break
    print('matches=%d' % n)
