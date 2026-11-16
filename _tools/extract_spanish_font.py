# -*- coding: utf-8 -*-
import glob
import os
import struct
import sys
import zlib

sys.path.insert(0, '_tools')
from pds_kosinski3 import decompress

sys.stdout.reconfigure(encoding='latin1')
base = [d for d in glob.glob('PZS_CD1*') if os.path.isdir(d)][0]
p = os.path.join(base, 'Parcheador PDSaga Disco 1', 'parche.saturno')
raw = open(p, 'rb').read()
i = raw.find(b'\x1f\x8b\x08')
dec = zlib.decompressobj(31)
out = bytearray()
pos = i
while len(out) < 8 * 1024 * 1024 and pos < len(raw):
    chunk = raw[pos:pos + 1 << 20]
    pos += len(chunk)
    out += dec.decompress(chunk, 8 * 1024 * 1024 - len(out))
    if dec.eof:
        break
print('decompressed', len(out))
open('_work/review_fixes/spanish_archive.bin', 'wb').write(out)
j = out.find(b'ASCII.CGZ')
rec = j - 33
ext = struct.unpack('<I', out[rec + 2:rec + 6])[0]
size = struct.unpack('<I', out[rec + 10:rec + 14])[0]
print('ASCII.CGZ ext', ext, 'size', size)
off = ext * 2048
blob = out[off:off + size]
print('data at', hex(off), blob[:16].hex(' '))
if blob:
    try:
        font, used, n = decompress(blob)
        print('decompressed font', len(font))
        open('_work/review_fixes/spanish_font.raw', 'wb').write(font)
    except Exception as e:
        print('decompress failed', e)
