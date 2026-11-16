# Sucht den Systemfont (Signatur aus resetVdp2StringsData) im Disc-Image.
import sys

sys.stdout.reconfigure(encoding='latin1')
SECT, DATA = 2352, 2048


def image_bytes(path):
    out = bytearray()
    with open(path, 'rb') as f:
        while True:
            c = f.read(SECT)
            if not c:
                break
            out += c[16:16 + DATA]
    return bytes(out)


sig = bytes.fromhex('00000000030013200840048033303330'
                    '048008401320030000000000')
sig2 = bytes.fromhex('00010005000000000000000000000000')
img = image_bytes('_work/patched_disc1.bin')
print('image user bytes', len(img))
for name, s in (('glyph0', sig), ('header', sig2)):
    pos = img.find(s)
    hits = []
    while pos != -1 and len(hits) < 5:
        hits.append(pos)
        pos = img.find(s, pos + 1)
    print(name, 'hits:', [hex(x) for x in hits])
