# find how the Spanish tool patched subtitles - look for "patch", "replace",
# "in-place", "length", "budget", "srt", "psubtitles" references
import io
import os
import glob
import re
import sys
sys.stdout.reconfigure(encoding='latin1')
P = 'C:/Users/FreakItOut/Downloads/pds-tools-master/pds-tools-master/'
for path in sorted(glob.glob(P + 'tools/*.py') + glob.glob(P + 'tools/common/*.py')):
    fname = os.path.basename(path)
    data = io.open(path, encoding='latin1').read()
    hits = []
    for line_num, line in enumerate(data.split('\n'), 1):
        ll = line.lower()
        if any(k in ll for k in ('patch', 'in-place', 'in_place', 'length-lim',
                                 'length limit', 'budget', 'srt->', 'max-len',
                                 'maxlen', 'es_pds', 'spanish', 'english',
                                 'too long', 'truncat')):
            hits.append((line_num, line.strip()[:120]))
    if hits:
        print('===', fname, '(%d hits)' % len(hits))
        for n, h in hits[:10]:
            print('  %3d: %s' % (n, h))
