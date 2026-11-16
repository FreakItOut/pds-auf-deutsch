# Compare _work/menu_de/TWN_E128_de.csv DE strings against patched disc 3.
import csv
import sys

sys.stdout.reconfigure(encoding='latin1')
SECT, DATA = 2352, 2048
NAME = 'TWN_E128.PRG'


def fs_index(disc):
    fs = '_work/fs_records_cd%d.csv' % disc
    return {r['name']: (int(r['lba']), int(r['size']))
            for r in csv.DictReader(open(fs, encoding='latin1'),
                                    delimiter=';') if int(r['lba']) > 0}


def read_file(binp, lba, size):
    out = bytearray()
    need, s = size, lba
    with open(binp, 'rb') as f:
        while need > 0:
            f.seek(s * SECT + 16)
            c = f.read(min(DATA, need))
            if not c:
                break
            out += c
            need -= len(c)
            s += 1
    return bytes(out[:size])


def unesc(s):
    return s.replace('\\n', '\n').replace('\\t', '\t')


idx = fs_index(3)
lba, size = idx[NAME]
data = read_file('_work/patched_disc3.bin', lba, size)

rows = list(csv.DictReader(open('_work/menu_de/TWN_E128_de.csv',
                                encoding='latin1'), delimiter=';'))
diff = []
too_long = []
oob = []
for r in rows:
    off = int(r['off'])
    de = unesc(r['de'])
    en = unesc(r['en'])
    de_b = de.encode('latin1')
    en_b = en.encode('latin1')
    if len(de_b) > len(en_b):
        too_long.append((off, len(de_b), len(en_b), de, en))
    if off + len(en_b) + 1 > len(data):
        oob.append(off)
        continue
    have = data[off:off + len(de_b)]
    if have != de_b:
        diff.append((off, de, have.decode('latin1', 'replace')))

print('rows=%d differ=%d too_long=%d oob=%d' % (
    len(rows), len(diff), len(too_long), len(oob)))
for x in too_long[:10]:
    print('  LONG off=%d %d>%d %r vs %r' % x)
for x in diff[:15]:
    print('  DIFF off=%d want=%r have=%r' % x)
