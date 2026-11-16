# -*- coding: utf-8 -*-
"""Diff Original-Kernel (Original_CD*/Track 1) vs. gepatchter Kernel (alle Discs)."""
import glob
import sys

sys.path.insert(0, '_tools')
from iso9660 import ISO9660Reader

sys.stdout.reconfigure(encoding='latin1')
SECT, DATA = 2352, 2048


def read(lba, size, path):
    out = bytearray()
    need, s = size, lba
    with open(path, 'rb') as f:
        while need > 0:
            f.seek(s * SECT + 16)
            c = f.read(min(DATA, need))
            if not c:
                break
            out += c
            need -= len(c)
            s += 1
    return bytes(out[:size])


def kernel_of(path):
    iso = ISO9660Reader(path)
    rec = [f for f in iso.list_files() if f['name'].upper() == '1ST_READ.PRG'][0]
    return read(rec['lba'], rec['size'], path), rec['lba']


for disc in (1, 2, 3, 4):
    orig = glob.glob('Original_CD%d/*(Track 1).bin' % disc)[0]
    o, _ = kernel_of(orig)
    c, lba = kernel_of('_work/patched_disc%d.bin' % disc)
    diff = [i for i in range(min(len(o), len(c))) if o[i] != c[i]]
    ranges = []
    for i in diff:
        if ranges and i == ranges[-1][1] + 1:
            ranges[-1][1] = i
        else:
            ranges.append([i, i])
    outside = [r for r in ranges if not (0x3D000 <= r[0] and r[1] <= 0x3DA00)]
    print('disc %d: %d diff ranges, ausserhalb Stringfenster: %d' % (
        disc, len(ranges), len(outside)))
    for r in outside[:10]:
        print('   !!! %06x-%06x' % (r[0], r[1]))
