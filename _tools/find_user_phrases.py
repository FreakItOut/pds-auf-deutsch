# live-disc grep for A) 'hepid' B) 'kehrt zurueck ist' C) 'Nicht viel zu fuette'
# D) 'Kurz nach Rueckker' E) 'fuer sie und fuer mich' F) 'Glaubst' (lonely)
# G) 'Denkst wir standen'
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


idx = {r['name']: (int(r['lba']), int(r['size']))
       for r in csv.DictReader(open('_work/fs_records_all.csv',
                                    encoding='latin1'), delimiter=';')
       if int(r['lba']) > 0}
PATTERNS = [b'hepid', b'kehrt zurueck ist', b'Nicht viel zu fuette',
            b'Kurz nach Rueckker', b'fuer sie und fuer mich',
            b'Denkst wir standen',
            b'Denkst wir haben',
            b'Glaubst', b'Glaubst du', b'kehrt zurueck']
for fname in ('TWN_E022.PRG', 'TWN_CAMP.PRG', 'TWN_RUIN.PRG',
              'TWN_JIRI.PRG', 'TWN_SEEK.PRG'):
    if fname not in idx:
        continue
    lba, size = idx[fname]
    data = read_file('_work/patched_disc1.bin', lba, size)
    for pat in PATTERNS:
        i = data.find(pat)
        if i < 0:
            continue
        s = max(0, i - 50)
        e = i + 110
        ctx = data[s:e]
        print('%-18s off=%7d pat=%s' % (fname, i, pat.decode()))
        print('  ', repr(ctx.decode('latin1', 'replace')))
