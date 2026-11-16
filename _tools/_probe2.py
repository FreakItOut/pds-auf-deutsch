# probe: raw bytes around CAMP uid37 offset + context rows; RUIN uid99/365/483 context
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

idx = fs_index(1)

def probe1(fn, o, back=40, fwd=90):
    lba, size = idx[fn]
    data = read_file('_work/patched_disc1.bin', lba, size)
    lo = max(0, o - back)
    raw = data[lo:o + fwd]
    # split on 0x00/0xFF keeping positions
    print('CSS off=%d' % o)
    s = lo
    txt = []
    while s < len(data) and s < o + fwd:
        e = s
        while e < len(data) and data[e] not in (0x00, 0xFF):
            e += 1
        txt.append((s, data[s:e].decode('latin1'), data[e:e+1].decode('latin1', 'replace')))
        s = e + 1
        while s < o + fwd and data[s] in (0x00, 0xFF):
            s += 1
    for a, b, c in txt:
        mark = ' <<<' if a <= o < a + max(1, len(b)) else ''
        print('   %6d %r%s' % (a, b, mark))

probe1('TWN_CAMP.PRG', 15898)

rows = []
for fn in ('_work/subtitles/TWN_RUIN_PRG_de.csv', '_work/subtitles/TWN_CAMP_PRG_de.csv'):
    for line in open(fn, encoding='latin1'):
        p = line.rstrip('\r\n').split(';')
        if len(p) >= 6:
            rows.append(('RUIN' if 'RUIN' in fn else 'CAMP', int(p[0]), p))

for tag in ('RUIN',):
    for t, uid, p in rows:
        if t == 'RUIN' and uid in (97, 98, 99, 100, 101, 363, 364, 365, 366, 367, 481, 482, 483, 484):
            print('RUIN %d len=%d offs=%s' % (uid, len(p[4]), p[2] + '|' + p[3]))
            print('     EN=%r' % p[4])
            print('     de=%r' % p[5])
