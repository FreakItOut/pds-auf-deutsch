# Safety: check EVERY DE row (any source file) for length violations against
# its own EN column (independent of the EN csv coverage).
import csv
import glob
import os
import sys

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def unesc(s):
    return s.replace('\\n', '\n')


bad = 0
for path in sorted(glob.glob('_work/menu_de/*_de*.csv')):
    if path.endswith('_en.csv'):
        continue
    with open(path, encoding='latin1') as fh:
        rd = csv.reader(fh, delimiter=';')
        next(rd)
        for r in rd:
            if len(r) < 6:
                continue
            en, de = unesc(r[4]), unesc(r[5])
            if len(de.encode('latin1')) > len(en.encode('latin1')):
                print('LEN VIOLATION %s off=%s %d/%d' % (
                    os.path.basename(path), r[1],
                    len(de.encode('latin1')), len(en.encode('latin1'))))
                print('   en=%r' % r[4][:70])
                print('   de=%r' % r[5][:70])
                bad += 1
            for line in de.split('\n'):
                if len(line) > 34:
                    print('WIDE LINE %s off=%s %d %r' % (
                        os.path.basename(path), r[1], len(line), line[:40]))
                    bad += 1
            try:
                de.encode('ascii')
            except UnicodeEncodeError:
                print('NON-ASCII %s off=%s' % (os.path.basename(path), r[1]))
                bad += 1
print('total violations:', bad)

# generate map templates for the remaining files
todo_files = ['TUTORIAL_CGB', 'FLD_A5_MCB', 'FLD_A7_FNT', 'FLD_A3_MCB',
              'FLD_B6_MCB', 'FLD_C4_6_MCB', 'FLD_B5_FNT', 'FLD_C2_FNT',
              'FLD_C4_FNT', 'FLD_B2_FNT', 'FLD_D2_FNT', 'FLD_D3_FNT',
              'FLD_D5_FNT', 'TWN_SEEK_PRG', 'TWN_CARA_PRG', 'TWN_E006_PRG',
              'TWN_E011_PRG', 'TWN_E014_PRG', 'TWN_E021_PRG', 'TWN_EXCA_PRG']
for name in todo_files:
    src = f'_work/menu_de/{name}_en.csv'
    if not os.path.exists(src):
        continue
    seen = set()
    out = f'_work/menu_de/{name}_map_todo.csv'
    with open(src, encoding='latin1') as fh, \
            open(out, 'w', encoding='latin1', newline='') as fo:
        rd = csv.reader(fh, delimiter=';')
        next(rd)
        for r in rd:
            if len(r) >= 5 and r[4].strip() not in seen:
                seen.add(r[4].strip())
                fo.write('%s;\n' % r[4])
    print('%-16s unique=%d -> %s' % (name, len(seen), out))
