# fix remaining: CAMP 685/686 (multiple copies) and RUIN 527 (multi copies)
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


fixes = [
    ('TWN_CAMP.PRG', [
        (101114, "If master An'jou doesn't return,",
         'Wenn Anjou nicht zurueck,'),
        (101217, "If master An'jou doesn't return,",
         'Wenn Anjou nicht zurueck,'),
        (101147, "we're in trouble.", 'haben wir Pech.'),
        (101250, "we're in trouble.", 'haben wir Pech.'),
    ]),
    ('TWN_RUIN.PRG', [
        (89768, 'she gained human emotions.', 'gewann sie Emotionen.'),
        (90034, 'she gained human emotions.', 'gewann sie Emotionen.'),
        (90234, 'she gained human emotions.', 'gewann sie Emotionen.'),
        (90499, 'she gained human emotions.', 'gewann sie Emotionen.'),
        (90690, 'she gained human emotions.', 'gewann sie Emotionen.'),
    ]),
]
for fname, pairs in fixes:
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
        data = bytearray(read_file('_work/patched_disc%d.bin' % d, lba, size))
        for off, en_t, de_t in pairs:
            en_b = en_t.encode('latin1')
            de_b = de_t.encode('latin1')
            if len(de_b) > len(en_b):
                continue
            end = off + len(en_b)
            data[off:off + len(de_b)] = de_b
            fill = off + len(de_b)
            for k in range(fill, end):
                data[k] = 0x00 if k == fill else 0xFF
        write_file_regions('_work/patched_disc%d.bin' % d, lba, bytes(data))
print('done')

# sync CSV
CAMP = {685: 'Wenn Anjou nicht zurueck,', 686: 'haben wir Pech.'}
RUIN = {527: 'gewann sie Emotionen.'}
for stem, umap in (('TWN_CAMP_PRG', CAMP), ('TWN_RUIN_PRG', RUIN)):
    p = '_work/subtitles/%s_de.csv' % stem
    lines = open(p, encoding='latin1').read().split('\n')
    out = []
    for line in lines:
        q = line.rstrip('\r\n').split(';')
        if len(q) >= 6 and q[0].isdigit() and int(q[0]) in umap:
            q[5] = umap[int(q[0])]
            line = ';'.join(q)
        out.append(line)
    open(p, 'w', encoding='latin1', newline='\n').write('\n'.join(out))
