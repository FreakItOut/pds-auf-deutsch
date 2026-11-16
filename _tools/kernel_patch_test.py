# -*- coding: utf-8 -*-
"""Patcht nur ausgewaehlte Kernel-Strings (fuer Boot-Bisect).

Aufruf:  python _tools/kernel_patch_test.py "Label" [--pad 00|ff|keep] "Orig1" "Orig2" ...
Ohne Strings: schreibt das Original unveraendert zurueck (Schreibpfad-Test).
"""
import math
import sys

sys.path.insert(0, '_tools')
from iso9660 import ISO9660Reader

sys.stdout.reconfigure(encoding='latin1')
SECT, DATA = 2352, 2048

T = {
    'Load Game From Internal RAM': 'Spielstand aus Intern-RAM',
    'Load Game From Cartridge RAM': 'Spielstand aus Cartridge-RAM',
    'Load Game From Expanded Memory': 'Spielstand aus Erw.-Speicher',
    'Not used': 'Frei',
    'Cannot be saved correctly.': 'Sichern nicht moeglich.',
    'Load Game': 'Laden',
    'It is incorrect data.': 'Daten ungueltig.',
    'Above the Excavation': 'Ueber der Ausgrabung',
    'Excavation Site': 'Ausgrabungsort',
    'Camp': 'Feld',
    'Valley': 'Tal',
    'Village of Cainus': 'Dorf Cainus',
    'Garil Desert': 'Garil-Wueste',
    'Caravan': 'Nomaden',
    'Forbidden Zone': 'Verbotene Zone',
    'Village of Zoah': 'Dorf Zoah',
    'Imperial Air Force': 'Reichsluftwaffe',
    'Air Force Post': 'Luftposten',
    'The Tower': 'Der Turm',
    'Uru Underground Ruins': 'Uru-Untergrund',
    'Forest of Zoah': 'Wald von Zoah',
    "Seekers' Stronghold": 'Sucherfestung',
}


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


args = sys.argv[1:]
pad = 'ff'
if '--pad' in args:
    i = args.index('--pad')
    pad = args[i + 1]
    del args[i:i + 2]
label = args[0] if args else 'orig'
wanted = args[1:]
orig_bin = '_work/restore_disc%d.bin'

# Original-Kernel einlesen (aus Disc 1) und zuerst identisch zurueckschreiben
pbin = '_work/patched_disc%d.bin' % 1
oiso = ISO9660Reader(orig_bin % 1)
orec = [f for f in oiso.list_files() if f['name'].upper() == '1ST_READ.PRG'][0]
orig = bytearray(read(orec['lba'], orec['size'], orig_bin % 1))
piso = ISO9660Reader(pbin)
prec = [f for f in piso.list_files() if f['name'].upper() == '1ST_READ.PRG'][0]
write(prec['lba'], bytes(orig), pbin)

if wanted:
    changed = 0
    for s in wanted:
        if s not in T:
            print('unbekannt:', s)
            continue
        needle = s.encode('latin1')
        pos = 0
        while True:
            a = orig.find(needle, pos)
            if a < 0:
                break
            pos = a + 1
            b = a + len(needle)
            if b >= len(orig) or orig[b] != 0:
                continue
            new = T[s].encode('latin1')
            if len(new) > len(needle):
                print('BUDGET', s)
                continue
            orig[a:a + len(new)] = new
            if pad == 'ff':
                for k in range(a + len(new), b):
                    orig[k] = 0xFF
            elif pad == '00':
                for k in range(a + len(new), b):
                    orig[k] = 0x00
            changed += 1
    write(prec['lba'], bytes(orig), pbin)
    print('%s: %d Ersetzungen (pad=%s)' % (label, changed, pad))
else:
    print('%s: Original unveraendert zurueckgeschrieben' % label)
