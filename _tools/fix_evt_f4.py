# Fix a single fmv line: 'we're a band of tomb raiders.'
# -> 'Wir sind Grabraeuber.'  und erneutes Patchen aller Discs.
import io
import subprocess
import sys

sys.stdout.reconfigure(encoding='latin1')
MAP = '_work/evt_de_map.csv'
KEY = "we're a band of tomb raiders."
NEW = 'Wir sind Grabraeuber.'

lines = io.open(MAP, encoding='latin1').read().split('\n')
hit = 0
out = []
for ln in lines:
    q = ln.rstrip('\r\n')
    if q.startswith(KEY + ';'):
        out.append(KEY + ';' + NEW)
        hit += 1
    else:
        out.append(ln)
if hit != 1:
    print('WARNUNG: %d Treffer' % hit)
else:
    io.open(MAP, 'w', encoding='latin1', newline='').write(
        '\n'.join(out))
    print('map aktualisiert (%s -> %s)' % (KEY, NEW))
    r = subprocess.run([sys.executable,
                        '_tools/patch_evt_subtitles.py',
                        '--disc', 'all', '--csv', MAP])
    print('patch rc=%d' % r.returncode)
