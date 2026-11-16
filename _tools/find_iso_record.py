# -*- coding: utf-8 -*-
import sys

sys.path.insert(0, '_tools')
from iso9660 import ISO9660Reader

sys.stdout.reconfigure(encoding='latin1')
iso = ISO9660Reader('_work/patched_disc1.bin')
root = iso._root
pending = [root]
seen = set()
while pending:
    lba, size = pending.pop(0)
    if (lba, size) in seen:
        continue
    seen.add((lba, size))
    data = iso.read_bytes(lba, size)
    pos = 0
    while pos + 34 <= len(data):
        ln = data[pos]
        if ln == 0:
            pos += 2048 - (pos % 2048)
            continue
        rec = data[pos:pos + ln]
        import struct
        ext = struct.unpack('<I', rec[2:6])[0]
        dsz = struct.unpack('<I', rec[10:14])[0]
        flags = rec[25]
        nlen = rec[32]
        name = rec[33:33 + nlen].decode('latin1', 'ignore').split(';')[0]
        if name not in ('\x00', '\x01'):
            if flags & 0x02:
                pending.append((ext, dsz))
            elif name.upper() in ('MERUKABA.MCB', 'MOVIE.DAT', 'MENU.SCB',
                                  'CHILDMP.MCB', 'FLD_A5.MCB', 'FLD_A7.FNT',
                                  'FLD_C4_6.MCB', 'FLD_D2.FNT',
                                  'BTL_A53.FNT', 'MOVIE.PRG', 'TITLE.PRG',
                                  'MENUEN.PRG', 'EVT000_1.FNT', 'EVT000_2.FNT'):
                print(name, 'lba', ext, 'size', dsz)
        pos += ln
