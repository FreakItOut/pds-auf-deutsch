# patch BTL_A5 hint + E014 EV subtitle to German on all 4 discs
import sys
import csv
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


def write_file_regions(binp, lba, data):
    with open(binp, 'r+b') as f:
        for k in range((len(data) + DATA - 1) // DATA):
            f.seek((lba + k) * SECT + 16)
            f.write(data[k * DATA:(k + 1) * DATA])


JOBS = [
    ('BTL_A5.FNT', 'Watch out for the ones with horns.', 'Achte auf die mit Hoernern.'),
    ('E014.EPK', 'This must be the one...', 'Das muss es sein...'),
]
for fname, en_t, de_t in JOBS:
    en_b = en_t.encode('latin1')
    de_b = de_t.encode('latin1')
    if len(de_b) > len(en_b):
        print('skip too long', fname)
        continue
    for d in (1, 2, 3, 4):
        fs = ('_work/fs_records_all.csv' if d == 1
              else '_work/fs_records_cd%d.csv' % d)
        idx = {r['name']: (int(r['lba']), int(r['size']))
               for r in csv.DictReader(open(fs, encoding='latin1'),
                                       delimiter=';')
               if int(r['lba']) > 0}
        if fname not in idx:
            continue
        lba, size = idx[fname]
        data = bytearray(read_file('_work/patched_disc%d.bin' % d, lba, size))
        i = data.find(en_b)
        print(fname, 'disc', d, 'off', i)
        if i < 0:
            continue
        end = i + len(en_b)
        data[i:i + len(de_b)] = de_b
        fill = i + len(de_b)
        for k in range(fill, end):
            data[k] = 0x00 if k == fill else 0xFF
        write_file_regions('_work/patched_disc%d.bin' % d, lba, bytes(data))
print('done')
