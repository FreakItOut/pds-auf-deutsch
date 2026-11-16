# write BOTH copies of CAMP 108/109 and RUIN 110 at all 4 discs; same German
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


FIX = {
    ('TWN_CAMP.PRG', 'TWN_CAMP_PRG'): {
        108: ('He looks busy,', 'Er wirkt beschaeftigt,'),
        109: ('gutting the monster...)', 'erschlaegt Monster.)'),
        685: ("If master An'jou doesn't return,",
              "Wenn Anjou nicht zurueck,"),
        686: ("we're in trouble.", 'haben wir Pech.'),
    },
    ('TWN_RUIN.PRG', 'TWN_RUIN_PRG'): {
        110: ("I'll go look for her right now.",
              'Ich gehe jetzt nach ihr suchen.'),
    },
}
for (fkey, csv_stem), umap in FIX.items():
    for d in (1, 2, 3, 4):
        fs = ('_work/fs_records_all.csv' if d == 1
              else '_work/fs_records_cd%d.csv' % d)
        idx = {r['name']: (int(r['lba']), int(r['size']))
               for r in csv.DictReader(open(fs, encoding='latin1'),
                                       delimiter=';')
               if int(r['lba']) > 0}
        if fkey not in idx:
            continue
        lba, size = idx[fkey]
        data = bytearray(read_file('_work/patched_disc%d.bin' % d, lba, size))
        rows = []
        for ln in open('_work/subtitles/%s_de.csv' % csv_stem,
                       encoding='latin1'):
            q = ln.rstrip('\r\n').split(';')
            if len(q) >= 6 and q[0].isdigit():
                rows.append((int(q[0]), q))
        rmap = dict(rows)
        touch = False
        for u, (en_t, de_t) in umap.items():
            ea = rmap.get(u)
            if not ea:
                continue
            offs = [int(x) for x in ea[3].split('|') if x] or [int(ea[2])]
            for o in offs:
                if o >= len(data):
                    continue
                en_b = en_t.encode('latin1')
                de_b = de_t.encode('latin1')
                end = min(o + len(en_b), len(data))
                data[o:o + len(de_b)] = de_b
                fill = o + len(de_b)
                for k in range(fill, end):
                    data[k] = 0x00 if k == fill else 0xFF
                touch = True
        if touch:
            write_file_regions('_work/patched_disc%d.bin' % d, lba,
                               bytes(data))
            print('disc', d, fkey, 'patched')
