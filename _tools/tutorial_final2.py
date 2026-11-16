import sys
sys.stdout.reconfigure(encoding='latin1')
FIX = {
    55432: 'denn ihm?',
    67708: 'Hab ich Unrecht gesagt?',
    64910: '(Wollte er wirklich',
}
lines = open('_work/menu_de/TUTORIAL_CGB_de.csv', encoding='latin1').read().split('\n')
n = 0
for i, l in enumerate(lines):
    q = l.split(';')
    if len(q) >= 6 and q[1].isdigit() and int(q[1]) in FIX:
        en = q[4].replace('\\n', '\n')
        de = FIX[int(q[1])]
        if len(de.encode('latin1')) <= len(en.encode('latin1')) and \
                q[5].replace('\\n', '\n') != de:
            q[5] = de.replace('\n', '\\n')
            lines[i] = ';'.join(q)
            n += 1
open('_work/menu_de/TUTORIAL_CGB_de.csv', 'w', encoding='latin1', newline='\n').write('\n'.join(lines) + '\n')
print('updated', n)
