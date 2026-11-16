# make csv match the DISC byte-for-byte (stabilize), then demand the user
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


stems = ('TWN_CAMP_PRG', 'TWN_E022_PRG', 'TWN_JIRI_PRG', 'TWN_RUIN_PRG')
csv_disc_reads = {}
for stem in stems:
    fname = stem.replace('_PRG', '.PRG')
    rows = []
    for ln in open('_work/subtitles/%s_de.csv' % stem, encoding='latin1'):
        q = ln.rstrip('\r\n').split(';')
        if len(q) >= 6 and q[0].isdigit():
            rows.append((int(q[0]), q))
    rmap = dict(rows)
    d = 1
    idx = fs_index(d)
    if fname not in idx:
        continue
    lba, size = idx[fname]
    data = read_file('_work/patched_disc%d.bin' % d, lba, size)
    fixed = 0
    out = []
    for i, (u, ea) in enumerate(rmap.items()):
        offs = [int(x) for x in ea[3].split('|') if x] or [int(ea[2])]
        o = offs[0]
        end = data.find(b'\x00', o)
        if end < 0 or end > o + 100:
            end = o + 40
        disc_de = data[o:end].decode('latin1', 'replace')
        new_line = None
        for j, row in enumerate(out):
            if not isinstance(row, str):
                continue
            p = row.rstrip('\r\n').split(';')
            if len(p) >= 6 and p[0].isdigit() and int(p[0]) == u:
                new_line = row  # from scratch per row
                break
    # write back the corrected csv
    with open('_work/subtitles/%s_de.csv' % stem, 'w',
              encoding='latin1', newline='\n') as f:
        f.write('\n'.join(out) + '\n')
    print('disc-1 csv-sync %s: %d rows updated to match disc'
          % (stem, fixed))
