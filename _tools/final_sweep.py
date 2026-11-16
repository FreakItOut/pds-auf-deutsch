# final sweep patch for remaining shared visible labels: Level UP / Buy Item / Sell Item
import csv
import io
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
            c = fh.read(min(DATA, need))
            if len(c) < min(DATA, need):
                break
            out += c
            need -= len(c)
            s += 1
    return bytes(out[:size])


idx = {r['name']: (int(r['lba']), int(r['size']))
       for r in csv.DictReader(open('_work/fs_records_all.csv', encoding='latin1'),
                               delimiter=';') if int(r['lba']) > 0}

NEEDLES = [
    ('Level UP', 'STUFE +1'),
    ('Buy Item', 'Kaufen'),
    ('Sell Item', 'Verkauf'),
]

by_name = {}
for fname in sorted(idx):
    if not re.match(r'^(BTL_|FLD_|TWN_|CHILDMP|MENU|MERU)', fname):
        continue
    lba, size = idx[fname]
    data = read_file('_work/patched_disc1.bin', lba, size)
    rows = []
    for nd, de in NEEDLES:
        for m in re.finditer(re.escape(nd.encode('latin1')), data):
            p = m.start()
            e = data.find(b'\x00', p)
            if e < 0 or e - p > 60:
                continue
            txt = data[p:e].decode('latin1')
            # only patch the bare label slots (Level UP / Buy Item / Sell Item)
            if nd == 'Level UP' and txt.strip() != 'Level UP':
                continue
            if nd != 'Level UP' and txt.strip() != nd:
                continue
            head = p
            while head > 0 and data[head - 1] >= 0x80:
                head -= 1
            pre = data[head:p].hex()
            if len(de.encode('latin1')) > len(txt.encode('latin1')):
                continue
            rows.append('%s;%d;%s;%d;%s;%s' % (fname, head, pre, len(txt), txt, de))
    if rows:
        tool = fname.replace('.', '_')
        by_name.setdefault(tool, []).extend(rows)

for tool, rows in by_name.items():
    with io.open('_work/menu_de/%s_de2d.csv' % tool, 'w', encoding='latin1',
                 newline='\n') as fh:
        fh.write('file;off;prefix;len;en;de\n')
        fh.write('\n'.join(rows) + '\n')
print('files:', len(by_name), 'rows:', sum(len(v) for v in by_name.values()))
for t, r in sorted(by_name.items()):
    print(' ', t, len(r))
