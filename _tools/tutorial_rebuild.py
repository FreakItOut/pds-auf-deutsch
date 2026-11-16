# Rebuild TUTORIAL_CGB_de.csv de-values from the patched disc (the disc holds
# the previously applied German). Rows where disc==EN keep EN (debug/unused).
import csv
import os
import sys
sys.stdout.reconfigure(encoding='latin1')
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SECT, DATA = 2352, 2048


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
       for r in csv.DictReader(open('_work/fs_records_all.csv',
                                    encoding='latin1'), delimiter=';')
       if int(r['lba']) > 0 and int(r['size']) > 0}
lba, size = idx['TUTORIAL.CGB']
patch = read_file('_work/patched_disc1.bin', lba, size)


def actual(o):
    e = o
    while e < len(patch) and patch[e] not in (0, 0xFF):
        e += 1
    return patch[o:e].decode('latin1')


# map for duplicate copies still in English on disc
m = {}
for ln in open('_work/menu_de/TUTORIAL_CGB_map.csv', encoding='latin1'):
    ln = ln.rstrip('\r\n')
    if not ln or ';' not in ln:
        continue
    en, de = ln.split(';', 1)
    if de.strip() and not en.startswith('#'):
        m.setdefault(en.strip(), de)

# First pass: collect disc DE per exact EN string (primary instance values)
disc_de = {}
src = []
for r in csv.reader(open('_work/menu_de/TUTORIAL_CGB_en.csv',
                         encoding='latin1'), delimiter=';'):
    pass
en_rows = []
for k, r in enumerate(csv.reader(open('_work/menu_de/TUTORIAL_CGB_en.csv',
                                      encoding='latin1'), delimiter=';')):
    if k == 0:
        continue
    if len(r) < 5:
        continue
    en_rows.append(r)
for r in en_rows:
    off = int(r[1])
    en = r[4]
    de = actual(off)
    if de != en and de.strip():
        disc_de.setdefault(en, de)

rows, kept_en, n = [], 0, 0
unmapped = []
for r in en_rows:
    off = int(r[1])
    en = r[4]
    de = actual(off)
    if de == en:
        # unpatched copy -> primary instance DE (same EN elsewhere) or map
        if en in disc_de:
            de_final = disc_de[en].replace('\n', '\\n')
        elif en.strip() in m:
            de_final = m[en.strip()]
        else:
            de_final = en
            kept_en += 1
            unmapped.append((off, en[:60]))
    else:
        de_final = de.replace('\n', '\\n')
    en_esc = en
    # budget sanity: de bytes (unescaped) must fit the en budget
    de_un = de_final.replace('\\n', '\n')
    en_un = en_esc.replace('\\n', '\n')
    ok = len(de_un.encode('latin1')) <= len(en_un.encode('latin1'))
    if not ok:
        print('BUDGET off=%d %r %d>%d' % (off, de_un[:40], len(de_un),
                                          len(en_un)))
    rows.append(['TUTORIAL.CGB', r[1], r[2], r[3], en_esc, de_final])

with open('_work/menu_de/TUTORIAL_CGB_de.csv', 'w', encoding='latin1',
          newline='\n') as fh:
    fh.write('file;off;prefix;len;en;de\n')
    for r in rows:
        fh.write(';'.join(r) + '\n')
print('rows=%d kept_en=%d' % (len(rows), kept_en))
import io
with io.open('_work/review_fixes/tutorial_unmapped.txt', 'w', encoding='latin1', newline='\n') as f:
    for o, e in unmapped:
        f.write('%d %s\n' % (o, e))
