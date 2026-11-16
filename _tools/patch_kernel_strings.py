# -*- coding: utf-8 -*-
"""Uebersetzt die Speicher-/Lade-Menue- und Gebietsnamen im Kernel
(1ST_READ.PRG) aller vier Discs - direkt inkl. Font-Slot-Umlauten.

Nur Datenbytes in der String-Tabelle (0x3D2C0..0x3DA00) werden angefasst.
Laengenregel: len(de) <= len(orig).  Padding: 0x00.
"""
import sys

sys.path.insert(0, '_tools')
from iso9660 import ISO9660Reader
import umlaut_conv as U

sys.stdout.reconfigure(encoding='latin1')
SECT, DATA = 2352, 2048

# (Original, Deutsch, umlaut_konvertieren)
ROWS = [
    ('Save Game to Internal RAM', 'Speichern: Intern-RAM', True),
    ('Save Game to Cartridge RAM', 'Speichern: Cartridge-RAM', True),
    ('Save Game to Expanded Memory', 'Speichern: Erw.-Speicher', True),
    ('You may save your game.', 'Spielstand speichern.', True),
    ('Location:', 'Ort: ', True),
    ('Will erase old file. Execute?\n', 'Alte Datei loeschen?\n', True),
    ('Saving:  Do not power down.', 'Nicht ausschalten!', True),
    ('Not enough space to save.', 'Nicht genug Platz.', True),
    ('NO DATA', 'LEER', True),
    ('NO BLOCK', 'VOLL', True),
    ('The data has been saved.', 'Daten gespeichert.', True),
    ('Cannot be saved correctly.', 'Sichern nicht moeglich.', True),
    ('Load Game From Internal RAM', 'Spielstand aus Intern-RAM', True),
    ('Load Game From Cartridge RAM', 'Spielstand aus Cartridge-RAM', True),
    ('Load Game From Expanded Memory', 'Spielstand aus Erw.-Speicher', True),
    ('Not used', 'Frei', True),
    ('Load Game', 'Laden', True),
    ('It is incorrect data.', 'Daten ungueltig.', True),
    ('Above the Excavation', 'Ueber der Ausgrabung', True),
    ('Excavation Site', 'Ausgrabungsort', True),
    ('Camp', 'Feld', True),
    ('Valley', 'Tal', True),
    ('Village of Cainus', 'Dorf Cainus', True),
    ('Garil Desert', 'Garil-Wueste', True),
    ('Caravan', 'Nomaden', True),
    ('Forbidden Zone', 'Verbotene Zone', True),
    ('Village of Zoah', 'Dorf Zoah', True),
    ('Imperial Air Force', 'Reichsluftwaffe', True),
    ('Air Force Post', 'Luftposten', True),
    ('The Tower', 'Der Turm', True),
    ('Uru Underground Ruins', 'Uru-Untergrund', True),
    ('Forest of Zoah', 'Wald von Zoah', True),
    ("Seekers' Stronghold", 'Sucherfestung', True),
    ('PRESS START BUTTON', 'START DR~CKEN', False),  # bereits Slot-fertig
]


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


LO, HI = 0x3D000, 0x3DA00
problems = 0

for disc in (1, 2, 3, 4):
    binp = '_work/patched_disc%d.bin' % disc
    iso = ISO9660Reader(binp)
    rec = None
    for f in iso.list_files():
        if f['name'].upper() == '1ST_READ.PRG':
            rec = f
            break
    if not rec:
        print('d%d: 1ST_READ.PRG fehlt' % disc)
        problems += 1
        continue
    data = bytearray(read(rec['lba'], rec['size'], binp))
    changed = 0
    for orig, de_ascii, do_conv in ROWS:
        needle = orig.encode('latin1')
        de = U.convert_text(de_ascii) if do_conv else de_ascii
        new = de.encode('latin1')
        if len(new) > len(needle):
            print('d%d BUDGET %r (%d) -> %r (%d)' % (
                disc, orig, len(needle), de, len(new)))
            problems += 1
            continue
        pos = 0
        hits = 0
        while True:
            a = data.find(needle + b'\x00', pos)
            if a < 0:
                break
            pos = a + 1
            if not (LO <= a <= HI):
                print('d%d AUSSERHALB %r @%x' % (disc, orig, a))
                problems += 1
                continue
            b = a + len(needle)
            data[a:a + len(new)] = new
            for k in range(a + len(new), b + 1):
                data[k] = 0x00
            hits += 1
            changed += 1
        if hits == 0:
            print('d%d NICHT GEFUNDEN %r' % (disc, orig))
            problems += 1
    write(rec['lba'], bytes(data), binp)
    print('d%d: %d Ersetzungen (Kernel-LBA %d)' % (disc, changed, rec['lba']))

print('Probleme:', problems)
