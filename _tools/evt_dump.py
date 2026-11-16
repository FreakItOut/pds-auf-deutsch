import io
import sys

sys.stdout.reconfigure(encoding='latin1')
lines = [l.rstrip('\r\n') for l in io.open('_work/evt_de_map.csv', encoding='latin1')
         if ';' in l]
with io.open('_work/review_fixes/evt_dump.txt', 'w', encoding='ascii',
             errors='backslashreplace', newline='\n') as out:
    for i, ln in enumerate(lines):
        en, de = ln.split(';', 1)
        out.write('%03d EN: %s\n' % (i, en))
        out.write('    DE: %s\n' % de)
print('rows=%d' % len(lines))
