import sys
sys.stdout.reconfigure(encoding='latin1')
p = '_work/menu_de/FLD_C4_6_MCB_map.csv'
FIX = {'So...': 'Also', '  No Entry': '  Verboten'}
lines = open(p, encoding='latin1').read().split('\n')
out = []
applied = 0
for l in lines:
    if ';' in l and l.strip():
        en, de = l.split(';', 1)
        if en in FIX:
            new = FIX[en]
            eb = en.encode('latin1')
            if len(new.encode('latin1')) <= len(eb) and de != new:
                l = en + ';' + new
                applied += 1
    out.append(l)
open(p, 'w', encoding='latin1', newline='\n').write('\n'.join(out))
print('applied', applied)
