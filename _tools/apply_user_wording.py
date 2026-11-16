# apply the 7 wording fixes requested by the user verbatim
# and patch each slot across all 4 discs.
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


# replace English placeholder text by German rewrite per requested wording
JOBS = [
    # CAMP 251: An'jou hat aufgegeben (EN: "An'jou gave up on the search,")
    ('TWN_CAMP.PRG', 'TWN_CAMP_PRG',
     ("An'jou gave up on the search,", "An'jou gave up on the search,",
      "An'jou hat aufgegeben,",
      "An'jou hat aufgegeben,")),
    # CAMP 252: kehrt zurueck (EN: "and returned here.")
    ('TWN_CAMP.PRG', 'TWN_CAMP_PRG',
     ("and returned here.", "and returned here.",
      "kehrt hierher.",
      "kehrt hierher.")),
    # CAMP 452: Wir koennen ihm nicht viel (EN: "We can't feed him much,")
    ('TWN_CAMP.PRG', 'TWN_CAMP_PRG',
     ("We can't feed him much,", "We can't feed him much,",
      "Wir koennen ihm nicht",
      "Wir koennen ihm nicht")),
    # CAMP 453: viel geben (EN: "but we do our best...")
    ('TWN_CAMP.PRG', 'TWN_CAMP_PRG',
     ("but we do our best...", "but we do our best...",
      "viel geben.",
      "viel geben.")),
    # CAMP 657: Kurz nach seiner Rueckkehr (EN: "Shortly after he returned,")
    ('TWN_CAMP.PRG', 'TWN_CAMP_PRG',
     ("Shortly after he returned,", "Shortly after he returned,",
      "Kurz nach seiner Rueckkehr",
      "Kurz nach seiner Rueckkehr")),

    # E022 42: Ihretwegen (EN: "for her sake as well as mine!)")
    ('TWN_E022.PRG', 'TWN_E022_PRG',
     ("for her sake as well as mine!)",
      "for her sake as well as mine!)",
      "Ihretwegen - und meinetwegen!",
      "Ihretwegen - und meinetwegen!")),
    # RUIN 108: Glaubst du (EN: "I know. Do you think")
    ('TWN_RUIN.PRG', 'TWN_RUIN_PRG',
     ("I know. Do you think", "I know. Do you think",
      "Glaubst du",
      "Glaubst du")),
    # RUIN 390: Denkst du wir haben Chancen (EN: "Do you think we stand a chance")
    ('TWN_RUIN.PRG', 'TWN_RUIN_PRG',
     ("Do you think we stand a chance", "Do you think we stand a chance",
      "Denkst du wir haben Chancen",
      "Denkst du wir haben Chancen")),
]

# group jobs by disc file (flat: fname, en_orig, de_orig, de_new, de_new)
by_file = {}
for job in JOBS:
    fname, en_t, de_t = job
    by_file.setdefault(fname, []).append((en_t, en_t, de_t, de_t))

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
        for (en_t, _de1, de_t, _de2) in pairs:
            i = 0
            en_b = en_t.encode('latin1')
            de_b = de_t.encode('latin1')
            while True:
                i = data.find(en_b, i)
                if i < 0:
                    break
                # budget
                if len(de_b) > len(en_b):
                    i += 1
                    continue
                end = i + len(en_b)
                data[i:i + len(de_b)] = de_b
                fill = i + len(de_b)
                for k in range(fill, end):
                    data[k] = 0x00 if k == fill else 0xFF
                i += 1
                touch = True
        if touch:
            write_file_regions(binp, lba, bytes(data))
            print(fname, 'disc', d, 'patched')
print('done')
