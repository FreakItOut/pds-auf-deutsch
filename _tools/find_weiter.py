# -*- coding: utf-8 -*-
import sys

sys.path.insert(0, '_tools')
sys.stdout.reconfigure(encoding='latin1')
from iso9660 import ISO9660Reader

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


path = '_work/patched_disc1.bin'
iso = ISO9660Reader(path)
needle = b'WEITER'
for f in iso.list_files():
    if f['dir'] or f['size'] == 0:
        continue
    d = read(f['lba'], f['size'], path)
    i = 0
    hits = []
    while True:
        i = d.find(needle, i)
        if i < 0:
            break
        hits.append(i)
        i += 1
    if hits:
        print(f['name'], 'lba', f['lba'], [hex(h) for h in hits])
