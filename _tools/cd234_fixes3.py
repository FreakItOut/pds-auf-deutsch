# cd234_fixes3: CARA/an-object shops + Switch Sell/Buy + Training beenden
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


NEEDLES = [
    ('(An object from the Ancient Age...', '(...Ein Objekt aus der Vorzeit.'),
    ('(The bridge was destroyed...', '(...)Die Bruecke zerstoert.'),
    ('Exit the Excavation Site', 'Verlasse Ausgrabungsort'),
    ("Don't Ende", 'Bleib hier'),
    ('Switch Sell/Buy', 'Kauf/Verkauf'),
    ('Will Training beenden', 'Training beenden!'),
]

by_tool = {}
for d in (1, 2, 3, 4):
    fs = '_work/fs_records_all.csv' if d == 1 else '_work/fs_records_cd%d.csv' % d
    idx = {r['name']: (int(r['lba']), int(r['size']))
           for r in csv.DictReader(open(fs, encoding='latin1'), delimiter=';')
           if int(r['lba']) > 0}
    for fname in sorted(idx):
        if not re.match(r'^(BTL_|FLD_|TWN_|CHILDMP|MENU|MERU)', fname):
            continue
        lba, size = idx[fname]
        data = read_file('_work/patched_disc%d.bin' % d, lba, size)
        rows = []
        for nd, de in NEEDLES:
            for m in list(re.finditer(re.escape(nd.encode('latin1')), data))[:8]:
                p = m.start()
                e = data.find(b'\x00', p)
                if e < 0 or e - p > 60:
                    continue
                txt = data[p:e].decode('latin1')
                if txt.strip() != nd:
                    continue
                if len(de.encode('latin1')) > len(txt.encode('latin1')):
                    continue
                head = p
                while head > 0 and data[head - 1] >= 0x80:
                    head -= 1
                pre = data[head:p].hex()
                rows.append('%s;%d;%s;%d;%s;%s' % (fname, head, pre, len(txt), txt, de))
        if rows:
            by_tool.setdefault(fname.replace('.', '_'), []).extend(rows)

for tool, rows in by_tool.items():
    outp = '_work/menu_de/%s_de2g.csv' % tool
    with io.open(outp, 'w', encoding='latin1', newline='\n') as fh:
        fh.write('file;off;prefix;len;en;de\n')
        fh.write('\n'.join(rows) + '\n')
print('files:', len(by_tool), 'rows:', sum(len(v) for v in by_tool.values()))
for t, r in sorted(by_tool.items()):
    print(' ', t, len(r))
