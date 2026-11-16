# csv-sync of the chain-fix batch (chains from b3): disc-authoritative
import re
import io
import glob
import os
import sys
sys.stdout.reconfigure(encoding='latin1')

REQUESTS = {
    ('TWN_E022_PRG', 35): 'Ehe Craymen mich weckte',
    ('TWN_E022_PRG', 36): 'sah ich Orte mit Atolm.',
    ('TWN_CAMP_PRG', 100): 'Ich hoerte: Ein Drache',
    ('TWN_CAMP_PRG', 101): 'kaempft gegen das',
    ('TWN_CAMP_PRG', 184): 'Habt ihr seltene Dinge,',
    ('TWN_CAMP_PRG', 185): 'zeigt sie mir.',
    ('TWN_RUIN_PRG', 337): 'Training beenden!',
    ('TWN_RUIN_PRG', 390): 'Denkst wir standen Chancen',
    ('TWN_RUIN_PRG', 391): 'gegen die Macht',
    ('TWN_RUIN_PRG', 456): 'Alle zu loeschen,',
    ('TWN_RUIN_PRG', 457): 'braucht Jahrhunderte.',
    ('TWN_RUIN_PRG', 467): 'Alte Aufzeichnungen nennen',
    ('TWN_RUIN_PRG', 468): 'eine Gruppe astraler Pfade',
    ('TWN_RUIN_PRG', 526): 'Als Nebenwirkung',
    ('TWN_RUIN_PRG', 527): 'menschliche Emotionen.',
    ('TWN_RUIN_PRG', 625): 'Krieg ist unumgaenglich,',
    ('TWN_RUIN_PRG', 626): 'wird der Ort verschont.',
    ('TWN_RUIN_PRG', 661): 'In einer Zeit ohne Ruinen,',
    ('TWN_SEEK_PRG', 529): 'Im Liberalen Bezirk wohnen',
    ('TWN_SEEK_PRG', 530): 'Reisende.',
    ('TWN_SEEK_PRG', 595): 'Denkst du, weil wir nie',
    ('TWN_SEEK_PRG', 596): 'etwas Gutes fanden',
    ('TWN_SEEK_PRG', 1043): 'Bezirk, also beschlossen sie',
    ('TWN_SEEK_PRG', 1044): 'zu bleiben',
    ('TWN_SEEK_PRG', 1068): 'Hast du gehoert?',
    ('TWN_SEEK_PRG', 1069): 'Paets Vater: Hoher Priest.',
    ('TWN_SEEK_PRG', 1074): 'Werde nicht freu. mit den',
    ('TWN_SEEK_PRG', 1075): 'Suchern, ausser im Schaeft.',
    ('TWN_SEEK_PRG', 1087): 'Stadt-Wasser: kam aus den Ruine',
    ('TWN_SEEK_PRG', 1088): 'und stieg staendig.',
    ('TWN_SEEK_PRG', 1099): 'weil der Wasserspiegel stieg.',
    ('TWN_SEEK_PRG', 1100): 'weil der Wasserspiegel stieg.',
    ('TWN_SEEK_PRG', 1126): '(Junge Frau: wirkt nicht',
    ('TWN_SEEK_PRG', 1127): 'beschaeftigt.)',
    ('TWN_SEEK_PRG', 1133): 'Du hast Mumm, hierher',
    ('TWN_SEEK_PRG', 1134): 'zu kommen, so spaet.',
    ('TWN_SEEK_PRG', 1135): 'Wenn ich genug Geld hab',
    ('TWN_SEEK_PRG', 1136): 'verlass ich hier.',
    ('TWN_SEEK_PRG', 1137): 'Bis dahin arbeite ich',
    ('TWN_SEEK_PRG', 1138): 'weiter hin.',
    ('TWN_SEEK_PRG', 1173): 'Das ist das Mindeste,',
    ('TWN_SEEK_PRG', 1174): 'als Dank.',
    ('TWN_SEEK_PRG', 1181): 'Nun, ich jage, seit ich',
    ('TWN_SEEK_PRG', 1182): 'ein Kind war.',
    ('TWN_SEEK_PRG', 1187): 'Waffe nutzen',
    ('TWN_SEEK_PRG', 1188): 'wart bis es frisst',
    ('TWN_SEEK_PRG', 1189): 'finde die Schwaeche.',
    ('TWN_SEEK_PRG', 1191): 'kreise einmal um sie',
    ('TWN_SEEK_PRG', 1192): 'lasse sie los.',
    ('TWN_SEEK_PRG', 1193): 'Toete Queen.',
    ('TWN_SEEK_PRG', 1195): 'dodges lasers',
    ('TWN_SEEK_PRG', 1196): 'Saeurspray!',
    ('TWN_SEEK_PRG', 1197): 'sie erholen sich',
}

# group by stem, rewrite de column for target uids
grouped = {}
for (stem, uid), de in REQUESTS.items():
    grouped.setdefault(stem, {})[uid] = de
changed = 0
for stem, umap in grouped.items():
    path = '_work/subtitles/%s_de.csv' % stem
    lines = open(path, encoding='latin1').read().split('\n')
    out = []
    for line in lines:
        p = line.rstrip('\r\n').split(';')
        if len(p) >= 6 and p[0].isdigit() and int(p[0]) in umap:
            new = umap[int(p[0])]
            if p[5] != new:
                p[5] = new
                changed += 1
                line = ';'.join(p)
        out.append(line)
    open(path, 'w', encoding='latin1', newline='\n').write('\n'.join(out))
print('csv cells updated:', changed)
