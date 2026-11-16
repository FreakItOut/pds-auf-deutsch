# dump remaining live suspects: movie fmv 10 + menu 155 unique ENs
import csv
import glob
import io
import os
import re
import sys
sys.stdout.reconfigure(encoding='latin1')

NAMEN = set('Edge Azel Craymen Gash Zoah Paet Boaz Bezer Vaiman Radgam Atolm '
            'Shou Mel-Kava Sestren Shelcoof Lathum Grig Orig Uru Kuo Seekers '
            'Frontier Zadoc Zastava Coolia Coolias Hopper Hoppers Seeker '
            'Prototype Nanyd D-Type Arwen An\'jou Rhua K-GOLIA Sentinel '
            'Exterminator Laser Items Level HP Max Exsis Pack'.split())
ID_OK = re.compile(r"^(Edge|Azel|Craymen|Gash|Zoah|Paet|Boaz|Bezer|Vaiman|Radgam|"
                   r"Atolm|Shou|Mel-Kava\?|Mel-Kava|Sestren|Shelcoof|Lathum|"
                   r"Grig Orig|Uru|Kuo|Seekers?|Frontier|Zadoc|Zastava|Coolia|"
                   r"Coolias|Hopper|Hoppers|Seeker|Prototype|Nanyd|D-Type|"
                   r"Arwen|An'jou|Rhua|K-GOLIA|Laser|Items|Light Wing|"
                   r"Level UP|HP Max|normal)$")


def is_graphicframe(en):
    return bool(re.match(r'^\( ([OX])+\s*\)$', en.strip()))


def is_dunit(en):
    return bool(re.match(r'^D Unit \d+$', en.strip()))


def is_pcm(en):
    return bool(re.search(r'\.PCM|T_[A-Z]{2}_', en))


def is_fmt(en):
    return '%' in en


print('=== movie fmv remaining ===')
for ln in io.open('_work/evt_de_map.csv', encoding='latin1'):
    ln = ln.rstrip('\r\n')
    if not ln.strip() or ';' not in ln or ln.startswith('#'):
        continue
    en, de = ln.split(';', 1)
    if de.strip() == en.strip() and en.strip():
        words = en.split()
        if ((ID_OK.match(' '.join(words)) or ' '.join(words) in NAMEN
                or is_graphicframe(en) or is_dunit(en) or is_pcm(en)
                or is_fmt(en))):
            continue
        print('  %r || ident' % en)

print('=== menu remaining (non-graphical) ===')
seen = set()
NAMEDOK = set('Absorption Mutation Explosion Sentinel PCM  film graphics '
              'Lightwing formatted\nframes'.split())
for path in sorted(glob.glob('_work/menu_de/*_de*.csv')):
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
        if en.strip() != de.strip() or not en.strip():
            continue
        words = en.split()
        if ((ID_OK.match(' '.join(words)) or ' '.join(words) in NAMEN
                or is_graphicframe(en) or is_dunit(en) or is_pcm(en)
                or is_fmt(en) or len(en.strip()) < 4)):
            continue
        if en.strip() in seen:
            continue
        seen.add(en.strip())
        print('  %r' % en)
