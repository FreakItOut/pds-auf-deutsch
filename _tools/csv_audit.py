# csv integrity: rows per stem, malformed lines (field count != 6), empty de,
# and any ROW whose uid is skipped for verification
import glob
import sys

sys.stdout.reconfigure(encoding='latin1')
for path in sorted(glob.glob('_work/subtitles/TWN_*_PRG_de.csv')):
    lines = open(path, encoding='latin1').read().split('\n')
    rows = [l for l in lines if l.strip()]
    bad = []
    uids = []
    for l in rows:
        q = l.split(';')
        if len(q) != 6 or not q[0].lstrip('-').isdigit():
            if len(q) != 6:
                bad.append((len(q), q))
        elif q[0].isdigit():
            uids.append(int(q[0]))
            if not q[5]:
                bad.append(('EMPTY-DE', q[:6]))
    dup = len(uids) - len(set(uids))
    miss = [u for u in range(min(uids), max(uids) + 1) if u not in set(uids)]
    print(path.split('/')[-1].split('\\')[-1],
          'rows=%d' % len(uids),
          'dupes=%d' % dup,
          'uid_gaps=%d' % len(miss),
          'malformed=%d' % len(bad))
    for b in bad[:6]:
        print('   BAD', b)
