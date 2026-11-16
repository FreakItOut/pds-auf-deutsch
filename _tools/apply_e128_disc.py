# Force-write TWN_E128 DE rows that differ from the disc image.
# usage: python apply_e128_disc.py [dry|apply]
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


def write_file_regions(binp, lba, data):
    with open(binp, 'r+b') as f:
        for k in range((len(data) + DATA - 1) // DATA):
            f.seek((lba + k) * SECT + 16)
            f.write(data[k * DATA:(k + 1) * DATA])


def unesc(s):
    return s.replace('\\n', '\n').replace('\\t', '\t')


def actual(data, o, limit):
    e = o
    while e < limit and data[e] not in (0x00, 0xFF):
        e += 1
    return data[o:e].decode('latin1')


MODE = sys.argv[1] if len(sys.argv) > 1 else 'dry'
DRY = MODE != 'apply'

lba, size = fs_index(3)[NAME]
data = bytearray(read_file('_work/patched_disc3.bin', lba, size))
rows = list(csv.DictReader(open('_work/menu_de/TWN_E128_de.csv',
                                encoding='latin1'), delimiter=';'))
offs = sorted({int(r['off']) for r in rows})

applied = same = fails = 0
for r in rows:
    off = int(r['off'])
    prefix = bytes.fromhex(r['prefix']) if r['prefix'] else b''
    en_b = unesc(r['en']).encode('latin1')
    de_b = unesc(r['de']).encode('latin1')
    new = prefix + de_b
    if len(new) > len(prefix) + len(en_b):
        print('FAIL LEN off=%d %d>%d %r' % (off, len(new), len(prefix) + len(en_b), r['de']))
        fails += 1
        continue
    if off + len(en_b) + 1 > len(data):
        print('FAIL OOB off=%d' % off)
        fails += 1
        continue
    old_actual = actual(data, off + len(prefix), off + len(prefix) + len(en_b) + 1)
    slot = off + max(len(prefix) + len(en_b), len(prefix) + len(old_actual) + 1)
    if bytes(data[off:off + len(new)]) == new and (
            slot >= len(data) or all(b in (0x00, 0xFF) for b in data[off + len(new):slot])):
        same += 1
        continue
    if not DRY:
        data[off:off + len(new)] = new
        for k in range(off + len(new), min(slot, len(data))):
            data[k] = 0x00 if k == off + len(new) else 0xFF
    applied += 1

if not DRY and applied:
    write_file_regions('_work/patched_disc3.bin', lba, bytes(data))

print('mode=%s rows=%d written=%d already_ok=%d fails=%d' % (
    MODE, len(rows), applied, same, fails))
