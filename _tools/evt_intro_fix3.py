# Intro/CD1-FMV quality pass 3: last 7 over-budget values trimmed.
import sys, io
sys.stdout.reconfigure(encoding='latin1')

FIX = {
    'Craymen will pay...': 'Craymen wird zahlen',
    'Edge, can I count on you?': 'Edge, bist du dabei?',
    'I expected no less from you,': 'Erwartet hab ich nicht mehr,',
    'destroy this Tower.': 'den Turm vernichten',
    'have been ripped to pieces': 'Doerfler nie zerfetzt.',
    'in a feeding frenzy.': 'in Fresslust.',
    'is the dragon itself!': 'ist der Drache selbst',
    'neighboring nations, but they': 'Nachbarn den Krieg. Doch',
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
