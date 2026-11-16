# -*- coding: utf-8 -*-
import struct
import sys

sys.stdout.reconfigure(encoding='latin1')
d = open('_work/patched_disc1.bin', 'rb').read()
names = [b'EVT000_1.FNT', b'EVT000_2.FNT', b'EVTZOAH.FNT', b'ASCII.CGZ']
for n in names:
    print('===', n.decode())
    pos = 0
    hits = 0
    while True:
        p = d.find(n, pos)
        if p < 0:
            break
        rec = p - 33
        if rec >= 0:
            ext = struct.unpack('<I', d[rec + 2:rec + 6])[0]
            size = struct.unpack('<I', d[rec + 10:rec + 14])[0]
            flags = d[rec + 25]
            nlen = d[rec + 32]
            if ext < 1000000 and size < 100 * 1024 * 1024:
                print('  rec@%#x ext=%d size=%d flags=%d nlen=%d' % (
                    rec, ext, size, flags, nlen))
                hits += 1
        pos = p + 1
        if hits > 10:
            break
    if hits == 0:
        print('  keine Records')
