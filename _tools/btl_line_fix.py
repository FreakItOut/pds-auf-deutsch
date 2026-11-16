# narrow per-line widths for battle explanation rows in BTL_REST_map
path = '_work/menu_de/BTL_REST_map.csv'
FIX = {
    'The Gun\\nEdge\'s normal attack, also\\nrequires only one gauge to fire.\\nBest used on individual enemies.':
        'Die Waffe: Standardangriff,\\nbraucht nur eine Anzeige.\\nAm besten gegen einzelne\\nFeinde.',
    'Use Item\\nRequires one full gauge. To use\\nan item, open the Battle Menu,\\nselect Items, use the D-pad to\\nhighlight the Item, and press C.':
        'Item nutzen: Eine volle\\nAnzeige. Fuer Items: Battle\\nMenu oeffnen, Items waehlen,\\nmit D-Pad waehlen, drueckt C.',
    'Homing Lasers\\nThe dragon\'s normal attack.\\nShoots multiple lasers.\\nThe number of lasers shot\\nat once is limited.':
        'Homing-Laser\\nStandardangriff, mehrere\\nLaser. Die Zahl je Schuss\\nist begrenzt.',
    'The status of your dragon is\\ndisplayed here in the Status\\nDisplay area.':
        'Der Status des Drachen ist\\nhier im Status-Bereich\\nangezeigt.',
    'To evade danger, your dragon\\ncan move to the front,\\nback, left, or right of any\\nenemy. This is called\\npositioning.':
        'Zur Gefahrvermeidung bewegt\\nsich der Drache vor, hinter,\\nlinks oder rechts jedes\\nFeindes. Heisst: Position.',
    'Gun\\nEdge\'s normal attack. Use the\\nD-pad to aim the sight at a\\nspecific enemy.':
        'Waffe: Edges Standardangriff.\\nSteuerkreuz zielt aufs Ziel\\neines Feindes.',
}
lines = open(path, encoding='latin1').read().split('\n')
out = []
applied = 0
for line in lines:
    if ';' in line and line.strip():
        en, de = line.split(';', 1)
        if en in FIX:
            new = FIX[en]
            budget = len(en.encode('latin1'))
            if len(new.encode('latin1')) <= budget:
                line = en + ';' + new
                applied += 1
            else:
                print('TOO LONG for budget %d: %r (%d)' % (budget, new, len(new)))
    out.append(line)
open(path, 'w', encoding='latin1', newline='\n').write('\n'.join(out))
print('applied', applied)

