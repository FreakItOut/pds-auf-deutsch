# Flag rows whose object nouns differ between EN and DE.
import io
import glob
import sys

sys.stdout.reconfigure(encoding='latin1')

CATS = {
    'lamp': ('lamp', 'lampe'),
    'pot': ('pot', 'topf'),
    'table': ('table', 'tisch'),
    'chair': ('chair', 'stuhl'),
    'bed': ('bed', 'bett'),
    'hammock': ('hammock', 'haengematte'),
    'door': ('door', 'tuer'),
    'window': ('window', 'fenster'),
    'ladder': ('ladder', 'leiter'),
    'rope': ('rope', 'seil'),
    'box': ('box', 'kiste'),
    'shelf': ('shelf', 'regal'),
    'book': ('book', 'buch'),
    'monster': ('monster', 'monster'),
    'weapon': ('gun', 'waffe'),
    'water': ('water', 'wasser'),
    'food': ('food', 'essen'),
    'meat': ('meat', 'fleisch'),
    'grain': ('grain', 'korn'),
    'nut': ('nut', 'nuss'),
    'wood': ('wood', 'holz'),
    'fire': ('fire', 'feuer'),
    'stove': ('stove', 'ofen'),
    'machine': ('machine', 'maschine'),
    'armor': ('armor', 'ruestung'),
    'cloth': ('cloth', 'tuch'),
    'medicine': ('medicine', 'medizin'),
    'oil': ('oil', 'oel'),
    'incense': ('incense', 'weihrauch'),
    'ladder2': ('stairs', 'treppe'),
}

files = sorted(glob.glob('_work/subtitles/TWN_*_de.csv'))
for path in files:
    if 'E128' not in path:
        continue
    for ln in io.open(path, encoding='latin1'):
        pass


def cats(s):
    low = s.lower()
    out = set()
    for name, (en_w, de_w) in CATS.items():
        if en_w in low or de_w in low:
            out.add(name)
    return out


for path in files:
    stem = path.split('\\')[-1].replace('_de.csv', '')
    for ln in io.open(path, encoding='latin1'):
        q = ln.rstrip('\r\n').split(';')
        if len(q) < 6 or not q[0].isdigit():
            continue
        en, de = q[4], q[5]
        if not de.strip():
            continue
        ec = cats(en)
        dc = cats(de)
        if ec and not (ec & dc):
            print('%s %s  EN=%r  DE=%r' % (stem, q[0], en, de))
