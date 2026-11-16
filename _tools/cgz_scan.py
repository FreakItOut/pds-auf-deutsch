# Probiert CGZ-Decompress-Startoffsets 0..64 durch.
import csv
import sys

sys.stdout.reconfigure(encoding='latin1')
SECT, DATA = 2352, 2048
VRAM = 0x80000


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


def run(p0, maxout=200000):
    d = bytearray()
    p = p0
    try:
        r6 = src[p]
    except IndexError:
        return None
    p += 1
    r7 = 9
    while True:
        if p >= len(src):
            return (len(d), 'EOF', p)
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
        else:
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
                    return (len(d), 'END', p)
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
                    d.append(d[s0 + i] if 0 <= s0 + i < len(d) else 0)
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
                    d.append(d[s0 + i] if 0 <= s0 + i < len(d) else 0)
        if len(d) > maxout:
            return (len(d), 'MAX', p)


for p0 in range(0, 65):
    r = run(p0)
    print('p0=%02x -> %s' % (p0, r))
