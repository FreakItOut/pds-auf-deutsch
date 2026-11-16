# direct probe of BTL_D5.FNT against disc1 for the phrase 'The one'
import sys
import csv
sys.stdout.reconfigure(encoding='latin1')
SECT, DATA = 2352, 2048


def read_file(bp, lba, size):
    out = bytearray()
    with open(bp, 'rb') as fh:
        need = size
        s = lba
        while need > 0:
            fh.seek(s * SECT + 16)
            c = fh.read(min(DATA, need))
            if len(c) < min(DATA, need):
                break
            out += c
            need -= len(c)
            s += 1
    return bytes(out[:size])


idx = {r['name']: (int(r['lba']), int(r['size']))
       for r in csv.DictReader(open('_work/fs_records_all.csv',
                                    encoding='latin1'), delimiter=';')
       if int(r['lba']) > 0}
lba, size = idx['BTL_D5.FNT']
print('lba', lba, 'size', size)
d = read_file('_work/patched_disc1.bin', lba, size)
for pat in (b'The one', b'The on', b'the one', b'controls Edge',
            b'The  one'):
    i = d.find(pat)
    print(repr(pat), '->', i)
print()
print('bytes [11430..11560] =', repr(d[11430:11560]))
print('bytes [11440..11570] =', repr(d[11440:11570].replace(b'\x00', b'|')))
# check disc2/3/4 for reward
for dn in (2, 3, 4):
    fs = '_work/fs_records_cd%d.csv' % dn
    idx2 = {r['name']: (int(r['lba']), int(r['size']))
            for r in csv.DictReader(open(fs, encoding='latin1'),
                                    delimiter=';')
            if int(r['lba']) > 0}
    if 'BTL_D5.FNT' not in idx2:
        print('disc', dn, 'BTL_D5 absent')
        continue
    d2 = read_file('_work/patched_disc%d.bin' % dn,
                   *idx2['BTL_D5.FNT'])
    print('disc', dn, 'lba', idx2['BTL_D5.FNT'], 'len', len(d2))
    for pat in (b'The one', b'controls Edge', b'there'):
        i2 = d2.find(pat)
        print('   disc', dn, 'pat', pat, '->', i2)
        if i2 >= 0:
            break
