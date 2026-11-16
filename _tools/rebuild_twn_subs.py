# rebuild ALL TWN subtitle csvs from their EN csv + batch01..N files
import glob
import io
import os
import sys
sys.stdout.reconfigure(encoding='latin1')

for stem in ('TWN_CAMP_PRG', 'TWN_RUIN_PRG', 'TWN_JIRI_PRG',
             'TWN_E022_PRG', 'TWN_SEEK_PRG'):
    batch = {}
    for p in sorted(glob.glob('_work/subtitles/%s_de_batch*.csv' % stem)):
        for ln in io.open(p, encoding='latin1'):
            q = ln.rstrip('\r\n').split(';')
            if len(q) < 2 or not q[0].isdigit():
                continue
            try:
                uid = int(q[0])
            except Exception:
                continue
            ger = ';'.join(q[1:])
            batch[uid] = ger
    en_path = '_work/subtitles/%s_en.csv' % stem
    if not os.path.exists(en_path):
        print(stem, 'no en csv, skip')
        continue
    lines = io.open(en_path, encoding='latin1').read().split('\n')
    out = []
    filled = missed = 0
    for line in lines:
        q = line.rstrip('\r\n').split(';')
        if len(q) >= 5 and q[0].isdigit():
            uid = int(q[0])
            de = batch.get(uid, '')
            if de:
                filled += 1
            else:
                missed += 1
            out.append(';'.join(q[:5]) + ';' + de)
        else:
            out.append(line)
    with open('_work/subtitles/%s_de.csv' % stem, 'w', encoding='latin1',
              newline='\n') as f:
        f.write('\n'.join(out) + '\n')
    print(stem, 'rebuilt', filled, 'missing', missed)
