# patch remaining TWN_RUIN uid0 second copy at off 16815 on all discs
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
            chunk = fh.read(min(DATA, need))
            if len(chunk) < min(DATA, need):
                break
            out += chunk
            need -= len(chunk)
            s += 1
    return bytes(out[:size])


def write_file_regions(binp, lba, data):
    with open(binp, 'r+b') as f:
        for k in range((len(data) + DATA - 1) // DATA):
            f.seek((lba + k) * SECT + 16)
            f.write(data[k * DATA:(k + 1) * DATA])


en_b = b"Seekers' Stronghold"
de_b = b'Sucher-Festung'
for d in (1, 2, 3, 4):
    fs = ('_work/fs_records_all.csv' if d == 1
          else '_work/fs_records_cd%d.csv' % d)
    idx = {r['name']: (int(r['lba']), int(r['size']))
           for r in csv.DictReader(open(fs, encoding='latin1'), delimiter=';')
           if int(r['lba']) > 0}
    data = bytearray(read_file('_work/patched_disc%d.bin' % d,
                               *idx['TWN_RUIN.PRG']))
    o = 16815
    end = o + len(en_b)
    data[o:o + len(de_b)] = de_b
    fill = o + len(de_b)
    for k in range(fill, end):
        data[k] = 0x00 if k == fill else 0xFF
    write_file_regions('_work/patched_disc%d.bin' % d, idx['TWN_RUIN.PRG'][0],
                       bytes(data))
print('patched 16815 all discs')
