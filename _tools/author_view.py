# authoring view: for theLOCAL broken uids, dump uid-3..uid+3 rows with
# uid / EN / csv-de / disc value per disc (all offsets)
import csv
import sys

sys.stdout.reconfigure(encoding='latin1')
SECT, DATA = 2352, 2048


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


def actual(data, o):
    e = o
    while e < len(data) and data[e] not in (0x00, 0xFF):
        e += 1
    return data[o:e].decode('latin1')


WANT = {
    'TWN_CAMP_PRG': [705, 706, 707, 708, 709, 750, 751, 752, 753, 754, 755],
    'TWN_RUIN_PRG': [97, 98, 99, 100, 101, 102, 107, 108, 109, 110],
    'TWN_SEEK_PRG': [52, 53, 54, 55, 486, 487, 488, 489, 490, 491, 492, 493,
                     995, 996, 997, 998, 999, 1000, 1066, 1067, 1068, 1069,
                     1070, 1071, 1124, 1125, 1126, 1127, 1128],
}
out = open('_work/review_fixes/author_view.txt', 'w', encoding='latin1',
           newline='\n')
for stem, uids in WANT.items():
    name = stem.replace('_PRG', '.PRG')
    rows = {}
    for line in open('_work/subtitles/%s_de.csv' % stem, encoding='latin1'):
        p = line.rstrip('\r\n').split(';')
        if len(p) >= 6 and p[0].isdigit():
            rows[int(p[0])] = p
    datas = {}
    for d in (1, 2, 3, 4):
        idx = fs_index(d)
        if name in idx:
            datas[d] = read_file('_work/patched_disc%d.bin' % d, *idx[name])
    out.write('===== %s =====\n' % stem)
    for u in uids:
        for k in range(u - 2, u + 3):
            r = rows.get(k)
            if not r:
                continue
            offs = [int(x) for x in r[3].split('|') if x] or [int(r[2])]
            discs = []
            for d in sorted(datas):
                vals = []
                for o in offs:
                    if o < len(datas[d]):
                        vals.append(actual(datas[d], o))
                discs.append('d%d=%r' % (d, vals))
            out.write('%s%4d en=%-40r csv=%-40r %s\n' % (
                '*' if k == u else ' ', k, r[4], r[5], ' '.join(discs)))
        out.write('\n')
out.close()
print('ok')
