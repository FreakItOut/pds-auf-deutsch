import sys
sys.stdout.reconfigure(encoding='latin1')
p = '_work/menu_de/TUTORIAL_CGB_map.csv'
FIX = {
    "Hey, think about what you're doing!": 'Hey, denk mal, was du da tust!',
    'still have any life left in them.': 'steckt noch Leben in ihnen.',
    'the ancient ones. Would any God': 'der Alten. Wuerde ein Gott',
}
lines = open(p, encoding='latin1').read().split('\n')
out, applied = [], 0
for l in lines:
    if ';' in l and l.strip():
        en, de = l.split(';', 1)
        if en in FIX and len(FIX[en].encode('latin1')) <= len(en.encode('latin1')) and de != FIX[en]:
            l = en + ';' + FIX[en]
            applied += 1
    out.append(l)
open(p, 'w', encoding='latin1', newline='\n').write('\n'.join(out))
print('applied', applied)
