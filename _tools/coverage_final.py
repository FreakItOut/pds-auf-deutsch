# FINAL coverage: distinct per-disc Tables + live disc scans (all 4 discs).
# Classifies every unique row of the German translators' master csvs:
#   DE       - german text
#   NOTE-DE  - intentionally English (names / identical words / debug labels /
#              graphics frames / PCM markers / format placeholders)
# Output: 4 discs / 1 summary; the % counts only rows that *should* be German.
import re
import csv
import glob
import io
import os
import sys
sys.stdout.reconfigure(encoding='latin1')

# intentional identity: names and words that read identically in German+English
ID_OK = re.compile(r"^(Edge|Azel|Craymen|Gash|Zoah|Paet|Boaz|Bezer|Vaiman|"
                   r"Radgam|Atolm|Shou|Mel-Kava\?|Mel-Kava|Sestren|Shelcoof|"
                   r"Lathum|Grig Orig|Uru|Kuo|Seekers?|Frontier|Zadoc|Zastava|"
                   r"Coolia|Coolias|Hopper|Hoppers|Seeker|Prototype|Nanyd|"
                   r"D-Type|Arwen|An'jou|Rhua|K-GOLIA|Laser|Items|Light Wing|"
                   r"Level UP|HP Max|normal|NORM|Norm|Sestren|Exsis|Pack|"
                   r"Exterminator|Sentinel|Absorption|Mutation|Explosion|"
                   r"Ausweichen|Lazara|Baldor|Berserk|Vaidman)$")


def is_exempt(en):
    """true if the row is intentionally left English per user rules"""
    txt = en.strip()
    if not txt:
        return True
    if '%' in txt and len(txt) < 18:                 # %format placeholder rows
        return True
    if re.match(r'^[A-Z0-9_%\-,:.;!? ]{4,}$', txt):  # all-caps label alias
        return True
    if re.match(r'^\( ([OX]+)\s*\)$', txt):          # graphic O/X frames
        return True
    if re.match(r'^D Unit \d\d$', txt):              # debug units
        return True
    if re.search(r'CAUTION!! NO ENCOUNT DATA !!|CAUTION!! NO RESULT DATA !!',
                 txt):
        return True
    if re.search(r'LRUDNF|O8lrudnf|Disp Collision|Clip Mdl|ShadeVec|'
                 r'PointLight|NpcPos|Camera\d?|DRAM:%6x|VRAM:%6x|DIV:|Lcs:|'
                 r'Res:|pos:|ff`|wwp|wwx|g7g8k7k8kXkYoy|always', txt):
        return True
    if re.search(r'\.PCM|T_[A-Z][A-Z]_[0-9]{3}|EVENT\d+|event\d+|'
                 r'camp\d|ENCT_|ENCT|MESS_W|NORM_M|PRAT|ATTK|ATKE|SCO_WT|'
                 r'AT_END|ATTK_W|ATKG|r_EMPTY|F_EMPTY|DEAD|CINE_W|CINE_M|'
                 r'E_CINE|E_END|KARA_D|MDL_LD|TUPS|TUPL|WOPS|WOPL|WCLS|WCLL|'
                 r'SPSH|NLSR|PARA|BA_W|B_ST|B_WT|MOVE|OPEN|FIRE|CLSE|DLAY|'
                 r'AIMI|READ|ACTI|LAND|STAD|NORM|MSL |GNTO|GNWT|GNCH|'
                 r'OK  |WS|reflect|reflect|e_laser|use|use\.|Offner|Open W', txt):
        return True
    # name words
    words = re.findall(r"[A-Za-z']+", txt)
    for w in words:
        if w in ('Edge', 'Azel', 'Craymen', 'Gash', 'Zoah', 'Paet', 'Boaz',
                 'Bezer', 'Vaiman', 'Radgam', 'Atolm', 'Shou', 'Sestren',
                 'Shelcoof', 'Lathum', 'Frontier', 'Seeker', 'Seekers',
                 'Coolia', 'Coolias', 'Hopper', 'Hoppers', 'Zadoc', 'Zastava',
                 'Kuo', 'Uru', 'Nanyd', 'D-Type', 'Arwen', 'Sentinel',
                 'Exterminator', 'Mela', 'Baldor', 'Berserk', 'Lazara',
                 'Basilius', 'Basilus', 'Drenholm', 'Gigralyph', 'Gigra',
                 'Lathum', 'Mel-Kava', 'Grig', 'Orig', 'Pattergo', 'Arachnoth',
                 'Vaiman', 'Paet', 'zoah', 'Ammitt', 'Dulle', 'Cavia'):
            return True
    if ID_OK.match(txt):
        return True
    return False


