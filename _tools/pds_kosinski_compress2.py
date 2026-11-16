# -*- coding: utf-8 -*-
"""Stärkerer PDS-Kosinski-Kompressor: Hash-Ketten + Lazy Matching."""
import sys


def _build_chains(data, max_chain=64, window=8192):
    chains = {}
    n = len(data)
    for i in range(n - 2):
        key = data[i:i+3]
        lst = chains.get(key)
        if lst is None:
            chains[key] = [i]
        else:
            lst.append(i)
    return chains


def compress(data, max_len=256, window=8192, max_chain=96):
    n = len(data)
    chains = _build_chains(data)
    out = bytearray()
    st = {'bp': -1, 'bl': 0}

    def putbit(b):
        if st['bl'] == 0:
            st['bp'] = len(out)
            out.append(0)
            st['bl'] = 8
        if b:
            out[st['bp']] |= 1 << (8 - st['bl'])
        st['bl'] -= 1

    def longest(pos, limit):
        if pos + 2 >= n:
            return 0, 0
        key = data[pos:pos+3]
        lst = chains.get(key)
        if not lst:
            return 0, 0
        best = 0
        bestd = 0
        lo = pos - window
        cnt = 0
        for j in reversed(lst):
            if j >= pos:
                continue
            if j < lo:
                break
            cnt += 1
            if cnt > max_chain:
                break
            if best and j + best < n and data[j+best] != data[pos+best]:
                continue
            ln = 3
            while ln < limit and j + ln < n and data[j+ln] == data[pos+ln]:
                ln += 1
            if ln > best:
                best = ln
                bestd = pos - j
                if ln == limit:
                    break
        return best, bestd

    def emit_long(dist, length):
        putbit(0)
        putbit(1)
        if 2 <= length <= 9:
            v = ((window - dist) << 3) | (length - 2)
            out.append(v & 0xFF)
            out.append(v >> 8)
        else:
            v = (window - dist) << 3
            out.append(v & 0xFF)
            out.append(v >> 8)
            out.append(length - 1)

    def emit_inline(dist, length):
        putbit(0)
        putbit(0)
        c = length - 2
        putbit((c >> 1) & 1)
        putbit(c & 1)
        out.append(256 - dist)

    pos = 0
    while pos < n:
        limit = min(n - pos, max_len)
        ln, dist = longest(pos, limit)
        # Lazy: pruefe naechste Position
        if ln >= 3 and pos + 1 < n:
            ln2, d2 = longest(pos + 1, min(n - pos - 1, max_len))
            if ln2 > ln:
                putbit(1)
                out.append(data[pos])
                pos += 1
                continue
        if ln >= 3:
            emit_long(dist, ln)
            pos += ln
        else:
            ln2, d2 = longest(pos, min(n - pos, 5))
            if ln2 == 2 and d2 <= 256:
                emit_inline(d2, 2)
                pos += 2
            else:
                putbit(1)
                out.append(data[pos])
                pos += 1
    putbit(0)
    putbit(1)
    out.append(0)
    out.append(0)
    return bytes(out)


if __name__ == '__main__':
    sys.path.insert(0, '_tools')
    from pds_kosinski3 import decompress
    src = open(sys.argv[1], 'rb').read()
    comp = compress(src)
    dec, used, n = decompress(comp)
    print('%d -> %d; roundtrip=%s out=%d' % (
        len(src), len(comp), dec[:len(src)] == src, n))
    if len(sys.argv) > 2:
        open(sys.argv[2], 'wb').write(comp)
