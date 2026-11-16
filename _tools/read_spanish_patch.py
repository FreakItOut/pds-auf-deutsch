# -*- coding: utf-8 -*-
import glob
import io
import os
import sys
import zlib

sys.stdout.reconfigure(encoding='latin1')
base = [d for d in glob.glob('PZS_CD1*') if os.path.isdir(d)][0]
p = os.path.join(base, 'Parcheador PDSaga Disco 1', 'parche.saturno')
raw = open(p, 'rb').read()
i = raw.find(b'\x1f\x8b\x08')
print('gzip at', hex(i), 'file size', len(raw))
dec = zlib.decompressobj(31)
out = bytearray()
chunk = raw[i:i + 1 << 20]
data = dec.decompress(chunk, 4 * 1024 * 1024)
out += data
print('first decompressed', len(out))
open('_work/review_fixes/spanish_prefix.bin', 'wb').write(out)
print('head', out[:32].hex(' '))
# ISO-Record fuer ASCII.CGZ suchen
j = out.find(b'ASCII.CGZ')
print('ASCII.CGZ string at', hex(j) if j >= 0 else -1)
if j >= 0:
    rec = j - 33
    import struct
    ext = struct.unpack('<I', out[rec + 2:rec + 6])[0]
    size = struct.unpack('<I', out[rec + 10:rec + 14])[0]
    print('record ext', ext, 'size', size)
