# probe CD4 CARA remaining 7 items + disc3/4 Quit Game occurrences
import csv
import re
import sys
sys.stdout.reconfigure(encoding='latin1')

SECT, DATA = 2352, 2048


def read_file(bp, lba, size):
    with open(bp, 'rb') as fh:
        out = bytearray()
        need = size
        s = lba
        while need > 0:
            fh.seek(s * SECT + 16)
            chunk = fh.read(min(DATA, need))
            if len(chunk) < min(DATA, need):
                break
            out += chunk
            need -= len(chunk)
            s += 1
    return bytes(out[:size])


for d, f, show_first in ((4, 'TWN_CARA.PRG', 12), (3, 'TWN_CAMP.PRG', 3),
                         (4, 'TWN_CAMP.PRG', 3)):
    fs = '_work/fs_records_cd%d.csv' % d
    idx = {r['name']: (int(r['lba']), int(r['size']))
           for r in csv.DictReader(open(fs, encoding='latin1'), delimiter=';')
           if int(r['lba']) > 0}
    lba, size = idx[f]
    data = read_file('_work/patched_disc%d.bin' % d, lba, size)
    print('===== disc%d %s' % (d, f))
    EN_WORDS = set('the you and your your item items of it s its all gone from'
                   ' a is that was were be with and that for my me him she her they him'
                   ' no what was where now all my their my these were will not so'.split())
    seen = {}
    n = 0
    for part in data.split(b'\x00'):
        if len(part) < 8 or len(part) > 240:
            continue
        txt = part.decode('latin1', 'replace')
        words = re.findall(r"[a-z']+", txt.lower())
        if not words:
            continue
        en = sum(1 for w in words if w in EN_WORDS)
        if en < 3 or ' ' not in txt.strip():
            continue
        if txt in seen:
            continue
        seen[txt] = True
        o = data.find(txt.encode('latin1'))
        n += 1
        if n > show_first:
            continue
        print('  off=%d len=%d %r' % (o, len(txt), txt[:110]))
