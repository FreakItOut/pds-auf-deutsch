# Fix BTL_REST_map.csv: replace over-budget or untranslated DE with proper
# German that fits len(de) <= len(en) (byte budget, trailing EN spaces count).
# DEBUG rows that must stay English are left untouched.
import os

DEBUG_LEAVE = {  # stripped keys that must stay as-is
    'CAUTION!! NO ENCOUNT DATA!!', 'CAUTION!! NO RESULT DATA!!',
    'COMBO :%1d,%1d', 'GET ITEM %3d !!,%3d:%3d ,%3d:%3d', 'OFF# :%2d %2x',
    'P %s %d  hp %d  y : %d', 'action kind %d  who %d', 'combo: %1d,%1d,%1d,%1d',
    'damage:%3d,%3d,%3d,%3d:%4d', 'ene %d: cmd %02x sts %02x per %d  heal %d',
    'hit_frame:%3d', 'level :%2d', 'move_cnt 0 :%04x', 'move_cnt 1 :%04x',
    'rate:%3d,%3d,%3d,%3d', 'time:%3d,%3d,%3d,%3d:%3d:%4x', 'no camera data',
    'no data', 'no use', 'heal',
}

FIX = {
    "...Not much of a listener, eh?": "...Hoerst du gar nicht zu?",
    "...We'll be back!": "...Bis bald!",
    "AGILITY CLASS": "WENDIG-KLASSE   ",
    "All ships, good luck.": "Schiffe: viel Glueck!",
    "All units, open fire!": "Alle: Offenes Feuer!",
    "All weapons, lock on!": "Alle: aufs Ziel!",
    "Atolm... you still need rest.": "Atolm... du brauchst Ruhe.",
    "Azel, I just...": "Azel, ich...",
    "B ATTACK": "B ANGR.",
    "Cannon tower... operational.": "Kanonenturm: aktiv.",
    "Customize Gun": "Waffen-Setup",
    "DAMAGE": "SCHAD.",
    "DELETE": "TILGEN",
    "Damage minimal, no problems, sir!": "Schaden gering, alles klar!",
    "Damage report, now!": "Schaden melden!",
    "Displacer Shield": "Displacer-Schild",
    "Display Berserk List": "Berserk zeigen",
    "Display Item List": "Items zeigen",
    "Don't make me attack you!": "Provokier mich nicht!",
    "Dragon Model Organism identified.": "Drachen-Exemplar erkannt.",
    "EXTRA CLASS": "EXTRA-KLAS.",
    "Edge, the red one is the queen.": "Edge: Der Rote ist Koenigin.",
    "Engine Room hit, minimal damage!": "Motorraum: leichte Schaden.",
    "Engine Room hit, severe damage!": "Motorraum: schwere Schaden.",
    "Engine room damaged.": "Motorraum defekt.",
    "Evasion System Poor": "Ausweichen schwach",
    "FIGHT": "KAMPF",
    "FIGHT!": "KAMPF!",
    "FLY AWAY": "ABFLUG",
    "FRONT MOVE": "VORWAERTS",
    "FULL-GAUGE CLASS": "VOLLLADE-KLASSE",
    "Fire the vaporizing shrapnel missile!": "Feuere die Splitter-Rakete!",
    "Fire.": "Feuer",
    "First and second engines are restored!": "Erste und zweite Motoren repariert!",
    "First and second engines failing.": "Erste und zweite Motoren faellen.",
    "Flagship Grig Orig": "Flaggs. Grig Orig",
    "Flare Bomb": "Leuchtb.",
    "Good, use the Emperor's Battlestation.": "Gut, nutzt die Kampfstation.",
    "Gunners, finish them!": "Kanoniere: erledigt!",
    "He's insane!!": "Verrueckt!!",
    "High Speed Cannon": "Schnellkanone",
    "Hit Point at maximum.": "HP auf Maximum.",
    "Hit it with everything we've got!": "Mit allem drauf!",
    "I don't want to fight you!": "Ich will nicht kaempfen!",
    "I have already told you...": "Hab dir doch gesagt...",
    "I'll end this... Now.": "Ich ende es... jetzt.",
    "I'll kill you... Understand?": "Du stirbst... Verstanden?",
    "It's coming right at us!": "Es kommt auf uns zu!",
    "It's no match for the Reaper.": "Keine Chance gg. Reaper.",
    "LASER Power": "LASER-Kraft",
    "Let's kill this dragon!": "Wir toeten ihn!",
    "Man your battle stations.": "An die Kampfstationen.",
    "NO ACTION": "KEINE TAT",
    "No damage to the Engine Room.": "Maschinenraum unversehrt.",
    "No damage to the turrets.": "Geschuetze unversehrt.",
    "No, my ship! It can't be...": "Nein! Nicht mein Schiff...!",
    "Not enough Action Gauge.": "Aktions-Anzeige leer.",
    "Not enough Berserk Points.": "Berserk-Punkte leer.",
    "Now.": "Nun.",
    "Open fire!": "Feuern!",
    "Our scouts have encountered a monster.": "Kundschafter trafen Monster.",
    "Radiation complete.": "Bestrahlung fertig.",
    "Ready Main Gun.": "Hauptk. klar.",
    "Ready the Bio Weapons!": "Bio-Waffen klar!",
    "Rotate all guns to the sides.": "Alle Geschuetze seitwaerts.",
    "Rotation Speed to Maximum.": "Drehzahl auf Maximum.",
    "SP MOVE": "SP-ZUG",
    "STUN BEGIN": "BETAEUB AN",
    "STUN END": "BET.AUS",
    "Signal Bomb": "Signalb.",
    "Strafe them!": "Beschuss!",
    "Strike First! Strike Hard!": "Erst schlagen, dann hart!",
    "Stun it before it kills us!": "Betaeub es zuerst!",
    "Suppressing Fire": "Feuer unterdr.",
    "The Disintegrator is charged!": "Disintegrator geladen!",
    "The engine room is hit!": "Motorraum getroffen!",
    "WARP MOVE": "WARP-ZUG",
    "Wait! Please... Stop!": "Hoer auf! Bitte!",
    "Wait, Azel!!": "Warte Azel!!",
    "We have failed our Emperor.": "Kaiser! Wir haben versagt.",
    "We have no choice. Return fire.": "Keine Wahl. Feuer erwidern.",
    "We need time to recharge.": "Zeit zum Nachladen!",
    "We've failed! Returning to base.": "Versagt! Zurueck zur Basis.",
    "What!?  Is the dragon nearby?": "Was!? Drache in der Naehe?",
    "Why are you on Craymen's side!?": "Warum auf Craymens Seite!?",
    "You do not know how to berserk.": "Du kannst nicht berserken.",
    "You don't know him!!": "Du kennst ihn nicht!",
    "Your Dragon can only move.": "Dein Drache bewegt sich.",
    "%c1Fire Gun.%c0": "%c1Feuern.%c0",
    "%c1Fire Laser.%c0": "%c1Laser feu.%c0",
    "%c1Make your move.%c0": "%c1Mach den Zug.%c0",
    "%c1Move to its rear.%c0": "%c1Nach hinten.%c0",
    "%c1Move to its right.%c0": "%c1Nach rechts.%c0",
    "%c1Use berserk technique.%c0": "%c1Berserk nutzen.%c0",
}

