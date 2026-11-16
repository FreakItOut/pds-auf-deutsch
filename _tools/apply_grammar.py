# Applies grammar fix batches to all discs + syncs CSV (idempotent).
# usage: python apply_grammar.py [dry|apply]
import csv
import sys

sys.stdout.reconfigure(encoding='latin1')
SECT, DATA = 2352, 2048

import fix_accuracy1
import fix_batch1
import fix_batch2
import fix_chains_camp
import fix_chains_r2
import fix_chains_ruin
import fix_chains_seek
import fix_chains_seek2
import fix_labels_f4
import fix_polish3
import fix_polish4
import fix_ruin2
import fix_seek2

STEMS = {}
for mod in (fix_batch1, fix_batch2):
    for stem, fixes in mod.STEMS.items():
        STEMS.setdefault(stem, {}).update(fixes)
STEMS.setdefault('TWN_SEEK_PRG', {}).update(fix_seek2.FIX)
STEMS.setdefault('TWN_RUIN_PRG', {}).update(fix_ruin2.FIX)
for stem, fixes in fix_polish3.STEMS.items():
    STEMS.setdefault(stem, {}).update(fixes)
for stem, fixes in fix_polish4.STEMS.items():
    STEMS.setdefault(stem, {}).update(fixes)
for stem, fixes in fix_chains_camp.STEMS.items():
    STEMS.setdefault(stem, {}).update(fixes)
for stem, fixes in fix_chains_ruin.STEMS.items():
    STEMS.setdefault(stem, {}).update(fixes)
for stem, fixes in fix_chains_seek.STEMS.items():
    STEMS.setdefault(stem, {}).update(fixes)
for stem, fixes in fix_labels_f4.STEMS.items():
    STEMS.setdefault(stem, {}).update(fixes)
for stem, fixes in fix_chains_seek2.STEMS.items():
    STEMS.setdefault(stem, {}).update(fixes)
for stem, fixes in fix_chains_r2.STEMS.items():
    STEMS.setdefault(stem, {}).update(fixes)
for stem, fixes in fix_accuracy1.STEMS.items():
    STEMS.setdefault(stem, {}).update(fixes)


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


def load_rows(stem):
    rows = {}
    order = {}
    with open('_work/subtitles/%s_de.csv' % stem, encoding='latin1') as f:
        n = -1
        for line in f:
            n += 1
            p = line.rstrip('\r\n').split(';')
            if len(p) >= 6 and p[0].isdigit():
                uid = int(p[0])
                rows[uid] = p
                order[uid] = n
    return rows, order


MODE = sys.argv[1] if len(sys.argv) > 1 else 'dry'
DRY = MODE != 'apply'
writes = 0
fails = []

for stem, fixes in STEMS.items():
    rows, order = load_rows(stem)
    name = stem.replace('_PRG', '.PRG')
    uids = sorted(fixes)
    lines = None
    if not DRY:
        with open('_work/subtitles/%s_de.csv' % stem, encoding='latin1') as f:
            lines = f.read().split('\n')
    for d in (1, 2, 3, 4):
        idx = fs_index(d)
        if name not in idx:
            continue
        lba, size = idx[name]
        binp = '_work/patched_disc%d.bin' % d
        data = bytearray(read_file(binp, lba, size))
        touch = False
        for uid in uids:
            if uid not in rows:
                fails.append('%s uid=%d missing row' % (stem, uid))
                continue
            en_b = rows[uid][4].encode('latin1')
            de = fixes[uid]
            de_b = de.encode('latin1')
            if len(de_b) > len(en_b):
                fails.append('%s uid=%d BUDGET %d>%d' % (stem, uid, len(de_b), len(en_b)))
                continue
            if any(ord(c) > 127 for c in de):
                fails.append('%s uid=%d NONASCII %r' % (stem, uid, de))
                continue
            offs = [int(x) for x in rows[uid][3].split('|') if x]
            if not offs:
                offs = [int(rows[uid][2])]
            for o in offs:
                if o + max(len(en_b), 1) > len(data):
                    fails.append('%s uid=%d off=%d OOB' % (stem, uid, o))
                    continue
                old = actual(data, o)
                span = max(len(en_b), len(old))
                end = o + span
                data[o:o + len(de_b)] = de_b
                fill = o + len(de_b)
                for k in range(fill, min(end, len(data))):
                    data[k] = 0x00 if k == fill else 0xFF
                writes += 1
                touch = True
        if touch:
            if not DRY:
                write_file_regions(binp, lba, bytes(data))
            print('%s d%d ok' % (name, d))
    if not DRY:
        for uid in uids:
            if uid not in rows:
                continue
            n = order[uid]
            q = lines[n].rstrip('\r\n').split(';')
            if len(q) >= 6 and int(q[0]) == uid:
                q[5] = fixes[uid]
                lines[n] = ';'.join(q)
        with open('_work/subtitles/%s_de.csv' % stem, 'w',
                  encoding='latin1', newline='') as f:
            f.write('\n'.join(lines))

print('mode=%s slots=%d fails=%d' % (MODE, writes, len(fails)))
for x in fails[:40]:
    print('  FAIL', x)
