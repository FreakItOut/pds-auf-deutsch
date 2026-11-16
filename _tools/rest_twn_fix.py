# final TWN subtitle fixes (4 remaining prose/labels) + patch all 4 discs
import sys
import csv
sys.stdout.reconfigure(encoding='latin1')

SECT, DATA = 2352, 2048

FIX = {
    ('TWN_CAMP_PRG', 0): '(Das Holz knistert im Feuer.)',
    ('TWN_JIRI_PRG', 0): 'Ruinen-Untergesch.',
    ('TWN_RUIN_PRG', 0): 'Sucher-Festung',
    ('TWN_SEEK_PRG', 1195): 'Weicht Lasern',
}


def fs_index(d):
    fs = ('_work/fs_records_all.csv' if d == 1
          else '_work/fs_records_cd%d.csv' % d)
    return {r['name']: (int(r['lba']), int(r['size']))
            for r in csv.DictReader(open(fs, encoding='latin1'), delimiter=';')
            if int(r['lba']) > 0}


def read_file(binp, lba, size):
    out = bytearray()
    with open(binp, 'rb') as f:
        while size > 0:
            f.seek(lba * SECT + 16)
            c = f.read(min(DATA, size))
            if not c:
                break
            out += c
            size -= len(c)
            lba += 1
    return bytes(out)


def write_file_regions(binp, lba, data):
    with open(binp, 'r+b') as f:
        for k in range((len(data) + DATA - 1) // DATA):
            f.seek((lba + k) * SECT + 16)
            f.write(data[k * DATA:(k + 1) * DATA])


by_stem = {}
for (s, u), de in FIX.items():
    by_stem.setdefault(s, []).append((u, de))
errs = writes = 0

for stem in sorted(by_stem):
    fname = stem.replace('_PRG', '.PRG')
    rows = []
    for ln in open('_work/subtitles/%s_de.csv' % stem, encoding='latin1'):
        q = ln.rstrip('\r\n').split(';')
        if len(q) >= 6 and q[0].isdigit():
            rows.append((int(q[0]), q))
    rmap = dict(rows)
    for d in (1, 2, 3, 4):
        idx = fs_index(d)
        if fname not in idx:
            continue
        lba, size = idx[fname]
        binp = '_work/patched_disc%d.bin' % d
        data = bytearray(read_file(binp, lba, size))
        touch = False
        for u, de in by_stem[stem]:
            entry = rmap.get(u)
            offs = [int(x) for x in entry[3].split('|') if x] or [int(entry[2])]
            o1 = offs[0]
            en = entry[4]
            en_b = en.encode('latin1')
            de_b = de.encode('latin1')
            if len(de_b) > len(en_b):
                errs += 1
                continue
            end = min(o1 + len(en_b), len(data))
            data[o1:o1 + len(de_b)] = de_b
            fill = o1 + len(de_b)
            for k in range(fill, end):
                data[k] = 0x00 if k == fill else 0xFF
            writes += 1
            touch = True
        if touch:
            write_file_regions(binp, lba, bytes(data))
print('writes:', writes, 'errs:', errs)

# sync the csv de column too
for (stem, uid), de in FIX.items():
    p = '_work/subtitles/%s_de.csv' % stem
    lines = open(p, encoding='latin1').read().split('\n')
    out = []
    for line in lines:
        q = line.rstrip('\r\n').split(';')
        if len(q) >= 6 and q[0].isdigit() and int(q[0]) == uid:
            q[5] = de
            line = ';'.join(q)
        out.append(line)
    open(p, 'w', encoding='latin1', newline='\n').write('\n'.join(out))
print('csv synced')
