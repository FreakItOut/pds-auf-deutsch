# final live-scan patch for control-prefixed labels (e.g. \x06\x07+ATTACK CLASS)
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
    ('AMP__ATTACK', r'ATTACK CLASS    '),
    ('TEMP', r'The reactor temperature is rising\.'),
    ('BLAST', r'Blast it out of the sky!'),
    ('POS', r'Move to attack positions!'),
]


def esc(t):
    return t.replace('\n', '\\n')


rows_out = []
for fname in sorted(idx):
    if not fname.startswith('BTL_'):
        continue
    lba, size = idx[fname]
    data = read_file('_work/patched_disc1.bin', lba, size)
    for tag, pat in NEEDLES:
        m = re.search(pat.encode('latin1'), data)
        if not m:
            continue
        p = m.start()
        # control-prefix: bytes >= 0x20 not part of ASCII text; we take bytes backwards
        # while they form \x06/\x07-style markers
        h = p
        while h > 0 and data[h - 1] >= 0x80:
            h -= 1
        # also catch \x06\x07 runs (they're < 0x80; walk back over them)
        while h > 2 and data[h - 1] == 0x07 and data[h - 2] == 0x06:
            h -= 2
        # keep walking over interleaved 6/7+byte runs
        pre_b = data[h:p]
        en = m.group(0).decode('latin1')
        toolname = fname.replace('.', '_')
        outp = '_work/menu_de/%s_de2c.csv' % toolname
        if tag == 'TEMP':
            de = 'Der Reaktor heizt auf!'
        elif tag == 'BLAST':
            de = 'Vom Himmel holen!'
        elif tag == 'POS':
            de = 'Angriffsstellen!'
        else:
            de = 'KAMPF-KLASSE    ' if en.strip() == 'ATTACK CLASS' else en
        if len(de.encode('latin1')) > len(en.encode('latin1')):
            print('TOO LONG', fname, tag, len(de), len(en))
            continue
        rows_out.append('%s;%d;%s;%d;%s;%s' % (fname, p, pre_b.hex(), len(en), esc(en), de))

# write as one meta part per tool name
by_name = {}
for r in rows_out:
    fn = r.split(';', 1)[0]
    toolname = fn.replace('.', '_')
    by_name.setdefault(toolname, []).append(r)
for toolname, rows in by_name.items():
    with io.open('_work/menu_de/%s_de2c.csv' % toolname, 'w', encoding='latin1',
                 newline='\n') as fh:
        fh.write('file;off;prefix;len;en;de\n')
        fh.write('\n'.join(rows) + '\n')
print('rows:', len(rows_out))
