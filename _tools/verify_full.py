# FULL verify dump, no truncation: all len/mismatch entries + csv+disc texts
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


bad_trunc, bad_len, bad_match, ok = [], [], [], 0
for stem in ('TWN_E022_PRG', 'TWN_JIRI_PRG', 'TWN_CAMP_PRG',
             'TWN_RUIN_PRG', 'TWN_SEEK_PRG'):
    name = stem.replace('_PRG', '.PRG')
    datas = {}
    for d in (1, 2, 3, 4):
        idx = fs_index(d)
        if name in idx:
            lba, size = idx[name]
            datas[d] = read_file('_work/patched_disc%d.bin' % d, lba, size)
    for line in open('_work/subtitles/%s_de.csv' % stem, encoding='latin1'):
        p = line.rstrip('\r\n').split(';')
        if len(p) < 6:
            continue
        uid, en, de = int(p[0]), p[4], p[5]
        offs = [int(x) for x in p[3].split('|') if x] or [int(p[2])]
        if len(de) > len(en):
            bad_len.append((stem, uid, len(de), len(en), en, de))
        for d, data in datas.items():
            for o in offs:
                if o >= len(data):
                    bad_trunc.append((stem, d, uid, o, 'OOB'))
                    continue
                a = actual(data, o)
                if a != de:
                    bad_match.append((stem, d, uid, o, a, de, en))
                else:
                    ok += 1
                if en.rstrip().endswith(('.', '!', '?', ')')) and a and \
                        not a.rstrip().endswith(('.', '!', '?', ')')):
                    bad_trunc.append((stem, d, uid, o, 'NOCLOSE:' + a[-25:]))

with open('_work/review_fixes/broken_all.txt', 'w', encoding='latin1',
          newline='\n') as f:
    f.write('=== LEN ===\n')
    for x in bad_len:
        f.write('LEN %s uid=%d %d>%d en=%r de=%r\n' % x)
    f.write('=== MISMATCH ===\n')
    for x in bad_match:
        f.write('MM %s d%d uid=%d off=%d disc=%r csv=%r en=%r\n' % x)
    f.write('=== NOCLOSE (unique per stem,uid) ===\n')
    seen = set()
    for x in bad_trunc:
        k = (x[0], x[2])
        if 'NOCLOSE' not in str(x[4]) or k in seen:
            continue
        seen.add(k)
        f.write('TR %s uid=%d %s\n' % (x[0], x[2], x[4]))

print('ok=%d len=%d mm=%d tr_groups=%d' % (ok, len(bad_len),
      len(bad_match), len(seen)))
print('written _work/review_fixes/broken_all.txt')

# context dump for every uid named in LEN or MM: u -2..u+2 with csv texts
need_uids = {}
for stem, u, *_ in [(x[0], x[1]) for x in bad_len + bad_match]:
    need_uids.setdefault(stem, set()).add(u)
f = open('_work/review_fixes/broken_ctx.txt', 'w', encoding='latin1',
         newline='\n')
for stem, us in sorted(need_uids.items()):
    rows = {}
    for line in open('_work/subtitles/%s_de.csv' % stem, encoding='latin1'):
        p = line.rstrip('\r\n').split(';')
        if len(p) >= 6 and p[0].isdigit():
            rows[int(p[0])] = p
    f.write('===== %s =====\n' % stem)
    for u in sorted(us):
        for k in range(u - 2, u + 3):
            r = rows.get(k)
            if not r:
                continue
            f.write('  %s%3d en=%-42r de=%r\n' % ('*' if k == u else ' ',
                                                  k, r[4], r[5]))
f.close()
print('ctx written')
