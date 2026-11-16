# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='latin1')
data = open('_work/patched_disc1.bin', 'rb').read()
pairs = [('m|glich', 'moeglich'), ('f|r', 'fuer'), ('|ber', 'ueber'),
         ('k|nnen', 'koennen'), ('w|rde', 'wuerde'), ('n|tig', 'noetig'),
         ('sch|n', 'schoen'), ('gr|ss', 'groess'), ('m|ss', 'muess')]
for slot, plain in pairs:
    a = data.count(slot.encode('latin1'))
    b = data.count(plain.encode('latin1'))
    print('%-10r slots=%-5d %-10r plain=%d' % (slot, a, plain, b))
print('total | in image', data.count(b'|'))
