# -*- coding: utf-8 -*-
"""Minimaler ISO9660-Leser fuer PDS-Disc-Abbilder (BIN, 2352 B/Sektor).

Ersetzt das frueher extern genutzte pds-tools/common/iso9660.py.
API: ISO9660Reader(path).list_files() / .extract_file(lba, size),
SECTOR_SIZE, DATA_SIZE, read_sector(f, n).
"""
import struct

SECTOR_SIZE = 2352
DATA_SIZE = 2048


def read_sector(f, n):
    """Roh-Sektor n (2352 Bytes) aus einer BIN-Datei."""
    f.seek(n * SECTOR_SIZE)
    return f.read(SECTOR_SIZE)


def _user_data(raw):
    if len(raw) < SECTOR_SIZE:
        return b''
    if raw[15] == 1:
        return raw[16:16 + DATA_SIZE]
    if raw[15] == 2:
        sub = raw[18]
        if sub & 0x20:  # Form 2
            return raw[24:24 + 2324]
        return raw[24:24 + DATA_SIZE]
    return raw[16:16 + DATA_SIZE]


class ISO9660Reader:
    def __init__(self, path):
        self.path = path
        self._f = open(path, 'rb')
        self._root = self._read_root()

    # ---- low level ----
    def sector(self, n):
        return _user_data(read_sector(self._f, n))

    def read_bytes(self, lba, size):
        out = bytearray()
        need = size
        s = lba
        while need > 0:
            chunk = self.sector(s)
            if not chunk:
                break
            out += chunk[:need]
            need -= min(DATA_SIZE, need)
            s += 1
        return bytes(out[:size])

    def _read_root(self):
        pvd = self.sector(16)
        if len(pvd) < 190:
            raise ValueError('kein ISO9660-PVD bei Sektor 16')
        rec = pvd[156:156 + 34]
        ext = struct.unpack('<I', rec[2:6])[0]
        size = struct.unpack('<I', rec[10:14])[0]
        return (ext, size)

    # ---- directory walk ----
    def _parse_dir(self, lba, size):
        data = self.read_bytes(lba, size)
        pos = 0
        out = []
        while pos + 34 <= len(data):
            ln = data[pos]
            if ln == 0:
                pos += (DATA_SIZE - (pos % DATA_SIZE)) or DATA_SIZE
                continue
            rec = data[pos:pos + ln]
            pos += ln
            if len(rec) < 34:
                break
            ext = struct.unpack('<I', rec[2:6])[0]
            dsize = struct.unpack('<I', rec[10:14])[0]
            flags = rec[25]
            nlen = rec[32]
            name = rec[33:33 + nlen].decode('latin1', 'ignore')
            if name in ('\x00', '\x01'):
                continue
            name = name.split(';')[0]
            out.append({'name': name, 'lba': ext, 'size': dsize,
                        'dir': bool(flags & 0x02)})
        return out

    def list_files(self):
        root_lba, root_size = self._root
        entries = []
        pending = [(root_lba, root_size)]
        seen = set()
        while pending:
            lba, size = pending.pop(0)
            if (lba, size) in seen:
                continue
            seen.add((lba, size))
            for e in self._parse_dir(lba, size):
                if e['dir']:
                    pending.append((e['lba'], e['size']))
                else:
                    entries.append(e)
        return entries

    def extract_file(self, lba, size):
        return self.read_bytes(lba, size)
