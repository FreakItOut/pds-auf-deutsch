# chains dump with prev/next context (3 rows before / 3 after)
import csv, glob, io, os, sys
sys.stdout.reconfigure(encoding='latin1')

rows_by = {}
for path in sorted(glob.glob('_work/subtitles/TWN_*_de.csv')):
    base = os.path.basename(path)[:-7]
    if base.startswith('TWN_E128'):
        continue
    rows = []
    for ln in io.open(path, encoding='latin1'):
        q = ln.rstrip('\r\n').split(';')
        if len(q) >= 6 and q[0].isdigit():
            rows.append({'uid': int(q[0]), 'off': int(q[2].split('|')[0]),
                         'en': q[4], 'de': q[5]})
    rows.sort(key=lambda r: r['off'])
    for i in range(len(rows) - 1):
        a, b = rows[i], rows[i + 1]
        ctx_before = rows[max(0, i-2):i]
        ctx_after = rows[i+2:i+4]
        en1, en2 = a['en'], b['en']
        # only treat as a real chain if EN1 doesn't end terminal and EN2 starts lowercase or separator
        if len(en1) < 3 or len(en2) < 3:
            continue
        chainlike = (
            (en1.endswith((',', ':', '-', ';')) or
             en1.split()[-1].islower() if en1.split() else False) and
            en2 and en2[0].islower() or
            en1 and en1.split()[-1].islower() and en2 and en2[0].islower()
        ) if en1.split() else False
        if chainlike and len(en1) > 4 and len(en2) > 4:
            chains = []
            rows_by.setdefault(base, [])
            rows_by[base].append((i, rows))
            continue
        # also if EN1 ends '.' but DE1 doesn't and DE2 begins lowercase
        # (a rare false flag) - skip
with open('_work/review_fixes/chain_context.txt', 'w',
          encoding='latin1', newline='\n') as f:
    for base, lst in sorted(rows_by.items()):
        for i, rows in lst:
            a, b = rows[i], rows[i+1]
            rows_before = rows[max(0, i-2):i]
            rows_after = rows[i+2:i+4]
            f.write('==== %s  %d + %d ====\n' % (base, a['uid'], b['uid']))
            for r in rows_before:
                f.write('  prev(%d): %r / %r\n' % (r['uid'], r['en'], r['de']))
            f.write('  A(%d): %r / %r\n' % (a['uid'], a['en'], a['de']))
            f.write('  B(%d): %r / %r\n' % (b['uid'], b['en'], b['de']))
            for r in rows_after:
                f.write('  next(%d): %r / %r\n' % (r['uid'], r['en'], r['de']))
            f.write('\n')
print('written _work/review_fixes/chain_context.txt')
