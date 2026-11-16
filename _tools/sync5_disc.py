# precise fix: sync ALL 5 TWN csvs to disc1 exactly (2nd clean attempt)
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


for stem in ('TWN_CAMP_PRG', 'TWN_JIRI_PRG', 'TWN_E022_PRG',
             'TWN_RUIN_PRG', 'TWN_SEEK_PRG'):
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
        # collect candidate offsets as integers
        cands = []
        if len(q) > 3 and q[3]:
            for x in q[3].split('|'):
                if x.isdigit():
                    cands.append(int(x))
        if len(q) > 2 and q[2].isdigit():
            cands.append(int(q[2]))
        # probe each candidate; use the one that hits the en string
        disc_de = None
        for o in cands:
            if o >= len(data):
                continue
            end = data.find(b'\x00', o)
            if end < 0 or end > o + 120:
                end = o + 40
            disc_de = data[o:end].decode('latin1', 'replace')
            break
        if disc_de is None:
            out.append(line)
            continue
        total += 1
        if q[5] != disc_de:
            q[5] = disc_de
            fixed += 1
            line = ';'.join(q)
        out.append(line)
    with open(path, 'w', encoding='latin1', newline='\n') as f:
        f.write('\n'.join(out) + '\n')
    print('%s: %d/%d synced' % (stem, fixed, total))
