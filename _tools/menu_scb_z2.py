# manual write of the two MENU.SCB extra rows (fits exact budgets)
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
lba, size = idx['MENU.SCB']
data = read_file('_work/patched_disc1.bin', lba, size)

DE = {
    'From upper floors to outer 13F':
        "Von oben nach aussen:\n13.OG -> mit Aufzug\nzu 12.OG -> oberer\nHangar\n\nVom oberen Hangar\nnach aussen: 11.OG ->\nmit Aufzug zu 9.OG\n-> mittlere Etagen",
    'From middle floors to outer 8F':
        "Von der Mitte nach\naussen: 8.OG -> mit\nAufzug zu 6.OG ->\nunterer Hangar\n\nVom unteren Hangar\nnach aussen: 5.OG ->\nmit Aufzug zu 4.OG\n-> untere Etagen",
}


def esc(t):
    return t.replace('\\', '\\\\').replace('\n', '\\n')


rows = ['file;off;prefix;len;en;de;force']
for nd, de in DE.items():
    p = data.find(nd.encode('latin1'))
    e = data.find(b'\x00', p)
    txt = data[p:e].decode('latin1')
    assert len(de.encode('latin1')) <= len(txt.encode('latin1')), (nd, len(de), len(txt))
    # prefix: ff-run before the text
    h = p
    while h > 0 and data[h - 1] >= 0x80:
        h -= 1
    pre = data[h:p].hex()
    rows.append('MENU.SCB;%d;%s;%d;%s;%s' % (p, pre, len(txt), esc(txt), esc(de)))
open('_work/menu_de/MENU_SCB_de_z2.csv', 'w', encoding='latin1', newline='\n') \
    .write('\n'.join(rows) + '\n')
print('rows written:', len(rows) - 1)
