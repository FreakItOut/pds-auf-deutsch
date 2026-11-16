# Two rows have BOTH firstOff AND secondOff - disc holds different de at each.
# Set csv entries to be disc-authoritative for BOTH offsets.
import csv
import io
import sys
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


d = 1
idx = fs_index(d)
for fname, stem in (('TWN_CAMP.PRG', 'TWN_CAMP_PRG'),
                    ('TWN_RUIN.PRG', 'TWN_RUIN_PRG')):
    if fname not in idx:
        continue
    lba, size = idx[fname]
    data = read_file('_work/patched_disc%d.bin' % d, lba, size)
    path = '_work/subtitles/%s_de.csv' % stem
    lines = io.open(path, encoding='latin1').read().split('\n')
    out = []
    n = 0
    for line in lines:
        q = line.rstrip('\r\n').split(';')
        if len(q) >= 6 and q[0].isdigit() and q[3] and '|' in q[3]:
            off_list = [int(x) for x in q[3].split('|') if x]
            en_b = q[4].encode('latin1')
            disc_s = []
            for o in off_list:
                if o >= len(data):
                    continue
                e = data.find(b'\x00', o)
                if e < 0 or e > o + 120:
                    e = o + 40
                disc_s.append(data[o:e].decode('latin1', 'replace'))
            # if all disc_s share a value, use it
            if disc_s and len(set(disc_s)) == 1 and q[5] != disc_s[0]:
                q[5] = disc_s[0]
                n += 1
                line = ';'.join(q)
        out.append(line)
    with io.open(path, 'w', encoding='latin1', newline='\n') as f:
        f.write('\n'.join(out) + '\n')
    print(stem, n, 'rows synced from disc multi-off')
