# context dump for RUIN block 370-380 (CSV + disc actual)
import csv

SECT, DATA = 2352, 2048

def fs_index(disc):
    fs = ('_work/fs_records_all.csv' if disc == 1 else '_work/fs_records_cd%d.csv' % disc)
    return {r['name']: (int(r['lba']), int(r['size']))
            for r in csv.DictReader(open(fs, encoding='latin1'), delimiter=';') if int(r['lba']) > 0}

def read_file(binp, lba, size):
    out = bytearray()
    need, s = size, lba
    with open(binp, 'rb') as f:
        while need > 0:
            f.seek(s * SECT + 16)
            c = f.read(min(DATA, need))
            out += c
            need -= len(c)
            s += 1
    return bytes(out[:size])

rows = []
with open('_work/subtitles/TWN_RUIN_PRG_de.csv', encoding='latin1') as f:
    for line in f:
        p = line.rstrip('\r\n').split(';')
        if len(p) >= 6:
            rows.append(p)

idx = fs_index(2)
lba, size = idx['TWN_RUIN.PRG']
data = read_file('_work/patched_disc2.bin', lba, size)

def actual(o):
    end = o
    while end < len(data) and data[end] not in (0x00, 0xFF):
        end += 1
    return data[o:end].decode('latin1')

for p in rows:
    uid = int(p[0])
    if 370 <= uid <= 380:
        o = int(p[2])
        print('%d len=%2d EN=%r' % (uid, len(p[4]), p[4]))
        print('      csv=%r  disc=%r' % (p[5], actual(o)))
