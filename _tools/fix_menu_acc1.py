# -*- coding: utf-8 -*-
# Acc1: Offset-Fixes fuer Menue-/Battle-/Tutorial- und TWN-Sondertexte.
# (file, off, neues DE, altes DE) - idempotent, Budget + Byte-Check.
import csv
import glob
import io
import os
import sys

sys.stdout.reconfigure(encoding='latin1')
SECT, DATA = 2352, 2048

ROWS = [
    ('TUTORIAL.CGB', 55659, 'Du und dein Freund koennten',
     'Du und dein Freund koennt'),
    ('TUTORIAL.CGB', 55688, 'mir was schulden, hm?',
     'mir was schulden.'),
    ('TWN_SEEK.PRG', 58333, '(Fluessigkeit leuchtet.)',
     '(Fluess. leuchtet.)'),
    ('TWN_E128.PRG', 58333, '(Fluessigkeit leuchtet.)',
     '(Die Fluess. leuchtet.)'),
    ('TWN_E128.PRG', 58413, 'Der Inhalt im Topf leuchtet.',
     '(Fluessigkeit leuchtet.)'),
    ('BTL_C2.FNT', 358265, 'Patrouillen verstaerken, los!',
     'Alle Einheiten, Patr. verst..'),
    ('BTL_B5.FNT', 335891, 'Einheiten, hoechste Vorsicht!',
     'Alle Einheiten, hoechste Vors..'),
]
CSV_DIRS = ('_work/menu_de', '_work/subtitles')


def fs_index(disc):
    fs = ('_work/fs_records_all.csv' if disc == 1
          else '_work/fs_records_cd%d.csv' % disc)
    return {r['name']: (int(r['lba']), int(r['size']))
            for r in csv.DictReader(open(fs, encoding='latin1'),
                                    delimiter=';') if int(r['lba']) > 0}


def read_file(binp, lba, size):
    out = bytearray()
    need, s = size, lba
    with open(binp, 'rb') as f:
        while need > 0:
            f.seek(s * SECT + 16)
            c = f.read(min(DATA, need))
            if not c:
                break
            out += c
            need -= len(c)
            s += 1
    return bytes(out[:size])


def write_file_regions(binp, lba, data):
    with open(binp, 'r+b') as f:
        for k in range((len(data) + DATA - 1) // DATA):
            f.seek((lba + k) * SECT + 16)
            f.write(data[k * DATA:(k + 1) * DATA])


def stem_to_file(stem):
    base = stem
    for suf in ('_d2', '_d3', '_d4'):
        if base.endswith(suf):
            base = base[:-3]
    if base == 'TWN_E128_cd3':
        return 'TWN_E128.PRG'
    return base.replace('_PRG', '.PRG')


def load_csv_rows(file, off):
    """Alle CSV-Zeilen, die (file, off) beschreiben."""
    hits = []
    for d in CSV_DIRS:
        for path in sorted(glob.glob(os.path.join(d, '*_de*.csv'))):
            stem = os.path.basename(path)
            stem = stem[:-7] if stem.endswith('_de.csv') else stem[:-8]
            lines = io.open(path, encoding='latin1').read().split('\n')
            for i, ln in enumerate(lines):
                p = ln.rstrip('\r\n').split(';')
                if len(p) < 6:
                    continue
                if d.endswith('menu_de'):
                    fname, foff = p[0], p[1]
                else:
                    fname = stem_to_file(stem)
                    foff = p[2].split('|')[0] if p[2] else ''
                if fname.upper() != file.upper():
                    continue
                if not foff.isdigit() or int(foff) != off:
                    continue
                hits.append((path, i, p, lines))
    return hits


MODE = sys.argv[1] if len(sys.argv) > 1 else 'dry'
DRY = MODE != 'apply'
painted = 0
csv_fix = {}

for file, off, new, old in ROWS:
    hits = load_csv_rows(file, off)
    if not hits:
        print('%-11s off=%d KEINE CSV-ZEILE' % (file, off))
        continue
    en = hits[0][2][4]
    budget = max(len(h[2][4].encode('latin1')) for h in hits)
    nb = new.encode('latin1')
    if len(nb) > budget:
        print('%-11s off=%d BUDGET %d>%d' % (file, off, len(nb),
                                             budget))
        continue
    if any(ord(c) > 127 for c in new):
        print('%-11s off=%d NONASCII' % (file, off))
        continue
    done = False
    for d in (1, 2, 3, 4):
        idx = fs_index(d)
        if file not in idx:
            continue
        lba, size = idx[file]
        binp = '_work/patched_disc%d.bin' % d
        data = bytearray(read_file(binp, lba, size))
        cur = bytes(data[off:off + len(nb)])
        if cur == nb:
            done = True
            continue
        ob = old.encode('latin1')
        if bytes(data[off:off + len(ob)]) != ob:
            obs = bytes(data[off:off + len(ob)])
            print('%-11s d%d off=%d SKIP (bytes %r)' % (
                file, d, off, obs[:20]))
            continue
        data[off:off + len(nb)] = nb
        fill = off + len(nb)
        for k in range(fill, min(off + max(budget, len(ob)), len(data))):
            data[k] = 0x00 if k == fill else 0xFF
        if not DRY:
            write_file_regions(binp, lba, bytes(data))
        done = True
        painted += 1
        print('%-11s d%d off=%d ok' % (file, d, off))
    if done:
        for path, i, p, lines in hits:
            q = list(p)
            q[5] = new
            lines[i] = ';'.join(q)
            csv_fix[path] = lines

if not DRY:
    for path, lines in csv_fix.items():
        io.open(path, 'w', encoding='latin1', newline='').write(
            '\n'.join(lines))
        print('csv aktualisiert:', path)
print('mode=%s writes=%d' % (MODE, painted))
