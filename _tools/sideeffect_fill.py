# patch remaining copies of the side-effect chain at their exact slots
import sys
import csv
sys.stdout.reconfigure(encoding='latin1')
SECT, DATA = 2352, 2048


def fs_index(d):
    fs = ('_work/fs_records_all.csv' if d == 1
          else '_work/fs_records_cd%d.csv' % d)
    return {r['name']: (int(r['lba']), int(r['size']))
            for r in csv.DictReader(open(fs, encoding='latin1'), delimiter=';')
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


TARGET = [
    (89563, 'Als Nebeneffekt', 21),
    (89581, 'gewann sie Emotionen.', 21),
]
for d in (1, 2, 3, 4):
    idx = fs_index(d)
    lba, size = idx['TWN_RUIN.PRG']
    binp = '_work/patched_disc%d.bin' % d
    data = bytearray(read_file(binp, lba, size))
    for off, de, budget in TARGET:
        en_b = data[off:off + budget]
        de_b = de.encode('latin1')
        end = off + budget
        data[off:off + len(de_b)] = de_b
        fill = off + len(de_b)
        for k in range(fill, end):
            data[k] = 0x00 if k == fill else 0xFF
    write_file_regions(binp, lba, bytes(data))
print('patched')
