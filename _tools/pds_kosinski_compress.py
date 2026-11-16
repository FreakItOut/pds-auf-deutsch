# -*- coding: utf-8 -*-
"""Kosinski-Kompressor (PDS-Variante), passend zu pds_kosinski3.decompress.
Nur Literale, Long-Matches und Inline-Matches; Terminator 0000.
"""
import sys


def compress(data, max_len=256, window=8192):
    out = bytearray()
    state = {'byte_pos': -1, 'bits_left': 0}

    def putbit(b):
        if state['bits_left'] == 0:
            state['byte_pos'] = len(out)
            out.append(0)
            state['bits_left'] = 8
        if b:
            out[state['byte_pos']] |= 1 << (8 - state['bits_left'])
        state['bits_left'] -= 1

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
        c = length - 2  # 0..3
        putbit((c >> 1) & 1)
        putbit(c & 1)
        out.append(256 - dist)

    n = len(data)
    pos = 0
    while pos < n:
        best_len = 0
        best_dist = 0
        if pos >= 1:
            start = max(0, pos - window)
            # simple hash of 2 bytes
            cand = []
            key = data[pos:pos + 2]
            j = start
            limit = min(n - pos, max_len)
            if limit >= 2:
                while j < pos:
                    if data[j:j + 2] == key:
                        ln = 2
                        while ln < limit and data[j + ln] == data[pos + ln]:
                            ln += 1
                        if ln > best_len:
                            best_len = ln
                            best_dist = pos - j
                            if ln == limit:
                                break
                    j += 1
        if best_len >= 3:
            emit_long(best_dist, best_len)
            pos += best_len
        elif best_len == 2 and best_dist <= 256:
            emit_inline(best_dist, 2)
            pos += 2
        else:
            putbit(1)
            out.append(data[pos])
            pos += 1
    # Terminator
    putbit(0)
    putbit(1)
    out.append(0)
    out.append(0)
    return bytes(out)


if __name__ == '__main__':
    import importlib.util
    sys.path.insert(0, '_tools')
    from pds_kosinski3 import decompress
    src = open(sys.argv[1], 'rb').read()
    comp = compress(src)
    dec, used, n = decompress(comp)
    ok = dec[:len(src)] == src
    print('%d -> %d bytes; roundtrip=%s (out %d)' % (
        len(src), len(comp), ok, n))
    if len(sys.argv) > 2:
        open(sys.argv[2], 'wb').write(comp)
