# rebuild the wiped TWN_CAMP_PRG_de.csv from batch01..26 + TWN_CAMP_PRG_en.csv
import csv
import glob
import io
import os
import sys
sys.stdout.reconfigure(encoding='latin1')

# 1. read all batch files: uid;German
batch = {}
for path in sorted(glob.glob('_work/subtitles/TWN_CAMP_PRG_de_batch[0-9][0-9].csv')):
    for ln in io.open(path, encoding='latin1'):
        q = ln.rstrip('\r\n').split(';')
        if len(q) < 2:
            continue
        try:
            uid = int(q[0])
        except Exception:
            continue
        ger = ';'.join(q[1:])
        batch[uid] = ger
print('batch entries:', len(batch))

# 2. read the EN csv and rebuild the combined file
lines = io.open('_work/subtitles/TWN_CAMP_PRG_en.csv',
                encoding='latin1').read().split('\n')
out = []
filled = 0
missing = 0
for line in lines:
    q = line.rstrip('\r\n').split(';')
    if len(q) >= 5 and q[0].isdigit():
        uid = int(q[0])
        en = q[4]
        de = batch.get(uid, '')
        if de:
            filled += 1
        else:
            missing += 1
        out.append(';'.join(q[:5]) + ';' + de)
    else:
        out.append(line)
with open('_work/subtitles/TWN_CAMP_PRG_de.csv', 'w', encoding='latin1',
          newline='\n') as f:
    f.write('\n'.join(out) + '\n')
print('rebuild: filled=%d missing=%d total=%d'
      % (filled, missing, filled + missing))
