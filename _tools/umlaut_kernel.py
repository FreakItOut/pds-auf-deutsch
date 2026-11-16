# -*- coding: utf-8 -*-
"""Setzt die Kernel-Menue strings (Gebietsnamen etc.) auf Font-Slots um."""
import re
import sys

sys.path.insert(0, '_tools')
from iso9660 import ISO9660Reader
import umlaut_conv as U

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


def write(lba, data, path):
    with open(path, 'r+b') as f:
        for k in range((len(data) + DATA - 1) // DATA):
            f.seek((lba + k) * SECT + 16)
            f.write(data[k * DATA:(k + 1) * DATA])


for disc in (1, 2, 3, 4):
    binp = '_work/patched_disc%d.bin' % disc
    iso = ISO9660Reader(binp)
    rec = None
    for f in iso.list_files():
        if f['name'].upper() == '1ST_READ.PRG':
            rec = f
            break
    data = bytearray(read(rec['lba'], rec['size'], binp))
    g = data.find(b'Georgius')
    lo = max(0, g - 0x500)
    hi = min(len(data), g + 0x500)
    changed = 0
    for m in re.finditer(rb'[ -~]{3,60}', data[lo:hi]):
        a = lo + m.start()
        b = lo + m.end()
        if b >= len(data) or data[b] != 0:
            continue
        s = m.group().decode('latin1')
        new = U.convert_text(s)
        if new == s:
            continue
        nb = new.encode('latin1')
        if len(nb) > len(m.group()):
            continue
        data[a:a + len(nb)] = nb
        fill = a + len(nb)
        for k in range(fill, b):
            data[k] = 0x00 if k == fill else 0xFF
        changed += 1
    write(rec['lba'], bytes(data), binp)
    print('d%d: %d Strings umlautisiert' % (disc, changed))
