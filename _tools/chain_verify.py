# final verify of chain fixes
import sys
import csv
sys.stdout.reconfigure(encoding='latin1')
SECT, DATA = 2352, 2048


def read_file(bp, lba, size):
    with open(bp, 'rb') as fh:
        out = bytearray()
        need = size
        s = lba
        while need > 0:
            fh.seek(s * SECT + 16)
            c = fh.read(min(DATA, need))
            if len(c) < min(DATA, need):
                break
            out += c
            need -= len(c)
            s += 1
    return bytes(out[:size])


CHECKS = [('TWN_CAMP.PRG', 100), ('TWN_CAMP.PRG', 101),
          ('TWN_E022.PRG', 35), ('TWN_E022.PRG', 36),
          ('TWN_RUIN.PRG', 456), ('TWN_RUIN.PRG', 457),
          ('TWN_RUIN.PRG', 526), ('TWN_RUIN.PRG', 527),
          ('TWN_SEEK.PRG', 529), ('TWN_SEEK.PRG', 530),
          ('TWN_SEEK.PRG', 595), ('TWN_SEEK.PRG', 596),
          ('TWN_SEEK.PRG', 1043), ('TWN_SEEK.PRG', 1044),
          ('TWN_SEEK.PRG', 1099), ('TWN_SEEK.PRG', 1100),
          ('TWN_SEEK.PRG', 1126), ('TWN_SEEK.PRG', 1127),
          ('TWN_SEEK.PRG', 1133), ('TWN_SEEK.PRG', 1134),
          ('TWN_SEEK.PRG', 1135), ('TWN_SEEK.PRG', 1136),
          ('TWN_SEEK.PRG', 1173), ('TWN_SEEK.PRG', 1174),
          ('TWN_SEEK.PRG', 1181), ('TWN_SEEK.PRG', 1182),
          ('TWN_SEEK.PRG', 1188), ('TWN_SEEK.PRG', 1189),
          ('TWN_SEEK.PRG', 1191), ('TWN_SEEK.PRG', 1192),
          ('TWN_SEEK.PRG', 1193), ('TWN_SEEK.PRG', 1195),
          ('TWN_SEEK.PRG', 1196), ('TWN_SEEK.PRG', 1068),
          ('TWN_SEEK.PRG', 1069), ('TWN_SEEK.PRG', 1074),
          ('TWN_SEEK.PRG', 1075), ('TWN_SEEK.PRG', 1087),
          ('TWN_SEEK.PRG', 1088), ('TWN_SEEK.PRG', 1137),
          ('TWN_SEEK.PRG', 1138)]
for fn in set(x[0] for x in CHECKS):
    stem = fn.replace('.PRG', '_PRG')
    path = '_work/subtitles/%s_de.csv' % stem
    if not open(path, encoding='latin1'):
        pass

for d in (1, 2, 3, 4):
    print('--- disc', d, '---')
    for fn_stem, uid in CHECKS:
        fn = fn_stem.replace(' ', '')
        stem = fn.replace('.PRG', '_PRG')
        fs = ('_work/fs_records_all.csv' if d == 1
              else '_work/fs_records_cd%d.csv' % d)
        idx = {r['name']: (int(r['lba']), int(r['size']))
               for r in csv.DictReader(open(fs, encoding='latin1'), delimiter=';')
               if int(r['lba']) > 0}
        if fn not in idx:
            print('  %s missing on disc%d' % (fn, d))
            continue
        dd = read_file('_work/patched_disc%d.bin' % d, *idx[fn])
        ents = None
        for ln in open('_work/subtitles/%s_de.csv' % stem, encoding='latin1'):
            p = ln.rstrip().split(';')
            if len(p) >= 6 and p[0] == str(uid):
                ents = p
                break
        if not ents:
            continue
        o = int(ents[3].split('|')[0]) if ents[3] else int(ents[2])
        e = dd.find(b'\x00', o)
        print('  uid %d: %r' % (uid, dd[o:e].decode('latin1', 'replace')))