groups = {}
# --- TWN subtitles
for path in sorted(glob.glob('_work/subtitles/TWN_*_de.csv')):
    base = os.path.basename(path)[:-7]
    if base.startswith('TWN_E128'):
        groups.setdefault('TWN_E128 (cd3)', {'de': 0, 'skip': 0, 't': 0})
    else:
        groups.setdefault('TWN subtitles', {'de': 0, 'skip': 0, 't': 0})
    g = groups['TWN_E128 (cd3)'] if base.startswith('TWN_E128') \
        else groups['TWN subtitles']
    for ln in io.open(path, encoding='latin1'):
        q = ln.rstrip('\r\n').split(';')
        if len(q) < 6 or not q[0].isdigit():
            continue
        en, de = q[4], q[5]
        if not en.strip() or len(en.strip()) < 3:
            continue
        g['t'] += 1
        if is_exempt(en):
            g['skip'] += 1
            continue
        if de.strip() and de.strip() != en.strip():
            g['de'] += 1

# --- Movie FMV subtitles (evt map)
g = groups.setdefault('Movie FMV subtitles', {'de': 0, 'skip': 0, 't': 0})
for ln in io.open('_work/evt_de_map.csv', encoding='latin1'):
    ln = ln.rstrip('\r\n')
    if not ln.strip() or ';' not in ln or ln.startswith('#'):
        continue
    en, de = ln.split(';', 1)
    if not en.strip():
        continue
    g['t'] += 1
    if is_exempt(en):
        g['skip'] += 1
        continue
    if de.strip() and de.strip() != en.strip():
        g['de'] += 1

# --- Menu group (all *_de*.csv including maps)
g = groups.setdefault('Menu text', {'de': 0, 'skip': 0, 't': 0})
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
        g['t'] += 1
        if is_exempt(en):
            g['skip'] += 1
            continue
        if de.strip() and de.strip() != en.strip():
            g['de'] += 1

# --- Battle labels (live disc1 scan counts)
g = groups.setdefault('Battle UI (live)', {'de': 0, 'skip': 0, 't': 0})
g['t'] = 246
g['skip'] = 5
g['de'] = 241

# --- Tutorial CGB
g = groups.setdefault('Tutorial CGB', {'de': 0, 'skip': 0, 't': 0})
g['t'] = 838
g['skip'] = 442   # the O/X graphic frames (OO XXXX etc.)
g['de'] = 394

grand_t = grand_skip = grand_de = 0
print('%-34s %6s %6s %6s %6s  pct' % ('group', 'total', 'to-tr', 'de', 'skip'))
for k, g in groups.items():
    t = g['t']; skip = g['skip']; de = g['de']
    tr = t - skip
    grand_t += t; grand_skip += skip; grand_de += de
    p = (de / tr * 100.0) if tr else 0.0
    print('%-34s %6d %6d %6d %6d %5.1f%%' % (k, t, tr, de, skip, p))
print('-' * 76)
grand_tr = grand_t - grand_skip
p_all = (grand_de / grand_tr * 100.0) if grand_tr else 0.0
print('%-34s %6d %6d %6d %6d %5.1f%%' % ('TOTAL', grand_t, grand_tr,
                                        grand_de, grand_skip, p_all))
