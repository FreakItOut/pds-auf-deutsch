# verify: for every row of TWN_E022/JIRI/CAMP/RUIN, disc text == csv de, len ok
import csv

SECT, DATA = 2352, 2048

def fs_index(disc):
    fs = ('_work/fs_records_all.csv' if disc == 1 else '_work/fs_records_cd%d.csv' % disc)
    return {r['name']: (int(r['lba']), int(r['size']))
            for r in csv.DictReader(open(fs, encoding='latin1'), delimiter=';') if int(r['lba']) > 0}

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
for stem in ('TWN_E022_PRG', 'TWN_JIRI_PRG', 'TWN_CAMP_PRG', 'TWN_RUIN_PRG'):
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
                    bad_match.append((stem, d, uid, o, a, de))
                else:
                    ok += 1
                # mid-word truncation: no closing punctuation though EN had none either
                if en.rstrip().endswith(('.', '!', '?', ')')) and a and not a.rstrip().endswith(('.', '!', '?', ')')):
                    bad_trunc.append((stem, d, uid, o, 'NOCLOSE:' + a[-25:]))
print('ok=%d' % ok)
print('len violations:', len(bad_len))
for x in bad_len[:20]:
    print('  LEN %s uid=%d %d>%d %r -> %r' % x[:4] + tuple()) if False else print('  LEN %s uid=%d %d>%d %r -> %r' % x[:6])
print('mismatch:', len(bad_match))
for x in bad_match[:20]:
    print('  MM %s d%d uid=%d off=%d disc=%r csv=%r' % x)
print('trunc/no-close:', len(bad_trunc))
for x in bad_trunc[:25]:
    print('  TR %r' % (x,))
