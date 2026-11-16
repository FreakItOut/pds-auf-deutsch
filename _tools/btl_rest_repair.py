# Repair BTL_REST_map: collapse duplicated de fields, fix '??' mojibake,
# write final shorter de for the remaining over-budget rows.
line_by_start = []

path = '_work/menu_de/BTL_REST_map.csv'
lines = open(path, encoding='latin1').read().split('\n')

NEW_DE = {
    'Gun\\nEdge\'s normal attack. Use the\\nD-pad to aim the sight at a\\nspecific enemy.':
        'Waffe: Edges Standardangriff.\\nSteuerkreuz zielt aufs Ziel\\neines Feindes.',
    'STUN\\nWhen your dragon is paralyzed,\\nit cannot fire lasers or use its\\nBerserk Techniques. Your dragon\\ncan only reposition itself.':
        'BETAEUBUNG\\nIst der Drache gelaehmt,\\nfeuert er keine Laser,\\nnutzt keine Berserk-Technik.\\nEr bewegt sich nur.',
    'The dragon was hit with a\\nspecial attack that paralyzed\\nit.':
        'Der Drache lief in einen\\nlaehmenden Spezialangriff.',
    'This enemy has an average\\ndefensive rating from the front.\\nAttack here and it will suffer\\naverage damage.':
        'Dieser Feind wehrt von\\nvorn nur durchschnittlich\\nab. Angriff hier: normaler\\nSchaden.',
    'To evade danger, your dragon\\ncan move to the front,\\nback, left, or right of any\\nenemy. This is called\\npositioning.':
        'Zur Gefahrvermeidung bewegt\\nsich der Drache vor, hinter,\\nlinks oder rechts jedes\\nFeindes. Das heisst Position.',
    'To inflict heavy damage, aim\\nfor an enemy\'s weak spot.\\nThis area is marked \'WEAK\'.':
        'Fuer Schaden: auf die\\nschwaechste Stelle zielen.\\nMarkiert \'WEAK\'.',
    'Unused portions of the gauge\\nare not lost. You may perform an\\naction as soon as the required\\ngauge(s) are charged, or wait\\nand deliver a series of actions.':
        'Ungenutzte Teile der Anzeige\\nbleiben erhalten. Handle sobald\\ndie Ladung passt, oder warte\\nund fuehre mehrere Aktionen\\nhintereinander aus.',
    'You can concentrate your attack\\non a weakness or a single enemy.':
        'Angriff buendeln: auf eine\\nSchwaeche oder einen Feind.',
    'The Reaper is overheating!': 'Der Reaper ueberhitzt!',
    'SHOT Power': 'SCHUSS',
    'heal': 'heil',
    'no camera data': 'keine Kamera',
    'no data': 'Ohne D.',
    'no use': 'leer',
}

out = []
repaired = 0
applied = 0
skipped = 0
for line in lines:
    if not line.strip():
        out.append(line)
        continue
    if ';' not in line:
        out.append(line)
        continue
    parts = line.split(';')
    en = parts[0]
    de_rest = parts[1:]
    if len(parts) > 2:
        # collapse duplicates of the same de (exact or mojibake variant)
        plain = de_rest[0]
        dup_all = True
        for x in de_rest[1:]:
            if x != plain and x.replace('?', '_') != plain.replace('?', '_') \
                    and x.replace('ae', '?') != plain.replace('ae', '?'):
                dup_all = False
                break
        if dup_all:
            line = en + ';' + plain.replace(' gel??hmt', ' gelaehmt').replace('??berhitzt', 'ueberhitzt')
            repaired += 1
    # apply NEW_DE where budgets fit
    if en in NEW_DE:
        new = NEW_DE[en].strip()
        if len(new.encode('latin1')) <= len(en.encode('latin1')):
            line = en + ';' + new
            applied += 1
    out.append(line)

open(path, 'w', encoding='latin1', newline='\n').write('\n'.join(out))
print('repaired duplicates: %d, applied new de: %d' % (repaired, applied))

# re-verify
over = 0
for line in open(path, encoding='latin1'):
    line = line.rstrip('\r\n')
    if not line or ';' not in line:
        continue
    p = line.split(';', 1)
    en, de = p[0], p[1]
    if len(de.encode('latin1')) > len(en.encode('latin1')):
        over += 1
        print('STILL OVER budget=%3d del=%3d EN=%r DE=%r' % (len(en), len(de), en, de))
print('still over:', over)
