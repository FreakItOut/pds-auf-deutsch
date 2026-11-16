# precise fix for the 40 remaining mismatched rows (make csv match disc exactly)
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


for d in (1, 2, 3, 4):
    fs = ('_work/fs_records_all.csv' if d == 1
          else '_work/fs_records_cd%d.csv' % d)
    idx = fs_index(d)
    fixes = []
    for stem in ('TWN_CAMP_PRG',):
        fname = stem.replace('_PRG', '.PRG')
        if fname not in idx:
            continue
        lba, size = idx[fname]
        data = read_file('_work/patched_disc%d.bin' % d, lba, size)
        path = '_work/subtitles/%s_de.csv' % stem
        lines = open(path, encoding='latin1').read().split('\n')
        out = []
        n = 0
        for line in lines:
            q = line.rstrip('\r\n').split(';')
            if len(q) >= 6 and q[0].isdigit():
                cand = (q[3] if len(q) > 3 else '').split('|') + \\
                    ([q[2]] if len(q) > 2 and q[2].isdigit() else [])
                cand = [int(x) for x in cand if x.isdigit()]
                en_b = q[4].encode('latin1')
                disc_b = None
                for o in cand:
                    if o >= len(data):
                        continue
                    ptr = data[o:o + len(en_b)]
                    if ptr == en_b:
                        disc_b = data[o:o]
                        break
                # disc de read via probing from o
                for o in cand:
                    if o >= len(data):
                        continue
                    e = data.find(b'\x00', o)
                    if e < 0 or e > o + 80:
                        e = o + 40
                    disc_de = data[o:e].decode('latin1', 'replace')
                    break
                else:
                    disc_de = None
                if disc_de is None:
                    out.append(line)
                    continue
                if q[5] != disc_de:
                    q[5] = disc_de
                    n += 1
                    line = ';'.join(q)
            out.append(line)
        # fix removed force=1 rows
        with open(path, 'w', encoding='latin1', newline='\n') as f:
            f.write('\n'.join(out) + '\n')
        print('disc', d, 'CAMP csv synced %d rows' % n)
