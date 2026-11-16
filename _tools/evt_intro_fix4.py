# Intro/CD1-FMV quality pass 4: leftover chain polish (academic report chain,
# palace scene, seekers intro). Reports any over-budget leftovers.
import sys, io
sys.stdout.reconfigure(encoding='latin1')

FIX = {
    'The Academy reported that the': 'Die Akademie meldete, dass die',
    'underground ruins were created with': 'unterirdischen Ruinen mit',
    'technologies beyond our understanding.': 'uns uebersteigender Technik:',
    'He did this to slow us down,': 'Er hielt uns nur auf,',
    'so he could go after the ruins.': 'und suchte die Ruinen auf.',
    'Although he leveled our Capital,': 'Er riss die Hauptstadt nieder,',
    'his tricks are nothing compared to': 'doch sein Trug ist nichts gegen',
    'The Empire declared war on its': 'Das Reich erklaerte den',
    'In a blinding flash,': 'In hellem Blitzlicht,',
    'our Capital was reduced to dust.': 'wurde unsere Stadt zu Staub.',
    "But we're not really living.": 'So richtig leben wir nicht.',
    'The seekers are a highly': 'Die Sucher sind eine hoch',
    'We have led the world to believe': 'Die Welt glaubt, wir seien',
    "we're a band of tomb raiders.": 'nur Grabraeuber.',
    'No one would suspect a man like me to': 'Niemand glaubt, dass ich',
    'lead anything.': 'fuehren kann.',
    'you are the dragon rider that': 'du bist der Reiter hier,',
    'has caused me so much trouble.': 'der viel Aerger stiftete.',
    'You are supposed to apologize': 'Verzeih ist angebracht',
    'at a time like this.': 'in so einer Zeit.',
    'Yes. And for that purpose,': 'Ja. Und dazu muessen wir',
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
