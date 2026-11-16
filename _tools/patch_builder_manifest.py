# -*- coding: utf-8 -*-
"""Traegt die Hashes der gepatchten Discs in die Builder-Tabellen ein.

Der Recompile-Builder erkennt Programme ueber SHA-256. Weil unsere Discs
Text-Patches in den Programmen haben, werden sonst die hand-geschriebenen
Funktionen und die Enhancements abgeschaltet (schwarzer Bildschirm).

Gepatcht werden:
  builder.exe                      Manifest (Build-Zeit)
  runtime/lib/libpds_runtime.a     Manifest (kommt in die EXE)
  symbols/port_symbols.txt         Kernel-Hash -> Adresstabelle

Idempotent: alle Modul-Hashes der MK-81307/E-Bloecke werden auf den aktuellen
Stand der gepatchten Discs gesetzt.
"""
import glob
import hashlib
import re
import sys

sys.path.insert(0, '_tools')
from iso9660 import ISO9660Reader

sys.stdout.reconfigure(encoding='latin1')
SECT, DATA = 2352, 2048
BASE = 'pdt-recompile-builder-2.0.0-win64'


def read(lba, size, path):
    out = bytearray()
    need, s = size, lba
    with open(path, 'rb') as f:
        while need > 0:
            f.seek(s * SECT + 16)
            c = f.read(min(DATA, need))
            if not c:
                break
            out += c
            need -= len(c)
            s += 1
    return bytes(out[:size])


# Datei-Hashes der gepatchten Discs: disc -> {name: sha256}
disc_files = {}
for disc in (1, 2, 3, 4):
    binp = '_work/patched_disc%d.bin' % disc
    iso = ISO9660Reader(binp)
    table = {}
    for f in iso.list_files():
        if f['dir']:
            continue
        table[f['name'].upper()] = hashlib.sha256(
            read(f['lba'], f['size'], binp)).hexdigest()
    disc_files[disc] = table

kernel_hash = disc_files[1]['1ST_READ.PRG']
print('Kernel-SHA256:', kernel_hash)

HEX64 = re.compile(rb'[0-9a-f]{64}')


def patch_manifest(path):
    data = bytearray(open(path, 'rb').read())
    n = 0
    pos = 0
    while True:
        s = data.find(b'product MK-81307', pos)
        if s < 0:
            break
        e = data.find(b'\x00', s)
        pos = s + 1
        block = bytes(data[s:e]).decode('latin1')
        lines = block.split('\n')
        if 'area E' not in lines:
            continue
        dn = None
        for l in lines:
            if l.startswith('disc '):
                dn = int(l.split()[1])
        if dn not in disc_files:
            continue
        off = s
        for l in lines:
            lo = off
            off += len(l) + 1
            if not l.startswith('module '):
                continue
            parts = l.split(' ')
            if len(parts) != 3:
                continue
            name, h = parts[1].upper(), parts[2]
            cur = disc_files[dn].get(name)
            if not cur:
                # Datei gibt es auf unserer Disc nicht -> Eintrag unveraendert
                continue
            ho = lo + len('module ') + len(parts[1]) + 1
            if bytes(data[ho:ho + 64]).decode('latin1') != cur:
                data[ho:ho + 64] = cur.encode('ascii')
                n += 1
    open(path, 'wb').write(bytes(data))
    print('%s: %d Modul-Hashes aktualisiert' % (path, n))


for target in ('builder.exe', 'runtime/lib/libpds_runtime.a'):
    patch_manifest(BASE + '/' + target)

# port_symbols.txt: Kernel-Hash im MK-81307-Block ersetzen
p = BASE + '/symbols/port_symbols.txt'
b = open(p, 'rb').read()
m = re.search(rb'# North America and Europe \(MK-81307 V1\.000\)[^\n]*\n'
              rb'kernel ([0-9a-f]{64})', b)
if not m:
    print('port_symbols.txt: MK-81307-Block nicht gefunden')
else:
    old = m.group(1).decode('ascii')
    if old != kernel_hash:
        b = b[:m.start(1)] + kernel_hash.encode('ascii') + b[m.end(1):]
        open(p, 'wb').write(b)
        print('port_symbols.txt: kernel %s -> %s' % (old[:12], kernel_hash[:12]))
    else:
        print('port_symbols.txt: schon aktuell')

# libpds_runtime.a enthaelt eine eingebettete Kopie derselben Tabelle
p = BASE + '/runtime/lib/libpds_runtime.a'
b = open(p, 'rb').read()
m = re.search(rb'# North America and Europe \(MK-81307 V1\.000\)[^\n]*\n'
              rb'kernel ([0-9a-f]{64})', b)
if not m:
    print('libpds_runtime.a: MK-81307-Block nicht gefunden')
else:
    old = m.group(1).decode('ascii')
    if old != kernel_hash:
        b = b[:m.start(1)] + kernel_hash.encode('ascii') + b[m.end(1):]
        open(p, 'wb').write(b)
        print('libpds_runtime.a: kernel %s -> %s' % (old[:12], kernel_hash[:12]))
    else:
        print('libpds_runtime.a: schon aktuell')
