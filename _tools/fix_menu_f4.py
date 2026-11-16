# -*- coding: utf-8 -*-
# Offset-basierter Force-Fixer fuer Menue-Texte (TUTORIAL/MEN/BTL/FLD/
# TWN-Residuen).  Zeilen: (file, off, neues DE).  Schreibt pro Disc,
# wo die Datei existiert und die ALTER-DE-Bytes (aus der CSV) am
# Offset stehen, und synchronisiert die *_de.csv.  Idempotent.
import csv
import io
import os
import sys

sys.stdout.reconfigure(encoding='latin1')
SECT, DATA = 2352, 2048

ROWS = [
    # (file, off, neues DE, vorheriges DE auf allen Discs)
    ('TUTORIAL.CGB', 70777, 'Zur Sucher-Festung', 'Halt'),
    ('TUTORIAL.CGB', 70842, 'Zur Sucher-Festung', 'Halt'),
    ('BTL_T0.FNT', 342932, 'Handeln jederzeit moeglich,\nsobald die '
     'noetigen\nAnzeigen geladen sind.',
     'Aktion jederzeit, sobald die\nnoetigen Anzeigen geladen.'),
    ('BTL_T0.FNT', 344634, 'Die Abwehr an den Seiten\n(links/rechts) '
     'ist hoch,\nSchaden bleibt dort klein.',
     'Die Abwehr an den Seiten\n(hoch) nimmt wenig Schaden.'),
    ('BTL_T0.FNT', 344956, 'Wie zu sehen, ist Positionieren\nvital '
     'fuer Ausweichen und\nKampf. Wer es beherrscht,\nsichert sein '
     'Ueberleben im\nKosmos von Panzer Dragoon.',
     'Wie zu sehen, ist Positionie-\nren vital fuer Ausweichen und\n'
     'Kampf. Beherrscht man es,\nsichert man das Ueberleben\nim '
     'Panzer-Dragoon-Universum.'),
    ('BTL_T0.FNT', 345241, 'Der Laser zielt nur auf\nnaechstgelegene '
     'Feinde.\nMehr Schaden als Edges\nWaffe, doch kein Fernziel.',
     'Der Laser zielt nur die\nnaechsten Feinde. Obwohl\nLaser mehr '
     'Schaden als Edges\nWaffe, kann man nicht auf\nferne Ziele '
     'zielen.'),
    ('BTL_T0.FNT', 346547, 'Ein Spezialangriff hat den\nDrachen '
     'gelaehmt.',
     'Auf dem Radar zeigt Rot nicht\nnur hohes physisches Risiko,\n'
     'sondern einen moeglichen\nSpezialangriff.'),
    ('BTL_X0.FNT', 407644, 'BETAEUBUNG', 'BETAEUB AN'),
    ('FLD_A3.MCB', 39231, 'Sind die Anzeigen voll,\nwillst du '
     'kombinieren.\nStarte eine Aktion und\ndruecke sofort eine '
     'Taste\nfuer die naechste Aktion.',
     'Sind die Anzeigen voll und\ndu kombinieren willst,\neine '
     'Aktion und druecke\nsofort eine Taste fuer die\nnaechste '
     'Aktion.'),
]
CSV_DIR = '_work/menu_de/'


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


def csv_rows(stem):
    import glob as g
    for path in sorted(g.glob(CSV_DIR + stem.replace('.', '_')
                              .replace(' ', '') + '_de*.csv')):
        with io.open(path, encoding='latin1') as fh:
            rd = csv.reader(fh, delimiter=';')
            try:
                next(rd)
            except StopIteration:
                pass
            for r in rd:
                if len(r) >= 6 and r[0] and \
                        r[0].upper().endswith(('FNT', 'MCB', 'SCB',
                                               'CGB', 'PRG')):
                    if os.path.splitext(r[0])[0] != stem.split('.')[0]:
                        continue
        yield path, rd  # not reached per file; see below


