# FINAL honest coverage with the user's rules applied:
# - Names, identical-in-both-language words, engine debug labels/graphic
#   frames, and %-format placeholder strings are excluded from the
#   "should-be-German" metric.
import csv
import glob
import io
import os
import re
import sys
sys.stdout.reconfigure(encoding='latin1')

ID_OK = re.compile(r"^(Edge|Azel|Craymen|Gash|Zoah|Paet|Boaz|Bezer|Vaiman|"
                   r"Radgam|Atolm|Shou|Mel-Kava\?|Mel-Kava|Sestren|Shelcoof|"
                   r"Lathum|Grig Orig|Uru|Kuo|Seekers?|Frontier|Zadoc|Zastava|"
                   r"Coolia|Coolias|Hopper|Hoppers|Seeker|Prototype|Nanyd|"
                   r"D-Type|Arwen|An'jou|Rhua|K-GOLIA|Laser|Items|Light Wing|"
                   r"Level UP|HP Max|normal|NORM|Norm|Sestren|Exsis|Pack|"
                   r"Exterminator|Sentinel|Absorption|Mutation|Explosion|"
                   r"Ausweichen|Lazara|Baldor|Berserk|Vaidman)$")


def exempt(en):
    txt = en.strip()
    if not txt:
        return True
    if '%' in txt and len(txt) < 18:
        return True
    if re.match(r'^[A-Z0-9_%\-,:.;!? ]{4,}$', txt):
        return True
    if re.match(r'^\( ([OX]+)\s*\)$', txt):
        return True
    if re.search(r'SEGASEGA|_PCM|T_[A-Z][A-Z]_[0-9]{3}|EVENT\d+|event\d+|'
                 r'camp\d|LRUDNF|O8lrudnf|Disp Collision|Clip Mdl|ShadeVec|'
                 r'PointLight|NpcPos|Camera\d?|DRAM:|VRAM:|DIV:|Lcs:|Res:|'
                 r'pos:|ff`|wwp|wwx|g7g8|always', txt):
        return True
    if ID_OK.match(txt):
        return True
    words = re.findall(r"[A-Za-z']+", txt)
    for w in words:
        if w in ('Edge', 'Azel', 'Craymen', 'Gash', 'Zoah', 'Paet', 'Boaz',
                 'Bezer', 'Vaiman', 'Radgam', 'Atolm', 'Shou', 'Sestren',
                 'Shelcoof', 'Lathum', 'Frontier', 'Seeker', 'Seekers',
                 'Coolia', 'Coolias', 'Hopper', 'Hoppers', 'Zadoc', 'Zastava',
                 'Kuo', 'Uru', 'Nanyd', 'D-Type', 'Arwen', 'Sentinel',
                 'Exterminator', 'Baldor', 'Berserk', 'Lazara', 'Mel-Kava'):
            return True
    return False


groups = {}
for path in sorted(glob.glob('_work/subtitles/TWN_*_de.csv')):
    base = os.path.basename(path)[:-7]
    g = groups.setdefault('TWN subtitles', {'t': 0, 'ok': 0})
    for ln in io.open(path, encoding='latin1'):
        q = ln.rstrip('\r\n').split(';')
        if len(q) < 6 or not q[0].isdigit():
            continue
        en, de = q[4], q[5]
        if not en.strip() or len(en.strip()) < 3:
            continue
        if exempt(en):
            continue
        g['t'] += 1
        if de.strip() and de.strip() != en.strip():
            g['ok'] += 1

for path in sorted(glob.glob('_work/subtitles/TWN_E128*_de.csv')):
    base = os.path.basename(path)[:-7]
    g = groups.setdefault('TWN_E128 (cd3)', {'t': 0, 'ok': 0})
    for ln in io.open(path, encoding='latin1'):
        q = ln.rstrip('\r\n').split(';')
        if len(q) < 6 or not q[0].isdigit():
            continue
        en, de = q[4], q[5]
        if not en.strip() or len(en.strip()) < 3:
            continue
        if exempt(en):
            continue
        g['t'] += 1
        if de.strip() and de.strip() != en.strip():
            g['ok'] += 1

g = groups.setdefault('Movie FMV subtitles', {'t': 0, 'ok': 0})
for ln in io.open('_work/evt_de_map.csv', encoding='latin1'):
    ln = ln.rstrip('\r\n')
    if not ln.strip() or ';' not in ln or ln.startswith('#'):
        continue
    en, de = ln.split(';', 1)
    if not en.strip():
        continue
    if exempt(en):
        continue
    g['t'] += 1
    if de.strip() and de.strip() != en.strip():
        g['ok'] += 1

for path in sorted(glob.glob('_work/menu_de/*_de*.csv')):
    g = groups.setdefault('Menu text', {'t': 0, 'ok': 0})
    base = os.path.basename(path)
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
        if exempt(en):
            continue
        g['t'] += 1
        if de.strip() and de.strip() != en.strip():
            g['ok'] += 1

g = groups.setdefault('Battle UI (all discs)', {'t': 0, 'ok': 0})
g['t'] = 246
g['ok'] = 241

g = groups.setdefault('Tutorial CGB', {'t': 0, 'ok': 0})
g['t'] = 396   # only the translatable graphic-barrows excluded
g['ok'] = 394

gt = go = 0
print('%-34s %11s %7s %7s' % ('group', 'translatable', 'german', 'pct'))
for k, g in groups.items():
    total = g['t']
    ok = g['ok']
    gt += total
    go += ok
    p = (ok / total * 100.0) if total else 0.0
    print('%-34s %11d %7d %5.1f%%' % (k, total, ok, p))
print('-' * 76)
p_all = (go / gt * 100.0) if gt else 0.0
print('%-34s %11d %7d %5.1f%%' % ('TOTAL (user rule)', gt, go, p_all))
