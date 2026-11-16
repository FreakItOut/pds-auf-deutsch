# -*- coding: utf-8 -*-
# Patcht den Umlaut-Font in ASCII.CGZ aller vier Discs + ISO-Groesse.
import csv
import os
import struct
import sys

sys.path.insert(0, '_tools')
from iso9660 import ISO9660Reader, SECTOR_SIZE, DATA_SIZE
from pds_kosinski3 import decompress
from pds_kosinski_compress3 import compress

sys.stdout.reconfigure(encoding='latin1')

BASE = 0xC60
SLOTS = {'ä': 0x5E, 'ö': 0x7C, 'ü': 0x7E, 'ß': 0x7B}
FONT = '_work/ascii_cgz/font_de.raw'


def read_user(path, lba, size):
    out = bytearray()
    need, s = size, lba
    with open(path, 'rb') as f:
        while need > 0:
            f.seek(s * SECTOR_SIZE + 16)
            c = f.read(min(DATA_SIZE, need))
            if not c:
                break
            out += c
            need -= len(c)
            s += 1
    return bytes(out)


def write_user(path, lba, data):
    with open(path, 'r+b') as f:
        for k in range((len(data) + DATA_SIZE - 1) // DATA_SIZE):
            f.seek((lba + k) * SECTOR_SIZE + 16)
            f.write(data[k * DATA_SIZE:(k + 1) * DATA_SIZE])


def find_record(path, want):
    """Liefert (rec_abs_offset, lba, size) fuer eine Datei im ISO."""
    iso = ISO9660Reader(path)
    root_lba, root_size = iso._root
    pending = [(root_lba, root_size)]
    seen = set()
    while pending:
        lba, size = pending.pop(0)
        if (lba, size) in seen:
            continue
        seen.add((lba, size))
        data = iso.read_bytes(lba, size)
        pos = 0
        while pos + 34 <= len(data):
            ln = data[pos]
            if ln == 0:
                pos += DATA_SIZE - (pos % DATA_SIZE)
                continue
            rec = data[pos:pos + ln]
            ext = struct.unpack('<I', rec[2:6])[0]
            dsz = struct.unpack('<I', rec[10:14])[0]
            flags = rec[25]
            nlen = rec[32]
            name = rec[33:33 + nlen].decode('latin1', 'ignore')
            name = name.split(';')[0]
            if name in ('\x00', '\x01'):
                pos += ln
                continue
            if flags & 0x02:
                pending.append((ext, dsz))
            elif name.upper() == want.upper():
                abs_off = lba * SECTOR_SIZE + 16 + pos
                return abs_off, ext, dsz
            pos += ln
    return None


def main():
    font = open(FONT, 'rb').read()
    comp = compress(font)
    # Test-Roundtrip
    dec, used, n = decompress(comp)
    assert dec[:len(font)] == font, 'roundtrip failed'
    print('font: %d -> %d bytes (roundtrip ok)' % (len(font), len(comp)))
    if len(comp) > 10240:
        print('FEHLER: groesser als 5 Sektoren')
        return 2
    for d in (1, 2, 3, 4):
        path = '_work/patched_disc%d.bin' % d
        rec = find_record(path, 'ASCII.CGZ')
        if not rec:
            print('d%d: ASCII.CGZ nicht gefunden' % d)
            continue
        abs_off, lba, size = rec
        print('d%d: record@%#x lba=%d size=%d' % (d, abs_off, lba, size))
        # Datei schreiben (max 5 Sektoren)
        payload = comp + b'\x00' * (10240 - len(comp))
        write_user(path, lba, payload)
        # ISO-Groesse aktualisieren (LE + BE)
        with open(path, 'r+b') as f:
            f.seek(abs_off + 10)
            f.write(struct.pack('<I', len(comp)))
            f.write(struct.pack('>I', len(comp)))
        print('d%d: geschrieben (%d B)' % (d, len(comp)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
