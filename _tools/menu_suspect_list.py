# list all menu suspects + fmv suspects with full row context
import csv
import glob
import io
import re
import sys

sys.stdout.reconfigure(encoding='latin1')

ID_OK = re.compile(r"^(Edge|Azel|Craymen|Gash|Zoah|Paet|Boaz|Bezer|Vaiman|Radgam|"
                   r"Atolm|Shou|Mel-Kava\?|Mel-Kava|Sestren|Shelcoof|Lathum|"
                   r"Grig Orig|Uru|Kuo|Seekers?|Frontier|Zadoc|Zastava|Coolia|"
                   r"Coolias|Hopper|Hoppers|Seeker|Prototype|Nanyd|D-Type|"
                   r"Arwen|An'jou|Rhua|K-GOLIA|Laser|Items|Light Wing|"
                   r"Level UP|HP Max|normal)$")
NAMEN = set('Edge Azel Craymen Gash Zoah Paet Boaz Bezer Vaiman Radgam Atolm '
            'Shou Mel-Kava Sestren Shelcoof Lathum Grig Orig Uru Kuo Seekers '
            'Frontier Zadoc Zastava Coolia Coolias Hopper Hoppers Seeker '
            'Prototype Nanyd D-Type Arwen An\'jou Rhua K-GOLIA Sentinel '
            'Exterminator Laser Items Level HP Max Exsis Pack'.split())


def is_ok(en):
    words = en.split()
    if (ID_OK.match(' '.join(words)) or ' '.join(words) in NAMEN
            or len(words) == 1 and (words[0].isupper() or words[0].islower())
            or '%' in en
            or re.match(r'^[A-Z0-9_ \-,:;.!?]+$', en.strip())):
        return True
    return False


suspects = []
for path in sorted(glob.glob('_work/menu_de/*_de.csv')):
    base = __import__('os').path.basename(path)
    with io.open(path, encoding='latin1') as f:
        rd = csv.reader(f, delimiter=';')
        header = next(rd, None)
        if not header or header[0] != 'file':
            continue
        for idx, r in enumerate(rd, start=2):
            if len(r) < 6:
                continue
            en, de = r[4], r[5]
            if not en.strip() or len(en.strip()) < 4:
                continue
            if en.strip() == de.strip() and not is_ok(en):
                suspects.append((base, idx, ';'.join(r[:4]), en))

with io.open('_work/review_fixes/menu_suspects.txt', 'w',
             encoding='latin1', newline='\n') as out:
    for base, idx, key, en in suspects:
        out.write('%s | line %d | %s | EN=%s\n' % (base, idx, key, en))
print('menu suspects:', len(suspects))

fsusp = []
for ln in io.open('_work/evt_de_map.csv', encoding='latin1'):
    ln = ln.rstrip('\r\n')
    if not ln.strip() or ';' not in ln or ln.startswith('#'):
        continue
    en, de = ln.split(';', 1)
    if not en.strip() or en.strip() != de.strip():
        continue
    if not is_ok(en):
        fsusp.append(en)
print('mv suspects:', len(fsusp))
for x in fsusp:
    print('   MV', repr(x))
