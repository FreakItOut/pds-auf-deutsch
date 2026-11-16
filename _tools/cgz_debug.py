# Debug des CGZ-Decompressors
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
print('head:', src[:32].hex(' '))
d = bytearray()
p = 0
r6 = src[p]
p += 1
r7 = 9
lit = match = 0
while True:
    if r7 == 1:
        if p >= len(src):
            print('EOF src'); break
        r6 = src[p]
        p += 1
        r7 = 8
    r7 -= 1
    bit = r6 & 1
    r6 >>= 1
    if bit:
        d.append(src[p])
        p += 1
        lit += 1
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
            print('END marker at out', len(d), 'src', p)
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
        s = len(d) + off
        if s < 0 or s >= len(d):
            print('BAD match off=%d n=%d out=%d p=%d' % (off, n, len(d), p))
            break
        for i in range(n):
            d.append(d[s + i])
        match += 1
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
        off = (r2 | 0xFF00)
        off -= 0x10000 if off >= 0x8000 else 0
        n = r0 + 2
        s = len(d) + off
        if s < 0 or s >= len(d):
            print('BAD short off=%d n=%d out=%d p=%d' % (off, n, len(d), p))
            break
        for i in range(n):
            d.append(d[s + i])
        match += 1
print('out', len(d), 'src consumed', p, 'lit', lit, 'match', match)
