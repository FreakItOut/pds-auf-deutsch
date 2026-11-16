# tr_ctx.py - dump uid-2..uid+2 (en + de + disc-actual) for every NOCLOSE uid
import csv
import io
import re
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


bau = io.open('_work/review_fixes/broken_all.txt', encoding='latin1').read()
tr = [(m.group(1), int(m.group(2)), m.group(3))
      for m in re.finditer(r"TR (\S+) uid=(\d+) NOCLOSE:(.*)", bau)]
groups = {}
for s, u, tail in tr:
    groups.setdefault(s, []).append(u)

out = io.open('_work/review_fixes/tr_ctx.txt', 'w', encoding='latin1',
              newline='\n')
for stem, uids in sorted(groups.items()):
    name = stem.replace('_PRG', '.PRG')
    rows = {}
    for line in io.open('_work/subtitles/%s_de.csv' % stem,
                        encoding='latin1'):
        p = line.rstrip('\r\n').split(';')
        if len(p) >= 6 and p[0].isdigit():
            rows[int(p[0])] = p
    datas = {}
    for d in (1, 2, 3, 4):
        idx = fs_index(d)
        if name in idx:
            datas[d] = read_file('_work/patched_disc%d.bin' % d, *idx[name])
    out.write('===== %s (%d groups) =====\n' % (stem, len(uids)))
    d1vals = {}
    for u in uids:
        r = rows.get(u)
        if not r:
            continue
        offs = [int(x) for x in r[3].split('|') if x] or [int(r[2])]
        d1vals[u] = actual(datas[1], offs[0])
    for u in uids:
        if u not in rows:
            continue
        for k in range(u - 2, u + 3):
            r = rows.get(k)
            if not r:
                continue
            disc = d1vals.get(k, '')
            out.write('%s%4d en=%-40r de=%-40r disc=%r\n' % (
                '*' if k == u else ' ', k, r[4], r[5], disc))
        out.write('\n')
out.close()
print('groups:', sum(len(v) for v in groups.values()))
