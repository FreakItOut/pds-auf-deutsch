# -*- coding: utf-8 -*-
# PDS-Kosinski mit VDP2-VRAM als Ringspeicher (0x80000, vorher genullt).
import sys

sys.stdout.reconfigure(encoding='latin1')
VRAM = 0x80000


def decompress(data, field='pds', start=0, maxout=0x40000):
    pos = start + 1
    r6 = data[start]
    r7 = 9
    mem = bytearray(VRAM)
    outn = 0

    def bit():
        nonlocal pos, r6, r7
        r7 -= 1
        if r7 == 0:
            r6 = data[pos]
            pos += 1
            r7 = 8
        b = r6 & 1
        r6 >>= 1
        return b

    def byte():
        nonlocal pos
        b = data[pos]
        pos += 1
        return b

    while outn < maxout:
        if bit():
            mem[outn % VRAM] = byte()
            outn += 1
            continue
        if bit():
            a = byte()
            b = byte()
            v = a | (b << 8)
            if field == 'pds':
                if v == 0:
                    break
                count = v & 7
                if count:
                    count += 2
                else:
                    count = byte() + 1
                delta = (v >> 3) - 8192
            else:
                if v == 0:
                    break
                count = b & 7
                if count:
                    count += 2
                else:
                    count = byte() + 1
                    if count == 1:
                        break
                    if count == 2:
                        continue
                delta = (((b & 0xF8) << 5) | a) - 8192
        else:
            count = 2
            if bit():
                count += 2
            if bit():
                count += 1
            delta = -((byte() ^ 0xFF) + 1)
        src = outn + delta
        for i in range(count):
            mem[outn % VRAM] = mem[(src + i) % VRAM]
            outn += 1
    return bytes(mem[:min(outn, VRAM)]), pos, outn


if __name__ == '__main__':
    src = open(sys.argv[1], 'rb').read()
    for field in ('pds', 'std'):
        for start in (0, 0x20):
            try:
                out, used, n = decompress(src, field, start)
                print('%s start=%#x -> %d (used %d/%d)' % (
                    field, start, n, used, len(src)))
                if 1000 < n < 0x40000:
                    open('_work/ascii_cgz/vram_%s_%x.raw' % (
                        field, start), 'wb').write(out)
            except Exception as e:
                print('%s start=%#x -> %s' % (field, start, e))
