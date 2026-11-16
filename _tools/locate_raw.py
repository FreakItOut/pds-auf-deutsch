# -*- coding: utf-8 -*-
import csv
import sys

sys.stdout.reconfigure(encoding='latin1')
SECT, DATA = 2352, 2048
raw = 0x24e2e5e4
lba = raw // SECT
off_in_sector = raw % SECT
print('lba', lba, 'sector off', off_in_sector)
recs = list(csv.DictReader(open('_work/fs_records_all.csv',
                                encoding='latin1'), delimiter=';'))
for r in recs:
    if not r['size'].isdigit() or not r['lba'].isdigit():
        continue
    a = int(r['lba'])
    n = int(r['size'])
    sectors = (n + DATA - 1) // DATA
    if a <= lba < a + sectors:
        print('file', r['name'], 'lba', a, 'size', n)
        file_off = (lba - a) * DATA + (off_in_sector - 16)
        print('approx file offset', file_off, hex(file_off))
