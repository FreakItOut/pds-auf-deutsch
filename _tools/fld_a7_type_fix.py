# patch FLD_A7.FNT 'The Attack Type specific Berserk Technique is Assault
# Wing. This increases die...' remaining 4-disc paragraph into pure German.
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


en_t = ('The Attack Type specific\n'
        'Berserk Technique is\n'
        'Assault Wing.  This increases\n'
        'die Laserleistung deines D')
de_t = ('Die Angriff-Typ-\n'
        'Berserk-Technik ist\n'
        'Angriffsfluegel:\n'
        'erhoeht die Laserkraft.\n')
for d in (1, 2, 3, 4):
    fs = ('_work/fs_records_all.csv' if d == 1
          else '_work/fs_records_cd%d.csv' % d)
    idx = {r['name']: (int(r['lba']), int(r['size']))
           for r in csv.DictReader(open(fs, encoding='latin1'), delimiter=';')
           if int(r['lba']) > 0}
    if 'FLD_A7.FNT' not in idx:
        continue
    lba, size = idx['FLD_A7.FNT']
    data = bytearray(read_file('_work/patched_disc%d.bin' % d, lba, size))
    i = data.find(en_t.encode('latin1'))
    print('disc', d, 'off', i)
    if i < 0:
        continue
    en_b = en_t.encode('latin1')
    de_b = de_t.encode('latin1')
    if len(de_b) > len(en_b):
        print('skip too long', d)
        continue
    end = i + len(en_b)
    data[i:i + len(de_b)] = de_b
    fill = i + len(de_b)
    for k in range(fill, end):
        data[k] = 0x00 if k == fill else 0xFF
    write_file_regions('_work/patched_disc%d.bin' % d, lba, bytes(data))
print('done')
