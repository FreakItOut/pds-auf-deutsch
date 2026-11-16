# Scan all DE CSVs for suspicious abbreviations/truncations and broken grammar.
import glob
import io
import re
import sys

sys.stdout.reconfigure(encoding='latin1')

SUS = re.compile(r'((?<!\.)\.\.(?!\.)|Masch\.|Toepf\.|Haengem\.|Getr\.|Aussenst\.|'
                 r'Raeucherst\.|\bf\.|Fluess\.|Werkz\.|Abgeschl\.|'
                 r'Persoenl\.|Reisegegenst\.|Beh\.)')
LOWER = re.compile(r'^\([a-z]')

n = 0
for path in sorted(glob.glob('_work/subtitles/TWN_*_de.csv')):
    stem = path.split('\\')[-1].replace('_de.csv', '')
    for ln in io.open(path, encoding='latin1'):
        q = ln.rstrip('\r\n').split(';')
        if len(q) < 6 or not q[0].isdigit():
            continue
        en, de = q[4], q[5]
        if not de.strip():
            continue
        hits = []
        if SUS.search(de):
            hits.append('SUS')
        if LOWER.match(de):
            hits.append('LOWER')
        if '  ' in de:
            hits.append('DBLSPACE')
        if de.count('(') != de.count(')'):
            hits.append('PAREN')
        if hits:
            print('%s %s %s | EN=%r | DE=%r'
                  % (stem, q[0], ','.join(hits), en, de))
            n += 1
print('flagged=%d' % n)
