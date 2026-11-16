# rewrite apply_user_wording.py with a simpler 3-tuple layout
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


JOBS = [
    # (file, EN-text (as on disc), German-new)
    ('TWN_CAMP.PRG', "An'jou gave up on the search,",
     "An'jou hat aufgegeben,"),
    ('TWN_CAMP.PRG', "and returned here.", "kehrt hierher."),
    ('TWN_CAMP.PRG', "We can't feed him much,",
     "Wir koennen ihm nicht"),
    ('TWN_CAMP.PRG', "but we do our best...", "viel geben."),
    ('TWN_CAMP.PRG', "Shortly after he returned,",
     "Kurz nach seiner Rueckkehr",
    ),
    ('TWN_E022.PRG', "for her sake as well as mine!)",
     "Ihretwegen - und meinetwegen!"),
    ('TWN_RUIN.PRG', "I know. Do you think", "Glaubst du"),
    ('TWN_RUIN.PRG', "Do you think we stand a chance",
     "Denkst du wir haben Chancen"),
]

for fname, pairs in [(f, [(p[1], p[2]) for p in [j] * 1 for j in []
                          if False])
                     for f in []]:
    pass

by_file = {}
for job in JOBS:
    fname, en_t, de_t = job
    by_file.setdefault(fname, []).append((en_t, de_t))

for fname, pairs in by_file.items():
    for d in (1, 2, 3, 4):
        fs = ('_work/fs_records_all.csv' if d == 1
              else '_work/fs_records_cd%d.csv' % d)
        idx = {r['name']: (int(r['lba']), int(r['size']))
               for r in csv.DictReader(open(fs, encoding='latin1'),
                                       delimiter=';')
               if int(r['lba']) > 0}
        if fname not in idx:
            continue
        lba, size = idx[fname]
        binp = '_work/patched_disc%d.bin' % d
        data = bytearray(read_file(binp, lba, size))
        touch = False
        for en_t, de_t in pairs:
            en_b = en_t.encode('latin1')
            de_b = de_t.encode('latin1')
            if len(de_b) > len(en_b):
                continue
            i = 0
            while True:
                i = data.find(en_b, i)
                if i < 0:
                    break
                end = i + len(en_b)
                data[i:i + len(de_b)] = de_b
                fill = i + len(de_b)
                for k in range(fill, end):
                    data[k] = 0x00 if k == fill else 0xFF
                i += 1
                touch = True
        if touch:
            write_file_regions(binp, lba, bytes(data))
    print(fname, 'patched all discs')
