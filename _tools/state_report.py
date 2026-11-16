# final honest coverage: count distinct TWN rows with DE differs from EN.
# also count rows where DE='EN' (untranslated name/identity cases).
import glob
import io
import os
import re
import sys
sys.stdout.reconfigure(encoding='latin1')

grand_t = grand_german = grand_same = 0
print('%-34s %7s %7s %7s' % ('group', 'rows', 'DE', 'same'))
for path in sorted(glob.glob('_work/subtitles/TWN_*_de.csv')):
    base = os.path.basename(path)[:-7]
    if base.startswith('TWN_E128'):
        continue
    g = (0, 0, 0)
    tot_d = tot_g = tot_s = 0
    for ln in io.open(path, encoding='latin1'):
        q = ln.rstrip('\r\n').split(';')
        if len(q) < 6 or not q[0].isdigit():
            continue
        en, de = q[4].strip(), q[5].strip()
        if not en:
            continue
        tot_d += 1
        if de and de != en:
            tot_g += 1
        elif de == en:
            tot_s += 1
    g = (tot_d, tot_g, tot_s)
    grand_t += tot_d; grand_german += tot_g; grand_same += tot_s
    print('%-34s %7d %7d %7d' % (base[:34], tot_d, tot_g, tot_s))
print('%-34s %7d %7d %7d' % ('TWN TOTAL', grand_t, grand_german, grand_same))
