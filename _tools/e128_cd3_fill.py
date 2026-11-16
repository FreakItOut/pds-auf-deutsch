# fill TWN_E128_cd3_de.csv from the final menu_de/TWN_E128_de.csv by EN key
import csv
import io
import re
import sys
sys.stdout.reconfigure(encoding='latin1')

pool = {}
for ln in io.open('_work/menu_de/TWN_E128_de.csv', encoding='latin1'):
    q = ln.rstrip('\r\n').split(';')
    if len(q) >= 6 and q[4]:
        pool[q[4]] = q[5]

path = '_work/subtitles/TWN_E128_cd3_de.csv'
lines = io.open(path, encoding='latin1').read().split('\n')
done = miss = 0
out = []
for line in lines:
    q = line.rstrip('\r\n').split(';')
    if len(q) >= 6 and q[0].isdigit() and not q[5].strip():
        en = q[4]
        de = pool.get(en)
        if de is not None and de.strip():
            q[5] = de
            done += 1
            line = ';'.join(q)
        else:
            # strip-based key second attempt
            key = en.strip()
            for k, v in pool.items():
                if k.strip() == key and v.strip():
                    q[5] = v
                    done += 1
                    line = ';'.join(q)
                    break
            else:
                miss += 1
    out.append(line)
io.open(path, 'w', encoding='latin1', newline='\n').write('\n'.join(out))
print('filled:', done, 'missing:', miss)
