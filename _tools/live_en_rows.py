# Build extra de-rows for the remaining disc-1 English slots located live on
# the patched disc (offset-exact, non-force). Rows appended as *_de_z2.csv so
# menu_text_tool --rpatch receives them without touching the map flows.
import csv
import re
import sys
sys.stdout.reconfigure(encoding='latin1')

SECT = 2352
DATA = 2048


def read_file(binpath, lba, size):
    with open(binpath, 'rb') as fh:
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


idx = {r['name']: (int(r['lba']), int(r['size']))
       for r in csv.DictReader(open('_work/fs_records_all.csv', encoding='latin1'),
                               delimiter=';') if int(r['lba']) > 0}


def slot_bounds(data, pos):
    # embedded control-code prefix (bytes >= 0x80, incl \xff runs) or plain NUL-gap
    s = pos
    back = 0
    while s - back > 0 and data[s - back - 1] >= 0x80:
        back += 1
    has_ff = back > 0 and data[s - 1] == 0xFF
    s2 = s - back
    return s2, has_ff


def esc(t):
    return t.replace('\\', '\\\\').replace('\n', '\\n')


JOBS = [
    # (fsfile, tool-name, [(needle, de)])
    ('CHILDMP.MCB', 'CHILDMP_MCB', [('  YES   NO', 'JA    NEIN')]),
    ('FLD_A3.MCB', 'FLD_A3_MCB',
     [('(Imperial piece of crap.)', '(Kaiserlicher Mist!)')]),
    ('FLD_B6.MCB', 'FLD_B6_MCB', [
        ('The Institute, which considered>', '<Das Institut, das ueberlegte>'),
        ('regarding the Light Wing...>', '<zu den Lichtfluegeln...>'),
        ('record and seal all data>', '<alle Daten sichern>'),
        ('regarding the Light Wing>', '<zum Lichtfluegel>'),
        ('them throughout the continent...>', '<sie am ganzen Kontinent...>'),
        ('But it is more than a dragon,>', '<Doch: mehr als ein Drache,>'),
    ]),
    ('FLD_A7.FNT', 'FLD_A7_FNT', [
        ("The dragon's forms can be",
         'Die Drachenformen lassen\nsich in fuenf %c6Typen%c0\nunterteilen. Je nach Typ\nveraendern sich Faehigkeiten\nund das Lernen neuer\nBerserk-Techniken.'),
        ('But, the armor will slow',
         'Aber die Ruestung bremst\ndeinen Drachen aus.'),
    ]),
    ('MENU.SCB', 'MENU_SCB', [
        ('From upper floors to outer 13F',
         "Von den oberen Etagen\nnach aussen: 13.OG ->\nmit Aufzug: 13 to. 12.OG\n-> zum oberen Hangar\n\nVom oberen Hangar\nnach aussen: 11.OG ->\nmit Aufzug: 11 to. 9.OG\n-> zu den mittleren\nEtagen"),
        ('From middle floors to outer 8F',
         "Von den mittleren Etagen\nnach aussen: 8.OG ->\nmit Aufzug: 8 to. 6.OG\n-> zum unteren Hangar\n\nVom unteren Hangar\nnach aussen: 5.OG ->\nmit Aufzug: 5 to. 4.OG\n-> zu den unteren\nEtagen"),
    ]),
]

rows_by_name = {}
for fsname, toolname, items in JOBS:
    lba, size = idx[fsname]
    data = read_file('_work/patched_disc1.bin', lba, size)
    rows = []
    for needle_text, de in items:
        nd = needle_text.encode('latin1')
        m = re.search(re.escape(nd), data)
        if not m:
            rows.append(('MISS', fsname, needle_text, de))
            continue
        pos = m.start()
        start = slot_bounds(data, pos)[0] if False else None
        # decide prefix: everything from slot-start to pos (controls or '<')
        s = pos
        prev = None
        while s > 0 and data[s] not in (0, 0xFF) is False:
            break
        # use a simple split for '<' openers (Menu/B6) and ff-runs (A7/MENU)
        head = 0
        if data[pos - 1] == 0x3C:  # '<'
            head = 1
        if data[max(0, pos - 1)] >= 0x80:
            h = pos
            while h > 0 and data[h - 1] >= 0x80:
                h -= 1
            head = pos - h
        e = data.find(b'\x00', pos)
        full = data[pos:e]
        prefix_bytes = data[pos - head:pos]
        en_text = bytes(full).decode('latin1')
        eb = len(en_text.encode('latin1'))
        db = len(de.encode('latin1'))
        flag = 'OK' if db <= eb else 'TOOLONG %d>%d' % (db, eb)
        rows.append(('ROW', fsname, toolname, pos, prefix_bytes.hex(), en_text, de, flag))
    rows_by_name[toolname] = rows

for name, rows in rows_by_name.items():
    ok = [r for r in rows if r[0] == 'ROW' and r[7].startswith('OK')]
    bad = [r for r in rows if r[0] != 'ROW' or not r[7].startswith('OK')]
    path = '_work/menu_de/%s_de_z2.csv' % name
    with open(path, 'w', encoding='latin1', newline='\n') as fh:
        fh.write('file;off;prefix;len;en;de;force\n')
        for r in ok:
            _, fsname, _t, pos, pre, en, de, _f = r
            fh.write('%s;%d;%s;%d;%s;%s\n' % (fsname, pos, pre,
                                              len(en.encode('latin1')),
                                              esc(en), esc(de)))
    print(name, 'written', len(ok), 'bad', len(bad))
    for b in bad:
        print('   BAD', b[1] if b[0] == 'ROW' else b[1], b[3] if b[0] == 'ROW' else b[2], b[7] if b[0] == 'ROW' else '')
