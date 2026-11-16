# scan TWN subtitles for identity rows (de==en); classify name vs rest
import glob
import io
import os
import re
import sys
sys.stdout.reconfigure(encoding='latin1')

NAMES = set('''Edge Azel Craymen Gash Zoah Paet Boaz Bezer An'jou Rhua Vaiman
Radgam Radgam's Atolm Mel-Kava Sestren Shelcoof Lathum Grig Orig Zastava
Uru Arwen Basilius Basilus Cadegyp Former Drenholm Gigralyph Kuo VIA Pureland
Lucich Coolia Coolias Hopper Hoppers Seeker Seekers Seekers' Palm Frontier
Zadoc Vaiman 8X4 M45 4321 Proto-D-Type PDS C_v Type#1
'''.split())
NAME_WORDS = set('''Edge Azel Craymen Gash Zoah Paet Boaz Bezer Vaiman Radgam
Atolm Shou Mel-Kava Sestren Shelcoof Lathum Grig Orig Uru Kuo Seekers Frontier
Zoah Seeker Zadoc Zastava Coolia Coolias Hopper Hoppers Seeker
Prototype Nanyd D-Type Arwen An'jou Rhua K-GOLIA'''.split())

pattern = re.compile(r'^[A-Z0-9_ %\-,:;.!?]+$')
id_rows = []
for path in sorted(glob.glob('_work/subtitles/TWN_*_de.csv')):
    base = os.path.basename(path)[:-7]
    if base.startswith('TWN_E128'):
        continue
    for ln in io.open(path, encoding='latin1'):
        q = ln.rstrip('\r\n').split(';')
        if len(q) < 6 or not q[0].isdigit():
            continue
        en, de = q[4], q[5]
        if de.strip() and de.strip() == en.strip() and len(en.strip()) >= 3:
            id_rows.append((base, int(q[0]), q[2], en))
print('identity rows:', len(id_rows))
# filter out those where EN is a single NAME/token (all-caps or known)
suspects = []
for base, uid, off, en in id_rows:
    words = en.split()
    if len(words) == 1 and (words[0] in NAME_WORDS or words[0].isupper()):
        continue
    if base.endswith('PRG') and pattern.match(en) and len(en) <= 14:
        continue
    suspects.append((base, uid, off, en))
print('suspects (non-name identity):', len(suspects))
for x in suspects[:60]:
    print(' ', x)
with open('_work/review_fixes/identity_suspects.txt', 'w', encoding='latin1',
          newline='\n') as f:
    for base, uid, off, en in id_rows:
        mar = 'SUSPECT' if (base, uid, off, en) in suspects else 'NAME/OK'
        f.write('%s;%s;%s;%s;%s\n' % (base, uid, off, en, mar))
print('written _work/review_fixes/identity_suspects.txt')
