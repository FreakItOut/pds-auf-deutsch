# CGZ-Decompressor mit VDP2-Adresswrap (19 Bit), Rest 0.
import csv
import sys

sys.stdout.reconfigure(encoding='latin1')
SECT, DATA = 2352, 2048


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


def fs_index(disc):
    fs = ('_work/fs_records_all.csv' if disc == 1
          else '_work/fs_records_cd%d.csv' % disc)
    return {r['name']: (int(r['lba']), int(r['size']))
            for r in csv.DictReader(open(fs, encoding='latin1'),
                                    delimiter=';') if int(r['lba']) > 0}


lba, size = fs_index(1)['ASCII.CGZ']
src = read_file('_work/patched_disc1.bin', lba, size)
d = bytearray()
p = 0
r6 = src[p]
p += 1
r7 = 9
VRAM = 0x80000


def byte_at(idx):
    if idx < 0:
        return 0
    return d[idx] if idx < len(d) else 0


while True:
    if r7 == 1:
        r6 = src[p]
        p += 1
        r7 = 8
    r7 -= 1
    bit = r6 & 1
    r6 >>= 1
    if bit:
        d.append(src[p])
        p += 1
        continue
    if r7 == 1:
        r6 = src[p]
        p += 1
        r7 = 8
    r7 -= 1
    bit2 = r6 & 1
    r6 >>= 1
    if bit2:
        r0 = src[p]
        r1 = src[p + 1]
        p += 2
        comp = (r1 << 8) | r0
        if comp == 0:
            print('END at', len(d), 'p', p)
            break
        if comp & 0x8000:
            comp -= 0x10000
        off = comp >> 3
        n = r0 & 7
        if n:
            n += 2
        else:
            n = src[p] + 1
            p += 1
        s0 = (len(d) + off) % VRAM
        for i in range(n):
            d.append(byte_at(s0 + i))
    else:
        r0 = 0
        if r7 == 1:
            r6 = src[p]
            p += 1
            r7 = 8
        r7 -= 1
        r0 |= r6 & 1
        r6 >>= 1
        if r7 == 1:
            r6 = src[p]
            p += 1
            r7 = 8
        r7 -= 1
        r0 <<= 1
        r0 |= r6 & 1
        r6 >>= 1
        r2 = src[p]
        p += 1
        off = r2 - 256
        n = r0 + 2
        s0 = (len(d) + off) % VRAM
        for i in range(n):
            d.append(byte_at(s0 + i))
print('unpacked', len(d), 'consumed', p, 'of', len(src))
open('_work/review_fixes/ascii_cgz.bin', 'wb').write(d)
