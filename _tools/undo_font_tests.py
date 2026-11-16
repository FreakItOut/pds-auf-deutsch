# -*- coding: utf-8 -*-
"""Entfernt die temporaeren Font-Test-Patches aus Disc 1."""
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


def write(lba, data, path):
    with open(path, 'r+b') as f:
        for k in range((len(data) + DATA - 1) // DATA):
            f.seek((lba + k) * SECT + 16)
            f.write(data[k * DATA:(k + 1) * DATA])


p = '_work/patched_disc1.bin'

# COMMON.DAT: zwei Kopien von "WEITER" zurueck
d = bytearray(open(p, 'rb').read())
for o, extra in ((0x746a8, 1), (0x7e6b0, 3)):
    pass
d[0x746a8 + 3] = ord('T')
d[0x7e6b0 + 4] = ord('T')
open(p, 'wb').write(bytes(d))
print('COMMON.DAT:', bytes(d[0x746a8:0x746ae]),
      bytes(d[0x7e6b0:0x7e6ba]))

# FLD_C2.PRG: "WEI{ER" -> "WEITER"
iso = ISO9660Reader(p)
rec = [f for f in iso.list_files() if f['name'].upper() == 'FLD_C2.PRG'][0]
fd = bytearray(read(rec['lba'], rec['size'], p))
i = fd.find(b'WEI{ER')
print('FLD_C2.PRG hit', hex(i))
if i >= 0:
    fd[i + 3] = ord('T')
    write(rec['lba'], bytes(fd), p)
    print('FLD_C2.PRG jetzt:', bytes(fd[i:i + 8]))
else:
    print('kein Test-Patch gefunden')
