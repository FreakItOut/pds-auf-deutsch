# Validate + patch the menu-block translations (MENU.SCB, MENUEN.FNT,
# TUTORIAL.CGB, CHILDMP.MCB, FLD_*, TWN residues).
#
# DE csv format (in _work/menu_de/<NAME>_de*.csv):
#   file;off;prefix;len;en;de[;force]   (\n escaped as literal \n)
# Validation: completeness vs EN csv, len(de) <= len(en) in bytes,
# every de line <= 34 bytes, ASCII only, no stray backslashes.
#
# Patch mode: --patch rewrites strings in all 4 patched discs in place
# (chunk = prefix + en + NUL... -> prefix + de + NUL + 0xFF padding up to
# the original chunk length), then readback-verifies every written offset.
# Rows with force=1 overwrite at their offset unconditionally (for chunks
# corrupted by earlier patch phases).
import csv
import os
import sys

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SECT = 2352
DATA = 2048
MAXLINE = 34


def unesc(s):
    return s.replace('\\n', '\n')


def load_de(name):
    """Load all _work/menu_de/<name>_de*.csv part files."""
    import glob as _g
    rows = []
    for path in sorted(_g.glob(f'_work/menu_de/{name}_de*.csv')):
        with open(path, encoding='latin1') as fh:
            rd = csv.reader(fh, delimiter=';')
            next(rd)
            for r in rd:
                if len(r) >= 6:
                    rows.append({'file': r[0], 'off': int(r[1]), 'prefix': r[2],
                                 'en_len': int(r[3]), 'en': r[4], 'de': r[5],
                                 'force': len(r) >= 7 and r[6] == '1'})
    return rows


def validate(name):
    enp = f'_work/menu_de/{name}_en.csv'
    enrows = {}
    with open(enp, encoding='latin1') as fh:
        rd = csv.reader(fh, delimiter=';')
        next(rd)
        for r in rd:
            enrows[int(r[1])] = r[4]
    derows = {}
    for d in load_de(name):
        derows[d['off']] = d
    probs = []
    for off, en in enrows.items():
        if off not in derows:
            probs.append(('MISSING-DE', off, en[:40]))
            continue
        d = derows[off]
        if d['en'] != en:
            probs.append(('EN-MISMATCH', off, en[:40]))
        de = unesc(d['de'])
        en_u = unesc(en)
        if len(de.encode('latin1')) > len(en_u.encode('latin1')):
            probs.append(('TOO-LONG', off, '%d/%d %r' % (
                len(de.encode('latin1')), len(en_u.encode('latin1')), de[:50])))
        # line width: no DE line wider than the widest EN line of the same
        # string (single-line EN strings may legitimately be up to ~40)
        en_lines = en_u.split('\n')
        limit = max([len(l) for l in en_lines] + [1])
        for line in de.split('\n'):
            if len(line) > limit:
                probs.append(('LINE>%d' % limit, off,
                              '%d %r' % (len(line), line)))
        try:
            de.encode('ascii')
        except UnicodeEncodeError:
            probs.append(('NON-ASCII', off, d['de'][:40]))
        resid = d['de'].replace('\\n', '')
        if '\\' in resid:
            probs.append(('STRAY-BACKSLASH', off, d['de'][:50]))
    for off, d in derows.items():
        if not d.get('force'):
            continue
        de = unesc(d['de'])
        en_u = unesc(d['en'])
        if len(de.encode('latin1')) > len(en_u.encode('latin1')):
            probs.append(('TOO-LONG-FORCE', off, '%d/%d' % (
                len(de.encode('latin1')), len(en_u.encode('latin1')))))
    print('%-16s en=%d de=%d problems=%d' % (name, len(enrows), len(derows),
                                             len(probs)))
    for p in probs[:40]:
        print('   ', p)
    return len(probs)


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


def write_file_regions(binpath, lba, filedata):
    with open(binpath, 'r+b') as fh:
        for k in range((len(filedata) + DATA - 1) // DATA):
            sector = lba + k
            fh.seek(sector * SECT + 16)
            fh.write(filedata[k * DATA:(k + 1) * DATA])


def fs_index(disc):
    fs = ('_work/fs_records_all.csv' if disc == 1
          else f'_work/fs_records_cd{disc}.csv')
    idx = {}
    for r in csv.DictReader(open(fs, encoding='latin1'), delimiter=';'):
        if int(r['lba']) > 0 and int(r['size']) > 0:
            idx[r['name']] = (int(r['lba']), int(r['size']))
    return idx


def patch(name):
    rows = load_de(name)
    for d in (1, 2, 3, 4):
        idx = fs_index(d)
        fsname = rows[0]['file'] if rows else name.replace('_', '.')
        if fsname not in idx:
            print('disc %d: %s not present, skipped' % (d, fsname))
            continue
        lba, size = idx[fsname]
        binp = f'_work/patched_disc{d}.bin'
        data = bytearray(read_file(binp, lba, size))
        written = []  # (verify_off, prefix, de_b)
        applied = skipped = 0
        for r in rows:
            off = r['off']
            prefix = bytes.fromhex(r['prefix']) if r['prefix'] else b''
            en_b = unesc(r['en']).encode('latin1')
            de_b = unesc(r['de']).encode('latin1')
            old = prefix + en_b
            if r.get('force'):
                end = off + len(old)
                data[off:off + len(prefix) + len(de_b)] = prefix + de_b
                for i in range(off + len(prefix) + len(de_b), end + 1):
                    data[i] = (0x00 if i == off + len(prefix) + len(de_b)
                               else 0xFF)
                written.append((off, prefix, de_b))
                applied += 1
                continue
            cur_off = off
            if len(prefix) + len(de_b) > len(prefix) + len(en_b):
                skipped += 1  # safety: never write longer than the original
                continue
            if bytes(data[cur_off:cur_off + len(old)]) != old:
                alt = data.find(old + b'\x00')
                if alt < 0:
                    skipped += 1
                    continue
                cur_off = alt
            new = prefix + de_b
            end = cur_off + len(old)
            data[cur_off:cur_off + len(new)] = new
            for i in range(cur_off + len(new), end + 1):
                data[i] = 0x00 if i == cur_off + len(new) else 0xFF
            written.append((cur_off, prefix, de_b))
            applied += 1
        write_file_regions(binp, lba, bytes(data))
        chk = read_file(binp, lba, size)
        mism = sum(1 for off, prefix, de_b in written
                   if chk[off:off + len(prefix) + len(de_b)]
                   != prefix + de_b)
        print('disc %d %-12s applied=%d skipped=%d readback-mismatch=%d' % (
            d, name, applied, skipped, mism))


if __name__ == '__main__':
    if len(sys.argv) >= 3 and sys.argv[1] == '--patch':
        patch(sys.argv[2])
    elif len(sys.argv) >= 3 and sys.argv[1] == '--validate':
        validate(sys.argv[2])
    else:
        names = ['MENU_SCB', 'MENUEN_FNT', 'TUTORIAL_CGB', 'CHILDMP_MCB',
                 'FLD_A5_MCB', 'FLD_A7_FNT']
        total = 0
        for n in names:
            if os.path.exists(f'_work/menu_de/{n}_en.csv'):
                total += validate(n)
        print('TOTAL problems:', total)
