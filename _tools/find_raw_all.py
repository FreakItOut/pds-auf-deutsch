# -*- coding: utf-8 -*-
# Sucht einen Text in allen patched_disc<n>.bin und zeigt die Rohbytes.
import sys

sys.stdout.reconfigure(encoding='latin1')
needle = sys.argv[1].encode('latin1')
for d in (1, 2, 3, 4):
    with open('_work/patched_disc%d.bin' % d, 'rb') as f:
        data = f.read()
    pos = 0
    count = 0
    while True:
        p = data.find(needle, pos)
        if p < 0:
            break
        print('disc %d hit at %#x' % (d, p))
        print('  ', repr(data[max(0, p - 24):p + 140]))
        count += 1
        if count >= 2:
            break
        pos = p + 1
    if count:
        print('disc %d: %d hit(s)' % (d, count))
