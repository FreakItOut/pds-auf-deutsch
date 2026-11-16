# Mechanischer Ketten-Ende-Fixer fuer alle TWN-CSVs.
# Wenn die letzte DE-Zeile einer Kette ohne Abschlusszeichen endet,
# aber das letzte EN mit '.'/')'/.../!'?' schliesst, und der NAECHSTE
# Block nicht kleinschreibend weiterfuehrt, wird das Zeichen angehaengt
# (nur wenn Budget reicht).  Idempotent, mit Readback.
import csv
import glob
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding='latin1')
SECT, DATA = 2352, 2048
TERMINAL = ('.', '!', '?', ')')


def unesc(s):
    return s.replace('\\n', '\n').replace('\\t', '\t')


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


def actual(data, o):
    e = o
    while e < len(data) and data[e] not in (0x00, 0xFF):
        e += 1
    return data[o:e].decode('latin1')


MODE = sys.argv[1] if len(sys.argv) > 1 else 'dry'
DRY = MODE != 'apply'

total = 0
fails = []
for path in sorted(glob.glob('_work/subtitles/TWN_*_de.csv')):
    stem = os.path.basename(path)[:-7]
    name = stem.replace('_PRG', '.PRG')
    rows = []
    with io.open(path, encoding='latin1') as fh:
        for line in fh:
            p = line.rstrip('\r\n').split(';')
            if len(p) >= 6 and p[0].isdigit():
                rows.append({'uid': int(p[0]),
                             'off': int(p[2].split('|')[0]) if p[2]
                             else 0,
                             'offs': [int(x) for x in p[3].split('|')
                                      if x] or [int(p[2])],
                             'en': p[4], 'de': p[5],
                             'oline': line.rstrip('\r\n')})
    rows.sort(key=lambda r: r['off'])
    # Ketten: Segment endet nach einem EN mit terminal
    chains = []
    cur = [rows[0]]
    for r in rows[1:]:
        if cur and cur[-1]['en'].strip().endswith(TERMINAL):
            chains.append(cur)
            cur = []
        cur.append(r)
    chains.append(cur)
    fix = {}
    for members in chains:
        last = members[-1]
        de = last['de'].rstrip()
        en = last['en'].strip()
        if not en or not de:
            continue
        if de.endswith(TERMINAL):
            continue
        # Naechster Block kleinschreibend?  Dann laeuft der Text weiter.
        nxt = members[-1]
        idx = rows.index(last) + 1
        nxt = rows[idx] if idx < len(rows) else None
        if nxt and unesc(nxt['de'])[:1].islower():
            continue
        if not en.endswith(TERMINAL):
            continue
        if en.endswith('...'):
            add = '...'
        elif en.endswith(')'):
            add = ')'
        elif en.endswith('?'):
            continue  # unbekannte Frageform: nicht automatisch
        else:
            add = '.'
        en_b = unesc(last['en']).encode('latin1')
        de_b = unesc(last['de']).encode('latin1')
        if len(de_b) + len(add) > len(en_b):
            continue
        new = last['de'] + add
        fix[last['uid']] = new
    if not fix:
        continue
    # Disc-Patch fuer alle Discs, wo die Datei existiert
    for d in (1, 2, 3, 4):
        idx = fs_index(d)
        if name not in idx:
            continue
        lba, size = idx[name]
        data = bytearray(read_file('_work/patched_disc%d.bin' % d, lba,
                                   size))
        touch = False
        for uid, new in fix.items():
            row = next(r for r in rows if r['uid'] == uid)
            de_b = unesc(row['de']).encode('latin1')
            new_b = unesc(new).encode('latin1')
            en_b = unesc(row['en']).encode('latin1')
            if len(new_b) > len(en_b):
                fails.append('%s uid=%d BUDGET' % (stem, uid))
                continue
            for o in row['offs']:
                if o >= len(data):
                    fails.append('%s uid=%d OOB' % (stem, uid))
                    continue
                cur_actual = actual(data, o)
                if cur_actual != row['de']:
                    fails.append('%s uid=%d off=%d DISC!=%r' % (
                        stem, uid, o, cur_actual[:30]))
                    continue
                data[o:o + len(new_b)] = new_b
                fill = o + len(new_b)
                end = o + max(len(en_b), len(cur_actual))
                for k in range(fill, min(end, len(data))):
                    data[k] = 0x00 if k == fill else 0xFF
                touch = True
                total += 1
        if touch and not DRY:
            write_file_regions('_work/patched_disc%d.bin' % d, lba,
                               bytes(data))
    if not DRY and fix:
        lines = io.open(path, encoding='latin1').read().split('\n')
        for uid, new in fix.items():
            for i, ln in enumerate(lines):
                q = ln.rstrip('\r\n').split(';')
                if len(q) >= 6 and q[0].isdigit() and int(q[0]) == uid:
                    q[5] = new
                    lines[i] = ';'.join(q)
        io.open(path, 'w', encoding='latin1', newline='').write(
            '\n'.join(lines))
    print('%-14s fixes=%d' % (stem, len(fix)))

print('mode=%s total=%d fails=%d' % (MODE, total, len(fails)))
for x in fails[:20]:
    print('  FAIL', x)
