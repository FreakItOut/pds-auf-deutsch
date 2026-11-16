# STABILIZE: write all TWN subtitles rows so csv matches disc bytes exactly.
# This locks coverage at a well-defined state - then we can inspect broken
# chains cleanly without disc/csv drift.
import sys
import csv
sys.stdout.reconfigure(encoding='latin1')
SECT, DATA = 2352, 2048


def fs_index(d):
    fs = ('_work/fs_records_all.csv' if d == 1
          else '_work/fs_records_cd%d.csv' % d)
    return {r['name']: (int(r['lba']), int(r['size']))
            for r in csv.DictReader(open(fs, encoding='latin1'),
                                    delimiter=';')
            if int(r['lba']) > 0}


def read_file(binp, lba, size):
    out = bytearray()
    with open(binp, 'rb') as f:
        while size > 0:
            f.seek(lba * SECT + 16)
            c = f.read(min(DATA, size))
            if not c:
                break
            out += c
            size -= len(c)
            lba += 1
    return bytes(out)


stems = ('TWN_E022_PRG', 'TWN_JIRI_PRG', 'TWN_CAMP_PRG', 'TWN_RUIN_PRG',
         'TWN_SEEK_PRG')
for stem in stems:
    fname = stem.replace('_PRG', '.PRG')
    path = '_work/subtitles/%s_de.csv' % stem
    lines = open(path, encoding='latin1').read().split('\n')
    disc_de = {}
    total_rows = 0
    d = 1
    idx = fs_index(d)
    if fname not in idx:
        print('skip', stem)
        continue
    lba, size = idx[fname]
    data = read_file('_work/patched_disc%d.bin' % d, lba, size)
    fixed = 0
    out = []
    for line in lines:
        q = line.rstrip('\r\n').split(';')
        if len(q) >= 6 and q[0].isdigit():
            o = int(q[2].split('|')[0]) if q[2] and q[2][0].isdigit() else None
            if o is None or o >= len(data):
                out.append(line)
                continue
            e = data.find(b'\x00', o)
            if e < 0 or e > o + 200:
                e = o + 60
            de_disc = data[o:e].decode('latin1', 'replace')
            total_rows += 1
            if q[5] != de_disc:
                q[5] = de_disc
                fixed += 1
                line = ';'.join(q)
        out.append(line)
    with open(path, 'w', encoding='latin1', newline='\n') as f:
        f.write('\n'.join(out) + '\n')
    print('csv-sync %s: %d/%d rows updated to match disc'
          % (stem, fixed, total_rows))

# verify
print()
