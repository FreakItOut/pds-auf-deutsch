# live-search disc 1 for the string 'controls Edge' / 'controls edge'
import csv
import re
import sys
sys.stdout.reconfigure(encoding='latin1')

SECT, DATA = 2352, 2048


def read_file(bp, lba, size):
    with open(bp, 'rb') as fh:
        out = bytearray()
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
for fname in sorted(idx):
    lba, size = idx[fname]
    if size > 30000000:
        continue
    data = read_file('_work/patched_disc1.bin', lba, size)
    for pat in (b'ontrl', b'ontrrol', b'ontrol'):
        i = 0
        while True:
            i = data.find(pat, i)
            if i < 0:
                break
            # include surrounding bytes
            s = i - 60
            s = max(0, s)
            e = min(i + 100, len(data))
            ctx = data[s:e]
            print('=== %-18s off=%d' % (fname, i))
            print('  ', repr(ctx.decode('latin1', 'replace')))
            i += 1
