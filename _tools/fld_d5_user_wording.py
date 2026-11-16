# user-revision: FLD_D5 'Wer dich steuert, Edge,' -> 'Derjenige der Edge steuert,'
import sys
import csv
sys.stdout.reconfigure(encoding='latin1')
SECT, DATA = 2352, 2048


def read_file(bp, lba, size):
    with open(bp, 'rb') as fh:
        out = bytearray()
        need = size
        s = lba
        while need > 0:
            fh.seek(s * SECT + 16)
            c = fh.read(min(DATA, need))
            if len(c) < min(DATA, need):
                break
            out += c
            need -= len(c)
            s += 1
    return bytes(out[:size])


def write_file_regions(binp, lba, data):
    with open(binp, 'r+b') as f:
        for k in range((len(data) + DATA - 1) // DATA):
            f.seek((lba + k) * SECT + 16)
            f.write(data[k * DATA:(k + 1) * DATA])


old_variants = [b'Wer dich steuert, Edge,']
new_de = b'Derjenige der Edge steuert,'
print('len new_de =', len(new_de), 'budget 27')

for d in (1, 2, 3, 4):
    fs = ('_work/fs_records_all.csv' if d == 1
          else '_work/fs_records_cd%d.csv' % d)
    idx = {r['name']: (int(r['lba']), int(r['size']))
           for r in csv.DictReader(open(fs, encoding='latin1'), delimiter=';')
           if int(r['lba']) > 0}
    if 'FLD_D5.FNT' not in idx:
        continue
    lba, size = idx['FLD_D5.FNT']
    data = bytearray(read_file('_work/patched_disc%d.bin' % d, lba, size))
    off = None
    for old in old_variants:
        i = data.find(old)
        if i >= 0:
            off = i
            break
    if off is None:
        # also look for empty-region version (old got overlaid)
        i = data.find(b'Derjenige der Edge steuert,')
        if i >= 0:
            print('disc', d, 'already patched')
            continue
        print('disc', d, 'not found, skip')
        continue
    print('disc', d, 'off', off)
    end = off + 27
    data[off:off + len(new_de)] = new_de
    fill = off + len(new_de)
    for k in range(fill, end):
        data[k] = 0x00 if k == fill else 0xFF
    write_file_regions('_work/patched_disc%d.bin' % d, lba, bytes(data))
# verify disc 1
idx = {r['name']: (int(r['lba']), int(r['size']))
       for r in csv.DictReader(open('_work/fs_records_all.csv',
                                    encoding='latin1'), delimiter=';')
       if int(r['lba']) > 0}
d1 = read_file('_work/patched_disc1.bin', *idx['FLD_D5.FNT'])
print('verify disc1 @11456:', repr(bytes(d1[11456:11510]).replace(b'\x00', b'|')))
