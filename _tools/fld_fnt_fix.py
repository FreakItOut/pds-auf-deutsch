# FLD_A7_FNT_map (FLD FNT union) fixes + rebuild + validate
import subprocess

PY = r'C:\Users\FreakItOut\AppData\Local\Programs\Python\Python312\python.exe'

FIX = {
    'MAP': 'KARTE',
    'PAL CHANGE': 'PAL-WECHS.',
    'WAIT': 'WART',
    'ALL LOAD !': 'ALLE LADEN',
    'A:LOAD, B:NOT LOAD, C:ALL LOAD': 'A:LADEN, B:NICHT, C:ALLES',
    'A:SAVE, B:NOT SAVE': 'A:SPEICH., B:NICHT',
    'FREE': 'FREI',
    'HIGH SCORE CLEAR': 'REKORDE LOESCHEN',
    'MOVE': 'ZUG',
    'NO DATA!!': 'KEINE!!',
    'NO USE': 'LEER',
    'RESTART BOX GAME': 'SPIEL NEUSTART',
    'X: dragon camera': 'X: Drachenkamera',
}

path = '_work/menu_de/FLD_A7_FNT_map.csv'
lines = open(path, encoding='latin1').read().split('\n')
out = []
applied = 0
bad = []
for line in lines:
    if ';' in line and line.strip():
        p = line.split(';', 1)
        en, de = p[0], p[1]
        k = en.strip()
        if k in FIX:
            new = FIX[k]
            if len(new.encode('latin1')) <= len(en.encode('latin1')):
                if de != new:
                    p[1] = new
                    line = ';'.join(p)
                    applied += 1
            else:
                bad.append((k, len(new), len(en)))
    out.append(line)
open(path, 'w', encoding='latin1', newline='\n').write('\n'.join(out))
print('applied', applied, 'bad', bad)

for n in ('FLD_A7_FNT', 'FLD_B2_FNT', 'FLD_B5_FNT', 'FLD_C2_FNT', 'FLD_C4_FNT',
          'FLD_D2_FNT', 'FLD_D3_FNT', 'FLD_D5_FNT'):
    subprocess.run([PY, '_tools/expand_menu_map.py', n, '_work/menu_de/FLD_A7_FNT_map.csv'],
                   check=False, capture_output=True, text=True)
    r = subprocess.run([PY, '_tools/menu_text_tool.py', '--validate', n],
                       capture_output=True, text=True)
    print(r.stdout.strip().splitlines()[0] if r.stdout else '(no stdout)')