path = '_work/menu_de/BTL_REST_map.csv'
lines = open(path, encoding='latin1').read().split('\n')
hits = set()
changed = []
out = []
for line in lines:
    if ';' in line and line.strip():
        p = line.split(';', 1)
        en, de = p[0], p[1]
        k = en.strip()
        if k in FIX:
            new = FIX[k]
            hits.add(k)
            budget = len(en.encode('latin1'))
            if len(new.encode('latin1')) <= budget:
                if de != new:
                    p[1] = new
                    changed.append((k, len(en), len(new)))
                line = ';'.join(p)
    out.append(line)
open(path, 'w', encoding='latin1', newline='\n').write('\n'.join(out))

miss = set(FIX) - hits
print('applied %d, changed %d' % (len(hits), len(changed)))
for k, b, n in changed:
    print('  %3d->%3d %r' % (b, n, k))
if miss:
    print('MISSING KEYS:', len(miss))
    for k in sorted(miss):
        print('   %r' % k)

# multi-line rows report for pass 2
print()
print('MULTILINE ROWS (budget, current de len):')
for line in open(path, encoding='latin1'):
    if '"' in line or line.count(';') > 1:
        p = line.rstrip('\n').split(';', 1)
        en, de = p[0], p[1]
        if '\\n' in en and (len(de) > len(en) or de.strip() == en.strip()):
            print('  budget=%3d del=%3d | %r' % (len(en), len(de), en))

