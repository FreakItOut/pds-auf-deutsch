# -*- coding: utf-8 -*-
# Brute-Force ueber Kosinski-Varianten fuer ASCII.CGZ.
import sys

sys.stdout.reconfigure(encoding='latin1')
src = open('_work/ascii_cgz/disc1.cgz', 'rb').read()


def try_variant(start, desc_bits, desc_order, bit_msb, field, maxout=200000):
    pos = start
    desc = 0
    left = 0
    out = bytearray()

    def load_desc():
        nonlocal pos, desc, left
        if desc_bits == 8:
            desc = src[pos]
            pos += 1
            left = 8
        else:
            a = src[pos]
            b = src[pos + 1]
            pos += 2
            desc = (b << 8) | a if desc_order == 'le' else (a << 8) | b
            left = 16

    def rbit():
        nonlocal desc, left
        if left == 0:
            load_desc()
        if bit_msb:
            b = (desc >> (desc_bits - 1)) & 1
            desc = (desc << 1) & ((1 << desc_bits) - 1)
        else:
            b = desc & 1
            desc >>= 1
        left -= 1
        return b

    def rbyte():
        nonlocal pos
        b = src[pos]
        pos += 1
        return b

    load_desc()
    try:
        while len(out) < maxout:
            if rbit():
                out.append(rbyte())
                continue
            if rbit():
                a = rbyte()
                b = rbyte()
                if field == 'pds':
                    v = a | (b << 8)
                    if v == 0:
                        return ('END', len(out), pos)
                    count = v & 7
                    if count:
                        count += 2
                    else:
                        count = rbyte() + 1
                    sv = v - 0x10000 if v & 0x8000 else v
                    dist = -(sv >> 3)
                else:  # standard
                    v = a | (b << 8)
                    if v == 0:
                        return ('END', len(out), pos)
                    count = b & 7
                    off = ((b & 0xF8) << 5) | a
                    dist = (off ^ 0x1FFF) + 1
                    if count:
                        count += 2
                    else:
                        count = rbyte() + 1
                        if count == 1:
                            return ('END', len(out), pos)
                        if count == 2:
                            continue
            else:
                count = 2
                if rbit():
                    count += 2
                if rbit():
                    count += 1
                dist = (rbyte() ^ 0xFF) + 1
            s = len(out) - dist
            if s < 0:
                return ('NEG', len(out), dist)
            for i in range(count):
                out.append(out[s + i])
        return ('MAX', len(out), pos)
    except IndexError:
        return ('EOF', len(out), pos)


for start in (0x0, 0x10, 0x20, 0x24, 0x30):
    for db in (8, 16):
        for order in ('le', 'be'):
            for msb in (False, True):
                for field in ('pds', 'std'):
                    r = try_variant(start, db, order, msb, field)
                    if r[0] in ('END', 'MAX') and r[1] > 500:
                        print('START=%#x desc=%d %s msb=%s field=%s -> %s' % (
                            start, db, order, msb, field, r))
