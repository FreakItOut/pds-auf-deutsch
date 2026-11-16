# surgical fix for the 10 remaining mismatched rows (each visible in verify)
import csv
import io
import sys
sys.stdout.reconfigure(encoding='latin1')

CAMP = {108: ' beschaeftigt,', 109: ' schlachtet Monster.)',
        685: 'Wenn Meister nicht zurueck,', 686: 'Schwierigkeiten.'}
RUIN = {110: 'Ich gehe jetzt nach ihr suchen.'}

for path, uid_map in (('_work/subtitles/TWN_CAMP_PRG_de.csv', CAMP),
                      ('_work/subtitles/TWN_RUIN_PRG_de.csv', RUIN)):
    lines = io.open(path, encoding='latin1').read().split('\n')
    out = []
    n = 0
    for line in lines:
        q = line.rstrip('\r\n').split(';')
        if len(q) >= 6 and q[0].isdigit() and int(q[0]) in uid_map:
            new_de = uid_map[int(q[0])]
            if q[5] != new_de:
                q[5] = new_de
                n += 1
                line = ';'.join(q)
        out.append(line)
    with io.open(path, 'w', encoding='latin1', newline='\n') as f:
        f.write('\n'.join(out) + '\n')
    print(path, n, 'updated')
