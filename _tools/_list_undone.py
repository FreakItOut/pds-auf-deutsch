# what is actually NOT German in the menu group (per the honest classify)
import csv
import glob
import io
import sys
sys.stdout.reconfigure(encoding='latin1')
ID_OK = None  # local simpler


def exempt(en):
    words = set()
    import re
    m = re.search(r"\(.*", en)
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
    NAMES = ('Edge Azel Craymen Gash Zoah Paet Boaz Bezer Vaiman Radgam Atolm '
             'Shou Sestren Shelcoof Lathum Grig-Orig Uru Kuo Seeker Seekers '
             'Coolia Coolias Hopper Hoppers Zadoc Zastava Nanyd D-Type Arwen '
             'Sentinel Exterminator Baldor Berserk Lazara Mel-Kava').split()
    if txt in NAMES or ID_OK:
        pass
    # match without complex regex: word-by-word
    toks = [x for x in txt.split()]
    for t in toks:
        if t in NAMES:
            return True
    return False

seen = set()
for path in sorted(glob.glob('_work/menu_de/*_de*.csv')):
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
        if de.strip() and de.strip() != en.strip():
            continue
        if en in seen:
            continue
        seen.add(en)
        print('%r' % en[:90])
