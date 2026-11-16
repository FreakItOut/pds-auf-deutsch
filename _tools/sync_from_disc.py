# carefully resync ALL 5 TWN subtitle csvs from disc1 (only the disc authoritative)
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


for stem in ('TWN_CAMP_PRG', 'TWN_RUIN_PRG', 'TWN_JIRI_PRG',
             'TWN_E022_PRG', 'TWN_SEEK_PRG'):
    fname = stem.replace('_PRG', '.PRG')
    path = '_work/subtitles/%s_de.csv' % stem
    lines = open(path, encoding='latin1').read().split('\n')
    d = 1
    idx = fs_index(d)
    if fname not in idx:
        continue
    lba, size = idx[fname]
    data = read_file('_work/patched_disc%d.bin' % d, lba, size)
    fixed = 0
    total = 0
    out = []
    for line in lines:
        q = line.rstrip('\r\n').split(';')
        if len(q) < 6 or not q[0].isdigit():
            out.append(line)
            continue
        o0 = None
        offs_col = q[3] if len(q) > 3 else ''
        for cand in (offs_col.split('|') if offs_col else []) + \
                ([q[2]] if q[2] and q[2][0].isdigit() else []):
            if cand.isdigit():
                o0 = int(cand)
                break
        if o0 is None or o0 >= len(data):
            out.append(line)
            continue
        e = data.find(b'\x00', o0)
        if e < 0 or e > o0 + 200:
            e = o0 + 40
        de_disc = data[o0:e].decode('latin1', 'replace')
        total += 1
        if q[5] != de_disc:
            q[5] = de_disc
            fixed += 1
            line = ';'.join(q)
        out.append(line)
    with open(path, 'w', encoding='latin1', newline='\n') as f:
        f.write('\n'.join(out) + '\n')
    print('%s: %d/%d rows synced from disc' % (stem, fixed, total))
