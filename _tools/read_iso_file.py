# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='latin1')
SECT, DATA = 2352, 2048


def read(lba, size, path='_work/patched_disc1.bin'):
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


lba = int(sys.argv[1])
size = int(sys.argv[2])
off = int(sys.argv[3], 0)
n = int(sys.argv[4], 0) if len(sys.argv) > 4 else 0x100
d = read(lba, size)
open('_work/review_fixes/extract_%d.bin' % lba, 'wb').write(d)
print('size', size)
for i in range(off, min(len(d), off + n), 16):
    print('%06x' % i, d[i:i + 16].hex(' '))
