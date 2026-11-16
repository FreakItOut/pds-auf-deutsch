# -*- coding: utf-8 -*-
"""Kosinski-Variante von Panzer Dragoon Saga (PDS-Tweak).

Belegt durch AzelLib/VDP2.cpp: unpackGraphicsToVDP2():
- Deskriptor: EIN Byte, LSB-first, 8 Bit pro Byte.
- Literal: Bit=1 -> naechstes Byte.
- Sonst Bit2=1 -> Long-Match: zwei Bytes LE = value;
    value==0 -> Ende;
    count = value & 7 (+2; bei 0: naechstes Byte +1);
    Offset = (signed16 value) >> 3 (13-Bit-Distanz).
- Sonst Inline-Match: count = 2 + 2*bit3 + bit4;
    Distanz = -(256 - byte) (Byte als 8-Bit-Zweierkomplement).
"""


def pds_decompress(data):
    pos = 1
    desc = data[0]
    left = 9
    out = bytearray()

    def rbit():
        nonlocal pos, desc, left
        left -= 1
        if left == 0:
            desc = data[pos]
            pos += 1
            left = 8
        b = desc & 1
        desc >>= 1
        return b

    def rbyte():
        nonlocal pos
        b = data[pos]
        pos += 1
        return b

    while True:
        if rbit():
            out.append(rbyte())
            continue
        if rbit():
            lo = rbyte()
            hi = rbyte()
            v = lo | (hi << 8)
            if v == 0:
                break
            count = v & 7
            if count:
                count += 2
            else:
                count = rbyte() + 1
            sv = v - 0x10000 if v & 0x8000 else v
            off = sv >> 3
            dist = -off
        else:
            count = 2
            b3 = rbit()
            b4 = rbit()
            count += (b3 << 1) | b4
            dist = (rbyte() ^ 0xFF) + 1
        src = len(out) - dist
        if src < 0:
            raise ValueError('distance before start: %d at out=%d' % (
                dist, len(out)))
        for i in range(count):
            out.append(out[src + i])
    return bytes(out), pos


if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='latin1')
    path = sys.argv[1]
    src = open(path, 'rb').read()
    out, used = pds_decompress(src)
    print('%s: %d -> %d (used %d/%d)' % (
        path, len(src), len(out), used, len(src)))
    dst = sys.argv[2] if len(sys.argv) > 2 else path + '.raw'
    open(dst, 'wb').write(out)
    print('->', dst)
