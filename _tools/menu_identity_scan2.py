# menu identity scan v2: drop format strings and debug labels
import csv
import glob
import io
import os
import re
import sys
sys.stdout.reconfigure(encoding='latin1')

suspects = []
tot_ident = 0
for path in sorted(glob.glob('_work/menu_de/*_de*.csv')):
    base = os.path.basename(path)
    if base.endswith('_en.csv'):
        continue
    f = io.open(path, encoding='latin1')
    rd = csv.reader(f, delimiter=';')
    header = next(rd, None)
    if not header or header[0] != 'file':
        f.close()
        f = io.open(path, encoding='latin1')
        rd = csv.reader(f, delimiter=';')
    for r in rd:
        if len(r) < 6:
            continue
        en, de = r[4], r[5]
        if not en or not en.strip() or len(en.strip()) < 4:
            continue
        if de.strip() != en.strip():
            continue
        # skip any format-string / debug row
        if '%' in en:
            continue
        # skip all-caps / mostly caps label families
        if re.match(r'^[A-Z0-9_ %\-,:;.!?]+$', en):
            continue
        # skip short lowercase internal tags like camp1/camp2
        if re.match(r'^[a-z0-9_]+$', en):
            continue
        # skip engine debug tags: LRUDNF etc.
        if re.search(r'(lrudnf|O8lrudnf|LRUDNF|g7g8|k7k8|kXk|Yoy|e_4|pos:|'
                     r'Res:|Lcs:|DRAM:|DIV:|VRAM:|Disp Collision|Clip Mdl|'
                     r'ShadeVec|PointLight|NpcPos|Camera\d?|ONE |TWO |THR |'
                     r'FOU |LOW |STD |LNG |SKY |DRV |LCS |PAUSE|STOCK)', en):
            continue
        # skip PCM/track markers
        if re.search(r'\.PCM|_PCM|T_[A-Z]{2}_', en):
            continue
        # identical-in-both-words stays (Laser etc.)
        if en.strip() in ('Laser', 'Items', 'Light Wing', 'Level UP',
                          'Laser', 'HP Max', 'normal'):
            continue
        tot_ident += 1
        suspects.append((base, r[1], en))
print('suspects:', tot_ident)
for x in suspects[:120]:
    print(' ', x)
with open('_work/review_fixes/menu_identity_suspects_v2.txt', 'w',
          encoding='latin1', newline='\n') as f:
    f.write('file;off;en\n')
    for base, off, en in suspects:
        f.write('%s;%s;%s\n' % (base, off, en))
print('written _work/review_fixes/menu_identity_suspects_v2.txt')
