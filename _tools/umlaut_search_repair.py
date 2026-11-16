# -*- coding: utf-8 -*-
# Repariert Menue-/Tutorial-Texte, deren CSV-Offsets veraltet sind:
# sucht den alten DE-Text direkt in der Datei und ersetzt ihn dort.
import glob
import io
import os
import sys

sys.path.insert(0, '_tools')
from umlaut_codec import convert_text

sys.stdout.reconfigure(encoding='latin1')
SECT, DATA = 2352, 2048


def fs_index(disc):
    fs = ('_work/fs_records_all.csv' if disc == 1
          else '_work/fs_records_cd%d.csv' % disc)
    out = {}
    for r in __import__('csv').DictReader(open(fs, encoding='latin1'),
                                          delimiter=';'):
        if int(r['lba']) > 0:
            out[r['name']] = (int(r['lba']), int(r['size']))
    return out


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


def stem_to_file(stem):
    base = stem
    for suf in ('_d2', '_d3', '_d4'):
        if base.endswith(suf):
            base = base[:-3]
    if base == 'TWN_E128_cd3':
        return 'TWN_E128.PRG'
    return base.replace('_PRG', '.PRG')


rows = []
for path in sorted(glob.glob('_work/menu_de/*_de.csv')):
    for i, ln in enumerate(io.open(path, encoding='latin1')):
        p = ln.rstrip('\r\n').split(';')
        if len(p) >= 6 and p[1].isdigit() and p[0]:
            rows.append({'csv': path, 'line': i, 'file': p[0],
                         'off': int(p[1]), 'en': p[4], 'de': p[5]})

cache = {}
csv_updates = {}
nf = []
done = 0
notfound = 0
for r in rows:
    if '.' not in r['file']:
        continue
    new = convert_text(r['de'])
    if new == r['de']:
        continue
    old = r['de']
    variants = [old]
    if '\\n' in old:
        variants.append(old.replace('\\n', '\n'))
    found = False
    chosen = new
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
        for var in variants:
            ob = var.encode('latin1')
            if not ob:
                continue
            pos = bytes(data).find(ob)
            while pos != -1:
                act = var
                na = convert_text(act)
                nb = na.encode('latin1')
                if len(nb) <= len(ob):
                    end = pos + max(len(ob), len(nb))
                    data[pos:pos + len(nb)] = nb
                    fill = pos + len(nb)
                    for k in range(fill, min(end, len(data))):
                        data[k] = 0x00 if k == fill else 0xFF
                    done += 1
                    found = True
                pos = bytes(data).find(ob, pos + 1)
        # Fragment-Suche (erste Zeile / erste 24 Zeichen)
        if not found:
            frag = old.split('\\n')[0][:24].replace('""', '"').strip('"')
            if len(frag) >= 8:
                fb = frag.encode('latin1')
                pos = bytes(data).find(fb)
                while pos != -1:
                    # Stringgrenzen
                    s0 = pos
                    while s0 > 0 and 32 <= data[s0 - 1] < 127:
                        s0 -= 1
                    e0 = pos
                    while e0 < len(data) and (32 <= data[e0] < 127
                                              or data[e0] == 0x0A):
                        e0 += 1
                    act = bytes(data[s0:e0]).decode('latin1')
                    if len(act) <= 400:
                        na = convert_text(act)
                        nab = na.encode('latin1')
                        if len(nab) <= len(act.encode('latin1')):
                            data[s0:s0 + len(nab)] = nab
                            fill = s0 + len(nab)
                            for k in range(fill,
                                           s0 + len(act.encode('latin1'))):
                                data[k] = 0x00 if k == fill else 0xFF
                            done += 1
                            found = True
                            chosen = na.replace('\n', '\\n')
                    pos = bytes(data).find(fb, pos + 1)
    if found:
        csv_updates.setdefault(r['csv'], {})[r['line']] = chosen
    else:
        notfound += 1
        nf.append('%s | %s | off=%d | %s' % (
            r['csv'], r['file'], r['off'], old))

for (d, name), (lba, data) in cache.items():
    write_file('_work/patched_disc%d.bin' % d, lba, bytes(data))
for path, upd in csv_updates.items():
    lines = io.open(path, encoding='latin1').read().split('\n')
    for i, new in upd.items():
        p = lines[i].rstrip('\r\n').split(';')
        if len(p) >= 6:
            p[5] = new
            lines[i] = ';'.join(p)
    io.open(path, 'w', encoding='latin1', newline='').write(
        '\n'.join(lines))
print('search-repair: replaced=%d rows_not_found=%d csvs=%d' % (
    done, notfound, len(csv_updates)))
io.open('_work/review_fixes/umlaut_notfound.txt', 'w',
        encoding='latin1', newline='\n').write('\n'.join(nf))
