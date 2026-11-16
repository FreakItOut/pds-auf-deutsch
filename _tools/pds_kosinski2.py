# -*- coding: utf-8 -*-
"""Kosinski/PDS-Decompressor mit exakter C-Semantik:
if (--r7 == 0) { r6 = next; r7 = 8; } bit = r6 & 1; r6 >>= 1;
Zwei Feld-Layouts: 'pds' (count=low 3 bits, dist=>>3) und
'std' (Kosinski: count=high&7, dist=((high&0xF8)<<5)|low).
"""


def decompress(data, field='pds', start=0):
    pos = start + 1
    r6 = data[start]
    r7 = 9
    out = bytearray()

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

    while True:
        if bit():
            out.append(byte())
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
                sv = v - 0x10000 if v & 0x8000 else v
                dist = -(sv >> 3)
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
                off = ((b & 0xF8) << 5) | a
                dist = (off ^ 0x1FFF) + 1
        else:
            count = 2
            if bit():
                count += 2
            if bit():
                count += 1
            dist = (byte() ^ 0xFF) + 1
        src = len(out) - dist
        if src < 0:
            raise ValueError('dist before start %d at %d' % (
                dist, len(out)))
        for i in range(count):
            out.append(out[src + i])
    return bytes(out), pos


if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='latin1')
    src = open(sys.argv[1], 'rb').read()
    for field in ('pds', 'std'):
        for start in (0, 0x20):
            try:
                out, used = decompress(src, field, start)
                print('%s start=%#x -> %d bytes (used %d/%d)' % (
                    field, start, len(out), used, len(src)))
                if len(out) > 500:
                    open('_work/ascii_cgz/out_%s_%x.raw' % (
                        field, start), 'wb').write(out)
            except Exception as e:
                print('%s start=%#x -> %s' % (field, start, e))
