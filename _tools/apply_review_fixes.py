# Apply review fixes from a specified fixes CSV to the patched discs.
# Usage: python apply_review_fixes.py <fixes_csv>
# Format: source_file;en;old_de;new_de;reason
import csv
import os
import sys

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SECT = 2352
DATA = 2048

FIXES = sys.argv[1] if len(sys.argv) > 1 else '_work/review_fixes/TWN_SEEK_small_fixes.csv'


def read_file(binpath, lba, size):
    out = bytearray()
    need = size
    s = lba
    with open(binpath, 'rb') as f:
        while need > 0:
            f.seek(s * SECT + 16)
            c = f.read(min(DATA, need))
            if not c:
                break
            out += c
            need -= len(c)
            s += 1
    return bytes(out[:size])


def write_file_regions(binpath, lba, filedata):
    with open(binpath, 'r+b') as f:
        for k in range((len(filedata) + DATA - 1) // DATA):
            f.seek((lba + k) * SECT + 16)
            f.write(filedata[k * DATA:(k + 1) * DATA])


def fs_index(disc):
    fs = ('_work/fs_records_all.csv' if disc == 1
          else f'_work/fs_records_cd{disc}.csv')
    return {r['name']: (int(r['lba']), int(r['size']))
            for r in csv.DictReader(open(fs, encoding='latin1'),
                                    delimiter=';')
            if int(r['lba']) > 0 and int(r['size']) > 0}


def fsname(src):
    return src.replace('_PRG_de.csv', '.PRG')


# load fixes
fixes = []
with open(FIXES, encoding='latin1') as fh:
    rd = csv.reader(fh, delimiter=';')
    next(rd)  # header
    for r in rd:
        if len(r) >= 5 and r[3] and r[3] != r[2] and r[2].strip().lower() != 'de':
            fixes.append((r[0], r[1], r[2], r[3]))

print('fixes loaded:', len(fixes))

groups = {}
for src, en, old, new in fixes:
    groups.setdefault(src, []).append((en, old, new))

total_applied = total_skipped = 0
for src, items in sorted(groups.items()):
    name = fsname(src)
    sub = f'_work/subtitles/{src}'
    en_off = {}
    if os.path.exists(sub):
        with open(sub, encoding='latin1') as fh:
            for ln in fh:
                parts = ln.rstrip('\r\n').split(';')
                if len(parts) >= 5:
                    e = parts[4]
                    offs = [int(x) for x in parts[2].split('|') if x]
                    en_off.setdefault(e, []).extend(offs)
    for d in (1, 2, 3, 4):
        idx = fs_index(d)
        if name not in idx:
            continue
        lba, size = idx[name]
        binp = f'_work/patched_disc{d}.bin'
        data = bytearray(read_file(binp, lba, size))
        applied = skipped = 0
        written = {}
        for en, old, new in items:
            old_b = old.encode('latin1')
            new_b = new.encode('latin1')
            en_b = en.encode('latin1')
            if len(new_b) > len(en_b):
                skipped += 1
                continue
            targets = []
            if d == 1 and en in en_off:
                for off in en_off[en]:
                    if data[off:off + len(old_b)] == old_b:
                        targets.append((off, off + len(en_b)))
            if not targets:
                start = 0
                while True:
                    i = data.find(old_b + b'\x00', start)
                    if i < 0:
                        break
                    j = i + len(old_b) + 1
                    while j < len(data) and data[j] in (0x00, 0xFF):
                        j += 1
                    if len(new_b) + 1 <= j - i:
                        targets.append((i, j))
                    start = i + 1
            if not targets:
                skipped += 1
                continue
            for off, slot_end in targets:
                if off + len(new_b) >= len(data):
                    continue
                data[off:off + len(new_b)] = new_b
                for k in range(off + len(new_b), slot_end):
                    data[k] = 0x00 if k == off + len(new_b) else 0xFF
                written[off] = new_b
                applied += 1
        write_file_regions(binp, lba, bytes(data))
        chk = read_file(binp, lba, size)
        mism = sum(1 for off, nb in written.items()
                   if chk[off:off + len(nb)] != nb)
        print('disc %d %-12s applied=%4d skipped=%4d readback-mismatch=%d'
              % (d, name, applied, skipped, mism))
        total_applied += applied
        total_skipped += skipped

print('TOTAL applied=%d skipped=%d' % (total_applied, total_skipped))
