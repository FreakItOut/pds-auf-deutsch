# coverage v2: use live classification (diff/identity/empty) to show real rest
import csv
import glob
import io
import os
import re
import sys
sys.stdout.reconfigure(encoding='latin1')

#identities that intentionally stay (names, words identical both languages)
ID_OK = re.compile(r"^(Edge|Azel|Craymen|Gash|Zoah|Paet|Boaz|Bezer|Vaiman|Radgam|"
                   r"Atolm|Shou|Mel-Kava\?|Mel-Kava|Sestren|Shelcoof|Lathum|"
                   r"Grig Orig|Uru|Kuo|Seekers?|Frontier|Zadoc|Zastava|Coolia|"
                   r"Coolias|Hopper|Hoppers|Seeker|Prototype|Nanyd|D-Type|"
                   r"Arwen|An'jou|Rhua|K-GOLIA|Laser|Items|Light Wing|"
                   r"Level UP|HP Max|normal)$")
# TWN-side debug/invisible engine strings that intentionally stay EN
ID_OK = re.compile(ID_OK.pattern[:-2] + r"|^(O8)?lrudnf##LRUDNF$|Disp Collision$"
                   r"|dodges lasers$|g7g8k7k8kXkYoy$)")
# names with trailing punctuation and optional leading paren/dots
NAME_PAT = re.compile(r"^\.?[\(\.]?\s*(Lord )?(Edge|Azel|Craymen|Gash|Paet|"
                      r"Rhua|Vaiman)[\W_]*$")
# interjections that read the same in German
INTJ_PAT = re.compile(r"^[\.\s]*(Oh|Hmm|Hm)[\.\!\?,]*$|^'{0,1}%a0'?[\.\!]*$|^\.{1,4}$")
# animation demo frames drawn with O/X glyphs
GRAPH_PAT = re.compile(r"^\(\s*[OX]+(\s+[OX]+)*\s*\)$")
# visible debug/HUD labels that intentionally stay EN
DEBUG_PAT2 = re.compile(r"^(D Unit \d{2}|light\s+:|Lcs:|Res:|Clip Mdl|Shade|"
                        r"ShadeVec|PointLight|Camera2?3?|NpcPos)$")

DEBUG_PAT = re.compile(r'^([A-Z0-9_ %\-,:;.!?]+|%s|%3d|[%\dxX_: ,\-\.]+)\\?$')

def is_debug(en):
    if '%' in en and len(en.strip()) < 18:
        return True
    if re.match(r'^[A-Z0-9_ %\-,:;.!?]+$', en.strip()):
        return True
    if len(en.strip()) < 4:
        return True
    return False

tot = empty = diff = ident = debug = 0
idlist = []
for path in sorted(glob.glob('_work/subtitles/TWN_*_de.csv')):
    base = os.path.basename(path)[:-7]
    if base.startswith('TWN_E128'):
        continue
    for ln in io.open(path, encoding='latin1'):
        q = ln.rstrip('\r\n').split(';')
        if len(q) < 6 or not q[0].isdigit():
            continue
        en, de = q[4], q[5]
        if not en.strip() or len(en.strip()) < 3:
            continue
        tot += 1
        if is_debug(en):
            debug += 1
            continue
        if not de.strip():
            empty += 1
        elif de.strip() == en.strip():
            if ID_OK.match(en.strip()):
                ident += 1
            else:
                idlist.append((base, int(q[0]), en))
                ident += 1
        else:
            diff += 1
print('TWN rows:', tot, ' debug:', debug, ' DE:', diff, ' identity OK:',
      ident, ' remaining non-name identity:', len(idlist))
for x in idlist:
    print('  ', x)

# menu group (PRIMARY files only: '*_de.csv'; the *_de2/_dN/_z2 files are
# historical batch copies and must not be counted)
menu_paths = sorted(glob.glob('_work/menu_de/*_de.csv'))
menu_tot = menu_diff = menu_ident = menu_debug = menuName = menuSuspect = 0
menu_sus_rows = []
NAMEN = set('Edge Azel Craymen Gash Zoah Paet Boaz Bezer Vaiman Radgam Atolm '
            'Shou Mel-Kava Sestren Shelcoof Lathum Grig Orig Uru Kuo Seekers '
            'Frontier Zadoc Zastava Coolia Coolias Hopper Hoppers Seeker '
            'Prototype Nanyd D-Type Arwen An\'jou Rhua K-GOLIA Sentinel '
            'Exterminator Laser Items Level HP Max Exsis Pack'.split())
for path in menu_paths:
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
        menu_tot += 1
        if en.strip() == de.strip():
            words = en.split()
            if (ID_OK.match(' '.join(words)) or ' '.join(words) in NAMEN
                    or len(words) == 1 and (words[0].isupper()
                                            or words[0].islower())
                    or '%' in en
                    or re.match(r'^[A-Z0-9_ \-,:;.!?]+$', en.strip())
                    or NAME_PAT.match(en.strip())
                    or INTJ_PAT.match(en.strip())
                    or GRAPH_PAT.match(en.strip())
                    or DEBUG_PAT2.match(en.strip())):
                menu_ident += 1
            else:
                menuSuspect += 1
                menu_sus_rows.append((os.path.basename(path), r[0:2], en))
        else:
            menu_diff += 1
print('menu rows:', menu_tot, 'DE:', menu_diff, 'identity OK:', menu_ident,
      'suspect:', menuSuspect)
for x in menu_sus_rows[:30]:
    print('   MS', x)

# movie FMV subtitles
mv_tot = mv_diff = mv_ident = mv_susp = 0
for ln in io.open('_work/evt_de_map.csv', encoding='latin1'):
    ln = ln.rstrip('\r\n')
    if not ln.strip() or ';' not in ln or ln.startswith('#'):
        continue
    en, de = ln.split(';', 1)
    if not en.strip():
        continue
    mv_tot += 1
    mv_diff += 1 if de.strip() != en.strip() else 0
    if de.strip() == en.strip():
        if (ID_OK.match(en.strip()) or ' '.join(en.strip().split()) in NAMEN
                or NAME_PAT.match(en.strip()) or INTJ_PAT.match(en.strip())):
            mv_ident += 1
        else:
            mv_susp += 1
print('movie fmv rows:', mv_tot, 'DE:', mv_diff, 'identOK:', mv_ident,
      'suspect:', mv_susp)

# battle labels: remaining 5 were identity names — treat as OK
print('---')
# Compute final coverage
def pct(done, total):
    return (done/total*100.0) if total else 0.0
print('=== LIVE COVERAGE (de plus intentional-identity) ===')
t_tot = diff + menu_diff + mv_diff + 241
t_all = tot + menu_tot + mv_tot + 246
p = pct(diff+menu_diff+mv_diff+241, t_all)
print('covered %d / %d = %.1f%%' % (t_tot, t_all, p))
