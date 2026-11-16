# extract the non-exempt non-de menu rows for review
import csv
import glob
import io
import os
import re
import sys
sys.stdout.reconfigure(encoding='latin1')

# replicate is_exempt from coverage_final.py
ID_OK = re.compile(r"^(Edge|Azel|Craymen|Gash|Zoah|Paet|Boaz|Bezer|Vaiman|"
                   r"Radgam|Atolm|Shou|Mel-Kava\?|Mel-Kava|Sestren|Shelcoof|"
                   r"Lathum|Grig Orig|Uru|Kuo|Seekers?|Frontier|Zadoc|Zastava|"
                   r"Coolia|Coolias|Hopper|Hoppers|Seeker|Prototype|Nanyd|"
                   r"D-Type|Arwen|An'jou|Rhua|K-GOLIA|Laser|Items|Light Wing|"
                   r"Level UP|HP Max|normal|NORM|Norm|Sestren|Exsis|Pack|"
                   r"Exterminator|Sentinel|Absorption|Mutation|Explosion|"
                   r"Ausweichen|Lazara|Baldor|Berserk|Vaidman)$")


def is_exempt(en):
    txt = en.strip()
    if not txt:
        return True
    if '%' in txt and len(txt) < 18:
        return True
    if re.match(r'^[A-Z0-9_%\-,:.;!? ]{4,}$', txt):
        return True
    if re.match(r'^\( ([OX]+)\s*\)$', txt):
        return True
    if re.match(r'^D Unit \d\d$', txt):
        return True
    if re.search(r'CAUTION!! NO ENCOUNT DATA !!|CAUTION!! NO RESULT DATA !!',
                 txt):
        return True
    if re.search(r'LRUDNF|O8lrudnf|Disp Collision|Clip Mdl|ShadeVec|'
                 r'PointLight|NpcPos|Camera\d?|DRAM:%6x|VRAM:%6x|DIV:|Lcs:|'
                 r'Res:|pos:|ff`|wwp|wwx|g7g8k7k8kXkYoy', txt):
        return True
    if re.search(r'\.PCM|T_[A-Z][A-Z]_[0-9]{3}|EVENT\d+|event\d+|'
                 r'camp\d|ENCT_|ENCT|MESS_W|NORM_M|PRAT|ATTK|ATKE|SCO_WT|'
                 r'AT_END|ATTK_W|ATKG|r_EMPTY|F_EMPTY|DEAD|CINE_W|CINE_M|'
                 r'E_CINE|E_END|KARA_D|MDL_LD|TUPS|TUPL|WOPS|WOPL|WCLS|WCLL|'
                 r'SPSH|NLSR|PARA|BA_W|B_ST|B_WT|MOVE|OPEN|FIRE|CLSE|DLAY|'
                 r'AIMI|READ|ACTI|LAND|STAD|NORM|MSL |GNTO|GNWT|GNCH|'
                 r'OK  |OFF|WAIT|free run|score rank|dot rate', txt):
        return True
    words = re.findall(r"[A-Za-z']+", txt)
    for w in words:
        if w in ('Edge', 'Azel', 'Craymen', 'Gash', 'Zoah', 'Paet', 'Boaz',
                 'Bezer', 'Vaiman', 'Radgam', 'Atolm', 'Shou', 'Sestren',
                 'Shelcoof', 'Lathum', 'Frontier', 'Seeker', 'Seekers',
                 'Coolia', 'Coolias', 'Hopper', 'Hoppers', 'Zadoc', 'Zastava',
                 'Kuo', 'Uru', 'Nanyd', 'D-Type', 'Arwen', 'Sentinel',
                 'Exterminator', 'Mela', 'Baldor', 'Berserk', 'Lazara',
                 'Basilius', 'Basilus', 'Drenholm', 'Gigralyph', 'Gigra',
                 'Mel-Kava', 'Grig', 'Orig', 'Pattergo', 'Arachnoth'):
            return True
    if ID_OK.match(txt):
        return True
    return False


suspects = set()
for path in sorted(glob.glob('_work/menu_de/*_de*.csv')):
    base = os.path.basename(path)
    if base.endswith('_en.csv'):
        continue
    f = io.open(path, encoding='latin1')
    rd = csv.reader(f, delimiter=';')
    header = next(rd, None)
    if not header or header[0] != 'file':
        f.close()
        continue
    for r in rd:
        if len(r) < 6:
            continue
        en, de = r[4], r[5]
        if not en.strip() or len(en.strip()) < 4:
            continue
        if de.strip() and de.strip() != en.strip():
            continue          # already German
        if is_exempt(en):
            continue
        suspects.add(en)
print('unique non-exempt non-de rows:', len(suspects))
ordered = sorted(suspects)
with open('_work/review_fixes/remaining_final.txt', 'w', encoding='latin1',
          newline='\n') as fh:
    for x in ordered:
        fh.write('%s\n' % x)
for x in ordered:
    print('  %r' % x[:90])
