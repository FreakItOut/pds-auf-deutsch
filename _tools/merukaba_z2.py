# MERUKABA.MCB: intro caption leftovers -> patch via a fresh menu-tool name.
import sys, csv, re
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
lba, size = idx['MERUKABA.MCB']
data = read_file('_work/patched_disc1.bin', lba, size)
rows = ['file;off;prefix;len;en;de;force']
FIX = [('  back now.', 'Sofort.'), ('back now.', 'Sofort.')]
for nd, de in FIX:
    p = data.find(nd.encode('latin1'))
    if p < 0:
        continue
    e = data.find(b'\x00', p)
    txt = data[p:e].decode('latin1')
    if len(de.encode('latin1')) > len(txt.encode('latin1')):
        print('TOO LONG', nd, len(de), len(txt))
        continue
    h = p
    while h > 0 and data[h - 1] >= 0x80:
        h -= 1
    pre = data[h:p].hex()
    rows.append('MERUKABA.MCB;%d;%s;%d;%s;%s' % (p, pre, len(txt), nd, de))
open('_work/menu_de/MERUKABA_de.csv', 'w', encoding='latin1', newline='\n') \
    .write('\n'.join(rows) + '\n')
print('rows:', len(rows) - 1)
