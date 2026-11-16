# patch FLD_D5.FNT / TWN_RUIN all 4 discs — apply my good values to the first copy only
import sys
import csv
sys.stdout.reconfigure(encoding='latin1')
SECT, DATA = 2352, 2048


def fs_index(d):
    fs = ('_work/fs_records_all.csv' if d == 1
          else '_work/fs_records_cd%d.csv' % d)
    return {r['name']: (int(r['lba']), int(r['size']))
            for r in csv.DictReader(open(fs, encoding='latin1'),
                                    delimiter=';')
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


# the listing for RUIN uid 100 gives TWO copies. The CSV break-track uses off0
# so must be applied at BOTH offsets.
FIX = {
    ('TWN_RUIN_PRG', 100): ('Sie ging, als ich',
                            'fort war,'),
    ('TWN_RUIN_PRG', 101): ('Ich haette jemanden',
                            'da sein lassen.'),
    ('TWN_RUIN_PRG', 108): ('Ich weiss: Glaubst',
                            'du'),
    ('TWN_RUIN_PRG', 109): ('sie tut',
                            'etwas Toerichtes?'),
}
by_val = {}
for (s, u), (d1, d2) in FIX.items():
    by_val.setdefault(s, {})[u] = (d1, d2)

writes = 0
errs = []
patched_first = {}
for stem, umap in by_val.items():
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
        umap = {u: (d1, d2) for u, (d1, d2) in umap.items()}
        # patch EVERY offset listed for each uid
        for u, (d1, d2) in umap.items():
            ea = rmap.get(u)
            if not ea:
                continue
            offs = [int(x) for x in ea[3].split('|') if x] or [int(ea[2])]
            for o1 in offs:
                en_b = ea[4].encode('latin1')
                de_b = d1.encode('latin1')
                if len(de_b) > len(en_b):
                    continue
                end = min(o1 + len(en_b), len(data))
                data[o1:o1 + len(de_b)] = de_b
                fill = o1 + len(de_b)
                for k in range(fill, end):
                    data[k] = 0x00 if k == fill else 0xFF
                writes += 1
                patched_first[o1] = de_b
        write_file_regions(binp, lba, bytes(data))
print('writes:', writes, 'errs:', len(errs))
