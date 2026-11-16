# refine: write both RUIN 527 copies with correct Chinese and sync csv
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


def write_file_regions(binp, lba, data):
    with open(binp, 'r+b') as f:
        for k in range((len(data) + DATA - 1) // DATA):
            f.seek((lba + k) * SECT + 16)
            f.write(data[k * DATA:(k + 1) * DATA])


de = b'menschliche Emotionen.'
for d in (1, 2, 3, 4):
    idx = fs_index(d)
    lba, size = idx['TWN_RUIN.PRG']
    data = bytearray(read_file('_work/patched_disc%d.bin' % d, lba, size))
    for off in (89581, 89768, 90034, 90234, 90499, 90690):
        end = off + 22  # 'she gained human emotions.'
        data[off:off + len(de)] = de
        fill = off + len(de)
        for k in range(fill, end):
            data[k] = 0x00 if k == fill else 0xFF
    write_file_regions('_work/patched_disc%d.bin' % d, lba, bytes(data))
print('patched')
p = '_work/subtitles/TWN_RUIN_PRG_de.csv'
lines = open(p, encoding='latin1').read().split('\n')
out = []
for line in lines:
    q = line.rstrip('\r\n').split(';')
    if len(q) >= 6 and q[0].isdigit() and int(q[0]) == 527:
        q[5] = de.decode('latin1')
        line = ';'.join(q)
    out.append(line)
open(p, 'w', encoding='latin1', newline='\n').write('\n'.join(out))
