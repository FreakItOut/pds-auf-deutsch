# CD234 final sweep-2: 'How long?' (RUIN), plus CARA sanity and 'That madman'
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
            chunk = fh.read(min(DATA, need))
            if len(chunk) < min(DATA, need):
                break
            out += chunk
            need -= len(chunk)
            s += 1
    return bytes(out[:size])


NEEDLES = [('How long?', 'Wie lang?')]

by_tool = {}
for d in (1, 2, 3, 4):
    fs = '_work/fs_records_all.csv' if d == 1 else '_work/fs_records_cd%d.csv' % d
    idx = {r['name']: (int(r['lba']), int(r['size']))
           for r in csv.DictReader(open(fs, encoding='latin1'), delimiter=';')
           if int(r['lba']) > 0}
    for fname in ('TWN_RUIN.PRG', 'TWN_CAMP.PRG'):
        if fname not in idx:
            continue
        lba, size = idx[fname]
        data = read_file('_work/patched_disc%d.bin' % d, lba, size)
        for nd, de in NEEDLES:
            p = data.find(nd.encode('latin1'))
            if p < 0 or data[p - 1] == 0xFF:
                continue
            e = data.find(b'\x00', p)
            txt = data[p:e].decode('latin1')
            head = p
            while head > 0 and data[head - 1] >= 0x80:
                head -= 1
            pre = data[head:p].hex()
            by_tool.setdefault(fname.replace('.', '_'), []).append(
                '%s;%d;%s;%d;%s;%s' % (fname, head, pre, len(txt), txt, de))

for tool, rows in by_tool.items():
    with io.open('_work/menu_de/%s_de2f.csv' % tool, 'w', encoding='latin1',
                 newline='\n') as fh:
        fh.write('file;off;prefix;len;en;de\n')
        fh.write('\n'.join(rows) + '\n')
print(by_tool)
