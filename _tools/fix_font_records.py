# -*- coding: utf-8 -*-
# Repariert die ISO-Directory-Records nach dem Font-Patch:
#  - ASCII.CGZ: echte Groesse = komprimierte Fontgroesse
#  - falsch geaenderter Record 0xC556 aus Backup wiederherstellen
import struct
import sys

sys.stdout.reconfigure(encoding='latin1')
SECT, DATA = 2352, 2048
NEW_SIZE = 9425


def find_ascii_record(img):
    pos = 0
    while True:
        p = img.find(b'ASCII.CGZ', pos)
        if p < 0:
            return None
        rec = p - 33
        if 0 <= rec and rec + 40 <= len(img) and img[rec] == 42:
            return rec
        pos = p + 1


for d in (1, 2, 3, 4):
    path = '_work/patched_disc%d.bin' % d
    bak = '_work/backup_preumlaut/patched_disc%d.bin' % d
    img = bytearray(open(path, 'rb').read())
    rec = find_ascii_record(img)
    print('disc', d, 'ascii record', hex(rec) if rec else None)
    if rec is None:
        continue
    print('  extent', struct.unpack('<I', img[rec+2:rec+6])[0],
          'old size', struct.unpack('<I', img[rec+10:rec+14])[0])
    # ASCII.CGZ-Groesse setzen
    img[rec+10:rec+14] = struct.pack('<I', NEW_SIZE)
    img[rec+14:rec+18] = struct.pack('>I', NEW_SIZE)
    # falschen Record 0xC556 aus Backup restaurieren
    b = open(bak, 'rb').read()
    print('  falscher Record Name:', b[0xc556+33:0xc556+33+b[0xc556+32]]
          .decode('latin1', 'ignore'))
    img[0xc556+10:0xc556+18] = b[0xc556+10:0xc556+18]
    open(path, 'wb').write(img)
    print('  korrigiert')
