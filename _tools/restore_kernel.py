# -*- coding: utf-8 -*-
"""Stellt 1ST_READ.PRG aus den ORIGINAL-Discs in den gepatchten Discs wieder her."""
import glob
import os
import sys

sys.path.insert(0, '_tools')
from iso9660 import ISO9660Reader

sys.stdout.reconfigure(encoding='latin1')
SECT, DATA = 2352, 2048


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


def write(lba, data, path):
    with open(path, 'r+b') as f:
        for k in range((len(data) + DATA - 1) // DATA):
            f.seek((lba + k) * SECT + 16)
            f.write(data[k * DATA:(k + 1) * DATA])


for d in (1, 2, 3, 4):
    cands = glob.glob('Original_CD%d/*(Track 1).bin' % d)
    if not cands:
        print('d%d: Original-Track-1 fehlt' % d)
        continue
    orig = cands[0]
    oiso = ISO9660Reader(orig)
    rec = None
    for f in oiso.list_files():
        if f['name'].upper() == '1ST_READ.PRG':
            rec = f
            break
    data = read(rec['lba'], rec['size'], orig)
    pbin = '_work/patched_disc%d.bin' % d
    piso = ISO9660Reader(pbin)
    prec = None
    for f in piso.list_files():
        if f['name'].upper() == '1ST_READ.PRG':
            prec = f
            break
    print('d%d: orig lba %d size %d -> patched lba %d size %d' % (
        d, rec['lba'], rec['size'], prec['lba'], prec['size']))
    if prec['size'] != rec['size']:
        print('  Groesse unterschiedlich - uebersprungen')
        continue
    write(prec['lba'], data, pbin)
print('fertig')
