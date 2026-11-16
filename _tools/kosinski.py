# -*- coding: utf-8 -*-
"""Kosinski-Decompressor (Referenz: Clownacy/accurate-kosinski).
Format: 16-Bit-Descriptor LE, Bits LSB-first.
"""
import sys

sys.stdout.reconfigure(encoding='latin1')


def kosinski_decompress(data):
    pos = 0
    out = bytearray()
    desc = 0
    bits = 0

    def rb():
        nonlocal pos
        b = data[pos]
        pos += 1
        return b

    def get_desc():
        nonlocal desc, bits
        lo = rb()
        hi = rb()
        desc = (hi << 8) | lo
        bits = 16

    def pop():
        nonlocal desc, bits
        v = desc & 1
        desc >>= 1
        bits -= 1
        if bits == 0:
            get_desc()
        return v

    get_desc()
    while True:
        if pop():
            out.append(rb())
        else:
            if pop():
                lo = rb()
                hi = rb()
                dist = ((hi & 0xF8) << 5) | lo
                dist = (dist ^ 0x1FFF) + 1
                count = hi & 7
                if count:
                    count += 2
                else:
                    count = rb() + 1
                    if count == 1:
                        break            # terminator
                    if count == 2:
                        continue         # 0xA000 boundary flag
            else:
                count = 2
                if pop():
                    count += 2
                if pop():
                    count += 1
                dist = (rb() ^ 0xFF) + 1
            src = len(out) - dist
            if src < 0:
                raise ValueError('distance before start: %d' % dist)
            for i in range(count):
                out.append(out[src + i])
    return bytes(out), pos


if __name__ == '__main__':
    path = sys.argv[1]
    src = open(path, 'rb').read()
    out, used = kosinski_decompress(src)
    print('%s: %d -> %d bytes (used %d of %d)' % (
        path, len(src), len(out), used, len(src)))
    dst = sys.argv[2] if len(sys.argv) > 2 else path + '.raw'
    open(dst, 'wb').write(out)
    print('geschrieben:', dst)
