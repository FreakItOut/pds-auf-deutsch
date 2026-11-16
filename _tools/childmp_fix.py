# CHILDMP_MCB_map fixes + rebuild + patch
import csv
import os
import subprocess
import sys

PY = r'C:\Users\FreakItOut\AppData\Local\Programs\Python\Python312\python.exe'

FIX = {
    'A bony tail from the Golia.': 'Knocheniger Golia-Schwanz',
    'RUN': 'FLI',
    'Aronak Unit': 'Aronak Ein.',
    'Lindstrum Unit': 'Lindstrum Ein.',
    'Not Use': 'Unben.',
    'DRAGON ARM WING': 'DRACHEN ARM GR.',
    'DRAGON EYE WING': 'DRACH AUGEN GR.',
    'DRAGON LIGHT WING': 'DRACH LICHT GR.',
    'DRAGON PANZER WING': 'DRACH PANZER GR.',
    'DRAGON SOLO WING': 'DRACH SOLO GR.',
    'DRAGON STRIPE WING': 'DRACH STREIF GR.',
    'DRAGON VALIANT WING': 'DRACH TAPFER GR.',
}

path = '_work/menu_de/CHILDMP_MCB_map.csv'
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
                p[1] = new
                line = ';'.join(p)
                applied += 1
            else:
                bad.append((k, len(new), len(en)))
    out.append(line)
open(path, 'w', encoding='latin1', newline='\n').write('\n'.join(out))
print('applied', applied, 'bad', bad)

for n in ('CHILDMP_MCB',):
    subprocess.run([PY, '_tools/expand_menu_map.py', n], check=True)
    r = subprocess.run([PY, '_tools/menu_text_tool.py', '--validate', n], capture_output=True, text=True)
    print(r.stdout.strip()[:400])
