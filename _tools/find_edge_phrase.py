# precise disc-1 search: look at every BTL/FLD/TWN file for the phrase
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
PATTERNS = [rb'The on', rb'The  one', rb'he one', rb'controls',
            rb'WHo', rb'the one', rb'he controls']
for fname in sorted(idx):
    lba, size = idx[fname]
    if size > 30000000:
        continue
    data = read_file('_work/patched_disc1.bin', lba, size)
    for pat in PATTERNS:
        for m in re.finditer(pat, data):
            p = m.start()
            ctx = data[max(0, p - 60):p + 160]
            print('=== %-15s off=%d pat=%s' % (fname, p, pat.decode()))
            print('  ', repr(ctx.decode('latin1', 'replace')))
