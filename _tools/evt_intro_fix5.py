import sys, io
sys.stdout.reconfigure(encoding='latin1')
FIX = {
    'In a blinding flash,': 'In hellem Blitz,',
    'The Academy reported that the': 'Die Akademie meldete, dass',
    'The seekers are a highly': 'Die Sucher: eine hoch',
}
path = '_work/evt_de_map.csv'
lines = io.open(path, encoding='latin1').read().split('\n')
hits, over = 0, []
out = []
for line in lines:
    if ';' not in line or not line.strip():
        out.append(line)
        continue
    en, de = line.split(';', 1)
    k = en.rstrip()
    if k in FIX:
        new = FIX[k]
        eb, nb = len(k.encode('latin1')), len(new.encode('latin1'))
        if nb <= eb:
            if de.strip() != new:
                line = en + ';' + new
                hits += 1
        else:
            over.append((k, eb, nb, new))
    out.append(line)
io.open(path, 'w', encoding='latin1', newline='\n').write('\n'.join(out) + '\n')
print('updated:', hits, ' still-over:', len(over))
for k, eb, nb, v in over:
    print('  OVER %d>%d %r -> %r' % (nb, eb, k, v))