def load_csv_for(stem):
    """Alle CSV-Spaltenzeilen je Datei: (path, dict off->row)."""
    import glob as g
    pat = CSV_DIR + stem.replace('.', '_') + '_de*.csv'
    out = []
    for path in sorted(g.glob(pat)):
        rows = {}
        with io.open(path, encoding='latin1') as fh:
            rd = csv.reader(fh, delimiter=';')
            next(rd, None)
            for r in rd:
                if len(r) >= 6 and r[0].replace('.', '_') == \
                        stem.replace('.', '_') and r[1].isdigit():
                    rows[int(r[1])] = r
        if rows:
            out.append((path, rows))
    return out


MODE = sys.argv[1] if len(sys.argv) > 1 else 'dry'
DRY = MODE != 'apply'

# CSV-Zeilen EINMAL vorab einlesen (Snapshot fuer alle Discs).
SNAP = {}
for d in (1, 2, 3, 4):
    pass
SNAP_ROWS = []
for name, off, new, old_pre in ROWS:
    src = None
    for path, rows in load_csv_for(name):
        if off in rows and src is None:
            src = (path, rows[off])
    SNAP_ROWS.append((name, off, new, src, old_pre))

csv_writes = {}
for d in (1, 2, 3, 4):
    idx = fs_index(d)
    names = {t[0] for t in ROWS}
    data_by_file = {}
    for name in sorted(names):
        if name not in idx:
            continue
        lba, size = idx[name]
        data_by_file[name] = bytearray(read_file(
            '_work/patched_disc%d.bin' % d, lba, size))
    touched = set()
    for name, off, new, src, old_pre in SNAP_ROWS:
        if name not in data_by_file:
            continue
        data = data_by_file[name]
        if src is None:
            print('d%d %-11s off=%d CSV-Zeile fehlt' % (d, name, off))
            continue
        path, row = src
        en_u = row[4].replace('\\n', '\n')
        old_de = row[5].replace('\\n', '\n')
        new_u = new.replace('\\n', '\n')
        budget = len(en_u.encode('latin1'))
        new_b = new_u.encode('latin1')
        if len(new_b) > budget:
            print('d%d %-11s off=%d BUDGET %d>%d' % (
                d, name, off, len(new_b), budget))
            continue
        cur = bytes(data[off:off + len(new_b)])
        if cur == new_b:
            print('d%d %-11s off=%d already_ok' % (d, name, off))
            continue
        matched = None
        for cand in (old_de, old_pre):
            cb = cand.encode('latin1')
            if bytes(data[off:off + len(cb)]) == cb:
                matched = cand
                break
        if matched is None:
            seen = bytes(data[off:off + len(old_de.encode('latin1'))])
            print('d%d %-11s off=%d SKIP (bytes sind %r)' % (
                d, name, off, seen[:20]))
            continue
        data[off:off + len(new_b)] = new_b
        for k in range(off + len(new_b),
                       min(off + budget, len(data))):
            data[k] = 0x00 if k == off + len(new_b) else 0xFF
        touched.add(name)
        csv_writes[(path, row[0], off)] = new.replace('\n', '\\n')
    if not DRY:
        for name in sorted(touched):
            lba, size = idx[name]
            write_file_regions('_work/patched_disc%d.bin' % d, lba,
                               bytes(data_by_file[name]))
            print('d%d %-11s written' % (d, name))

if not DRY:
    for (path, fname, off), new in csv_writes.items():
        lines = io.open(path, encoding='latin1').read().split('\n')
        for i, ln in enumerate(lines):
            q = ln.rstrip('\r\n').split(';')
            if len(q) >= 6 and q[0] == fname and q[1].isdigit() \
                    and int(q[1]) == off:
                q[5] = new.replace('\n', '\\n')
                lines[i] = ';'.join(q)
        io.open(path, 'w', encoding='latin1', newline='').write(
            '\n'.join(lines))

print('mode=%s' % MODE)
