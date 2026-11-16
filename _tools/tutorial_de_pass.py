# Final German pass for the remaining English TUTORIAL.CGB fragments.
# Overrides are keyed by offset; two dialogue chains get re-printed lines
# (their disc already has German -> force=true).
import csv
import sys
sys.stdout.reconfigure(encoding='latin1')
SECT, DATA = 2352, 2048


def read_file(binpath, lba, size):
    with open(binpath, 'rb') as fh:
        out = bytearray()
        need = size
        s = lba
        while need > 0:
            fh.seek(s * SECT + 16)
            chunk = fh.read(min(DATA, need))
            if len(chunk) < min(DATA, need):
                break
            out += chunk
            need -= len(chunk)
            s += 1
    return bytes(out[:size])


idx = {r['name']: (int(r['lba']), int(r['size']))
       for r in csv.DictReader(open('_work/fs_records_all.csv',
                                    encoding='latin1'), delimiter=';')
       if int(r['lba']) > 0 and int(r['size']) > 0}
lba, size = idx['TUTORIAL.CGB']
disc = read_file('_work/patched_disc1.bin', lba, size)


def actual(o):
    e = o
    while e < len(disc) and disc[e] not in (0, 0xFF):
        e += 1
    return disc[o:e].decode('latin1')


OVR = {
    52970: '(%a1 erholt sich...)',
    53325: 'Rueber kommst du nie allein',
    53438: 'Danke! Loehne dir...',
    53964: 'Danke! Loehne dir...',
    55575: 'Nimm. Verdient hast du es.',
    55688: 'mir was schulden.',
    55723: 'Geschafft! Danke!',
    55917: 'bist mir ein zaeher Bursche.',
    57981: 'Danke...',
    58064: 'He he he...',
    58302: 'Danke...',
    58385: 'He he he...',
    58623: 'Danke...',
    58706: 'He he he...',
    58973: 'Wurmgaenge, unterirdische',
    59000: 'Wasserwege...',
    59050: 'Wie dem auch sei: finden wir',
    59078: 'einen Untergrundweg.',
    59282: 'Wasserlaeufe als Wege.',
    59351: 'Oase, reisen wir unterirdisch.',
    59505: 'offene Gaenge nach unten nutzen.',
    59654: 'Gaenge zum Untergrundweg.',
    60497: 'vernichtete unzaehlige Sucher.',
    60748: 'So manche',
    61052: 'Man glaubt,',
    61541: 'gottgleiche Macht hatten.',
    61909: 'auf uns warteten.',
    62343: 'vielleicht Kriege,',
    63061: 'Tja,',
    63479: '...Tod?',
    63532: 'zu schuetzen.',
    63875: 'Ich kam nicht an Uru.',
    63949: 'Siegel?',
    63957: 'Das ist grossartig!',
    64034: 'Oh, pardon.',
    64476: 'Zerstoert man Mel-Kava,',
    64677: 'irgendwo in Zoah.',
    65234: 'Das ist ein Schatz, oder?',
    65470: 'Das ist ein Schatz, oder?',
    65500: '(Wirkt zufrieden.)',
    65612: '(Azel ist bewusstlos.)',
    65635: '(Da ist etwas nahe Azel.)',
    65804: '(Azel ist noch bewusstlos.)',
    66204: 'Ihm vertrauen.',
    66451: 'Wenn ich synchron bin, kann',
    66624: 'Ja, ich weiss...',
    66944: 'zu Craymen...',
    67256: 'Du bist anders.',
    67274: 'Du bist wie ein Anderer.',
    67375: 'wirktest manchmal leblos.',
    67834: 'Schon klar. Du verstehst',
    67902: 'Meine Denkmuster',
    68902: 'Ich... ich fuehlte fremd.',
    69292: 'Sogar mit Gewalt.',
    69404: 'vor Stunden.',
    69575: 'vor Stunden.',
    69752: 'Ich... ich fuehlte fremd.',
    70155: 'Sogar mit Gewalt.',
    70631: 'Halt', 70670: 'Halt', 70711: 'Halt', 70757: 'Halt',
    70777: 'Halt', 70822: 'Halt', 70842: 'Halt', 70889: 'Halt',
    70731: 'Zur Sucher-Festung',
    70803: None,  # placeholder, see chains below
    71321: '(Erzeugt es Hologramme?)',
    71491: '(Oh, er ist gestolpert...',
    71510: 'er geht kaum, oder?)',
    71590: '(Wie ein mutierter Coolia...)',
    72014: '(Er hasst mich wohl...)',
    72042: 'Beruh.',
    72049: 'Ignor.',
    72056: 'Tadel',
    72146: 'Tadel',
    72152: 'Blick',
    72158: 'Ignor.',
    72165: '(Muede?',
    72179: 'Muessen beim Kaempfen aufholen.)',
    72214: '(Ich mache ihn wohl nervoes.)',
    72244: 'Blick',
    72250: 'Ignor.',
    72257: 'Lach',
    72330: 'Str',
    72334: 'Lach',
    72340: 'Sauer',
    72455: 'Lach',
    72461: 'Ignor.',
    72468: 'Str',
    72472: '(Heute wirkt er gesund.)',
    72550: '(Huch? Hab ihn verletzt?)',
}
OVR[70803] = 'Zur Sucher-Festung'        # second Go-to string copy
OVR[70757] = 'Halt'                      # kept for clarity

retone = {}   # off -> (new de)
i1 = disc.find(b'Verdammt, was soll ich')
if i1 > 0:
    retone[i1] = 'Verdammt, was sag ich'
i2 = disc.find(b'den Drachen so sehen will?')
if i2 > 0:
    retone[i2] = 'sich den Drachen ansehn?)'
i3 = disc.find(b'was der Turm tut.')
if i3 > 0:
    retone[i3] = 'ich sagen, was der Turm tut.'

lines = open('_work/menu_de/TUTORIAL_CGB_de.csv', encoding='latin1').read() \
    .split('\n')
out, nfix, nforce, conflicts = [], 0, 0, []
for line in lines:
    q = line.split(';')
    if len(q) < 6:
        out.append(line)
        continue
    off_raw = q[1]
    if not off_raw.isdigit():
        out.append(line)
        continue
    off = int(off_raw)
    en = q[4].replace('\\n', '\n')
    de = q[5].replace('\\n', '\n')
    if off in OVR:
        new = OVR[off]
        if len(new.encode('latin1')) > len(en.encode('latin1')):
            conflicts.append('OVR TOO LONG off=%d %r %d>en%d' % (
                off, new, len(new), len(en)))
            out.append(line)
            continue
        q[5] = new.replace('\n', '\\n')
        nfix += 1
        out.append(';'.join(q))
        continue
    if off in retone:
        new = retone[off]
        if len(new.encode('latin1')) > len(en.encode('latin1')):
            conflicts.append('RETONE TOO LONG off=%d %r' % (off, new))
            out.append(line)
            continue
        q[5] = new.replace('\n', '\\n')
        if len(q) < 7:
            q.append('1')
        else:
            q[6] = '1'
        nforce += 1
        out.append(';'.join(q))
        continue
    out.append(line)
with open('_work/menu_de/TUTORIAL_CGB_de.csv', 'w', encoding='latin1',
          newline='\n') as fh:
    fh.write('\n'.join(out) + '\n')
print('overrides=%d refit=%d' % (nfix, nforce))
for c in conflicts:
    print(c)
