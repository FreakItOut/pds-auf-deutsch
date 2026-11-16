# -*- coding: utf-8 -*-
"""PDS-Kosinski-Kompressor mit dynamischer Programmierung (Bitkosten)."""
import sys


def compress(data, window=8192, max_len=256, max_chain=256):
    n = len(data)
    chains = {}
    for i in range(n - 2):
        key = data[i:i+3]
        chains.setdefault(key, []).append(i)

    def matches(pos):
        """Liste (length, dist) fuer diese Position, absteigend."""
        if pos + 2 >= n:
            return []
        lst = chains.get(data[pos:pos+3])
        if not lst:
            return []
        lo = pos - window
        res = []
        limit = min(max_len, n - pos)
        cnt = 0
        for j in reversed(lst):
            if j >= pos:
                continue
            if j < lo:
                break
            cnt += 1
            if cnt > max_chain:
                break
            ln = 3
            while ln < limit and data[j+ln] == data[pos+ln]:
                ln += 1
            res.append((ln, pos - j))
            if ln == limit:
                break
        res.sort(reverse=True)
        return res

    INF = 1 << 60
    cost = [INF] * (n + 1)
    choice = [None] * (n + 1)
    cost[n] = 0
    for pos in range(n - 1, -1, -1):
        c = 9 + cost[pos + 1]
        best = ('lit',)
        ms = matches(pos)[:6]
        for ln, dist in ms:
            maxl = min(ln, 256)
            for L in range(3, maxl + 1):
                if L <= 5 and dist <= 256:
                    cc = 10 + cost[pos + L]
                    if cc < c:
                        c = cc
                        best = ('inline', L, dist)
                if L <= 9:
                    cc = 18 + cost[pos + L]
                else:
                    cc = 26 + cost[pos + L]
                if cc < c:
                    c = cc
                    best = ('long', L, dist)
        cost[pos] = c
        choice[pos] = best

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

    pos = 0
    while pos < n:
        ch = choice[pos]
        if ch[0] == 'lit':
            putbit(1)
            out.append(data[pos])
            pos += 1
        elif ch[0] == 'long':
            _, L, dist = ch
            putbit(0)
            putbit(1)
            if L <= 9:
                v = ((window - dist) << 3) | (L - 2)
                out.append(v & 0xFF)
                out.append(v >> 8)
            else:
                v = (window - dist) << 3
                out.append(v & 0xFF)
                out.append(v >> 8)
                out.append(L - 1)
            pos += L
        else:
            _, L, dist = ch
            putbit(0)
            putbit(0)
            c = L - 2
            putbit((c >> 1) & 1)
            putbit(c & 1)
            out.append(256 - dist)
            pos += L
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
    dec, used, nn = decompress(comp)
    print('%d -> %d; roundtrip=%s out=%d' % (
        len(src), len(comp), dec[:len(src)] == src, nn))
    if len(sys.argv) > 2:
        open(sys.argv[2], 'wb').write(comp)
