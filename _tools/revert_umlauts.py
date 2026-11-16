# -*- coding: utf-8 -*-
# Stellt alle Slot-Zeichen (^ | ~ { } [ ]) wieder auf ae/oe/ue/ss zurueck.
import glob
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding='latin1')
SECT, DATA = 2352, 2048
REV = {'^': 'ae', '|': 'oe', '~': 'ue', '{': 'ss',
       '}': 'AE', '[': 'OE', ']': 'UE'}


def rev(s):
    for k, v in REV.items():
        s = s.replace(k, v)
    return s


def load_rows():
    rows = []
    for path in sorted(glob.glob('_work/subtitles/TWN_*_de.csv')):
        stem = os.path.basename(path)[:-7]
        for i, ln in enumerate(io.open(path, encoding='latin1')):
            p = ln.rstrip('\r\n').split(';')
            if len(p) >= 6 and p[0].isdigit():
                offs = [int(x) for x in p[3].split('|') if x]
                if not offs:
                    try:
                        offs = [int(p[2].split('|')[0])]
                    except Exception:
                        offs = []
                rows.append({'csv': path, 'line': i, 'file': file_of(stem),
                             'offs': offs, 'en': p[4], 'de': p[5]})
    for path in sorted(glob.glob('_work/menu_de/*_de.csv')):
        for i, ln in enumerate(io.open(path, encoding='latin1')):
            p = ln.rstrip('\r\n').split(';')
            if len(p) >= 6 and p[1].isdigit() and p[0]:
                rows.append({'csv': path, 'line': i, 'file': p[0],
                             'offs': [int(p[1])], 'en': p[4], 'de': p[5]})
    return rows


def file_of(stem):
    base = stem
    for suf in ('_d2', '_d3', '_d4'):
        if base.endswith(suf):
            base = base[:-3]
    if base == 'TWN_E128_cd3':
        return 'TWN_E128.PRG'
    return base.replace('_PRG', '.PRG')


def fs_index(disc):
    fs = ('_work/fs_records_all.csv' if disc == 1
          else '_work/fs_records_cd%d.csv' % disc)
    import csv as _csv
    return {r['name']: (int(r['lba']), int(r['size']))
            for r in _csv.DictReader(open(fs, encoding='latin1'),
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


def write_file(binp, lba, data):
    with open(binp, 'r+b') as f:
        for k in range((len(data) + DATA - 1) // DATA):
            f.seek((lba + k) * SECT + 16)
            f.write(data[k * DATA:(k + 1) * DATA])


rows = load_rows()
changes = []
for r in rows:
    new = rev(r['de'])
    if new != r['de']:
        changes.append((r, new))
print('rows=%d changed=%d' % (len(rows), len(changes)))
cache = {}
done = 0
for r, new in changes:
    ob = r['de'].encode('latin1')
    nb = new.encode('latin1')
    for d in (1, 2, 3, 4):
        idx = fs_index(d)
        if r['file'] not in idx:
            continue
        key = (d, r['file'])
        if key not in cache:
            lba, size = idx[r['file']]
            cache[key] = [lba, bytearray(read_file(
                '_work/patched_disc%d.bin' % d, lba, size))]
        data = cache[key][1]
        for off in r['offs']:
            if bytes(data[off:off + len(ob)]) == ob:
                end = off + max(len(ob), len(nb))
                data[off:off + len(nb)] = nb
                fill = off + len(nb)
                for k in range(fill, min(end, len(data))):
                    data[k] = 0x00 if k == fill else 0xFF
                done += 1
for (d, name), (lba, data) in cache.items():
    write_file('_work/patched_disc%d.bin' % d, lba, bytes(data))
# CSVs aktualisieren
for path in set(r['csv'] for r, _ in changes):
    lines = io.open(path, encoding='latin1').read().split('\n')
    for r, new in changes:
        if r['csv'] != path:
            continue
        p = lines[r['line']].rstrip('\r\n').split(';')
        if len(p) >= 6:
            p[5] = new
            lines[r['line']] = ';'.join(p)
    io.open(path, 'w', encoding='latin1', newline='').write(
        '\n'.join(lines))
print('written=%d files=%d' % (done, len(cache)))
