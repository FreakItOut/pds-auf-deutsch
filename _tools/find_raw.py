# -*- coding: utf-8 -*-
# Sucht einen Text in patched_disc1.bin und zeigt die Rohbytes davor/danach.
import sys

sys.stdout.reconfigure(encoding='latin1')
needle = sys.argv[1]
with open('_work/patched_disc1.bin', 'rb') as f:
    data = f.read()
pos = 0
count = 0
while True:
    p = data.find(needle.encode('latin1'), pos)
    if p < 0:
        break
    print('hit at %#x' % p)
    print(repr(data[p - 16:p + 120]))
    count += 1
    if count >= 3:
        break
    pos = p + 1
print('hits', count)
