# Extend battle translations to the remaining BTL_* FNT/PRG files.
# One EN->DE per unique key; per-slot budget checked; rows go into
# <NAME>_de2.csv which menu_text_tool --patch picks up automatically.
import glob
import io
import sys
sys.stdout.reconfigure(encoding='latin1')

FIX = {
    '(I can use them to shoot the nest.)': '(Damit schiess ich aufs Nest.)',
    "(They can't reflect gunshots...)": '(Das reflektiert Schuesse!)',
    '(This is getting old.': '(Das nervt langsam.',
    '(Use the gun!)': '(Waffe raus!)',
    'A message from the Main Fleet...': 'Meldung der Hauptflotte...',
    'Alarm sent from the Control Tower!': 'Der Kontrollturm alarmiert!',
    'All gunners, keep firing!': 'Alle Geschuetze feuern!',
    'All units, attack now!!': 'Alle: greift jetzt an!!',
    'All units, you have your orders.': 'Alle: Befehle liegen vor.',
    'Are the Homing Mines ready?': 'Sind die Homing-Minen klar?',
    'Are you all right, Edge?': 'Bist du okay, Edge?',
    'Arm the Stun Bombs!': 'Betaeubungsbomben!',
    'Attack Class': 'Angriffsart',
    'Attack with Gun': 'Angr. mit Waffe',
    'Attack with Homing Laser': 'Angr. Homing-Laser',
    'Battle Droid': 'Kampf-Droide',
    'Blast it out of the sky!': 'Hol es vom Himmel runter!',
    'Bottom floor of the Tower is secured.': 'Das Untergeschoss ist gesichert.',
    'Captain, the reactor is overheating!': 'Chef, der Reaktor ueberhitzt!',
    'Concentrate all firepower!': 'Alle Kanonen aufs Ziel!',
    'Damn! They set a trap!?': 'Mist! Eine Falle!?',
    'Do you think we can kill it?': 'Halten wir es fuer toetbar?',
    "Don't flinch!  This is our last stand!": 'Nicht weichen! Letzter Kampf!',
    "Don't let up now, Edge!": 'Nicht aufgeben, Edge!',
    "Don't shoot at the ones facing us.": 'Nicht auf die Vorderseite sch.',
    "Don't shoot the ones facing us.": 'Nicht auf die Vorderseite sch.',
    'Dragon Model Organism identified.': 'Drachen-Exemplar erkannt.',
    "Enemy approaching. It's the dragon.": 'Feind naht: Es ist der Drache.',
    "Enemy approaching. Where's our fleet?!": 'Feind naht. Wo ist die Flotte!?',
    'Enemy identified to the left.': 'Feind links erkannt.',
    'Enemy identified to the right.': 'Feind rechts erkannt.',
    'Fire the proximity light cannon!': 'Nah-Lichtkanone feuern!',
    'For the Emperor... Commence attack!': 'Fuer den Kaiser... Angriff!',
    'For the honor of the Empire.': 'Fuer die Ehre des Reiches.',
    'Funny... In ruins this size,': 'Witzig: So grosse Ruinen,',
    'Go for its head, end this!': 'Nimm den Kopf: Ende!',
    'Go for the weak spot!': 'Zur Schwachstelle!',
    'Guardian Dragon': 'Waechter-Drache',
    'Gunships engaging the enemy.': 'Kanonenboote im Gefecht.',
    "He's not taking any damage!?": 'Nimm keinen Schaden!?',
    'His jaws are too heavily armored!': 'Seine Kiefer zu gepanzert!',
    'How do we kill something this big?': 'Wie toetet man so ein Teil?',
    'Hurry and heal yourself.': 'Schnell, heile dich.',
    'I did it... That was so close...': 'Geschafft... So knapp...',
    "I don't think we can get away from it...": 'So entkomm ich ihm nicht...',
    'I see you have returned...': 'Du bist also zurueck...',
    'I sure hope that thing is dead!': 'Hoffe, das Ding ist tot!',
    'I wonder if that guy is okay...': 'Ob der Typ wohl okay ist...',
    "I've finally caught up with him...": 'Ich hab ihn endlich erwischt...',
    "I've got a bad feeling about this.": 'Da rechne ich mit Aerger.',
    "I've got to avoid that cannon!": 'Der Kanone weichen!',
    "I've never seen this creature before.": 'So ein Wesen hab ich nie gesehen.',
    'Ignite the burners. Maximum velocity!': 'Brenner an. Volle Fahrt!',
    'Indeed... If the Empire truly': 'Stimmt... Wenn das Reich',
    'Is this the end of us?': 'Ist das unser Ende?',
    'It sounds crazy, but the ancient texts': 'Ein Wahnsinn, aber die Texte',
    'It stopped moving! Edge! Now!': 'Es steht! Edge! Jetzt!',
    "It's absorbing the energy.": 'Es saugt Energie auf.',
    "It's deflecting my attack!": 'Mein Angriff prallt ab!',
    "It's guarding itself with its arms!": 'Es deckt sich mit den Armen!',
    "It's here.  Stop it now!": 'Es ist da! Stopp es!',
    "It's no match for my dragon!": 'Keine Chance fuer ihn!',
    "It's... up to you...": 'Du bist dran...',
    'Just kill it, so we can go.': 'Toetet es, dann gehen wir.',
    'Knock it out of the sky!': 'Vom Himmel holen!',
    "Let's see their Gods protect them now.": 'Ob die Goetter helfen!',
    'Long live the... Aaaaagghh...': 'Lang lebe... Aaargh...',
    "Look, the arms aren't moving.": 'Schau, die Arme stehen still.',
    'Move to attack positions!': 'An die Angriffspositionen!',
    'No response from the Second Fleet.': 'Keine Meldung der 2. Flotte.',
    "No!  We're falling!": 'Wir fallen!',
    'Not enough Action Gauge.': 'Aktions-Anzeige leer.',
    'Not enough Berserk Points.': 'Berserk-Punkte leer.',
    "Now it's up to us...": 'Jetzt sind wir dran',
    'Now we can get out of this place.': 'Jetzt koennen wir raus.',
    "Now, shoot!  It's exposed!": 'Schiess! Es ist offen!',
    'On your mark, sir.': 'Bereit, Herr.',
    'Our purpose is to fulfill': 'Unsere Aufgabe ist es,',
    'Our reports were correct. Attack!': 'Die Meldungen stimmten. Los!',
    'Our sacrifice was not in vain.': 'Unser Opfer war nicht umsonst.',
    "Perhaps your dragon's presence": 'Vielleicht weckte dein Drache',
    'Port Engine Out': 'BB-Motor aus',
    'Reload the Homing Mines. Hurry!': 'Homing-Minen laden. Schnell!',
    'Reload the guns!': 'Nachladen!',
    'Remember your training.': 'Denk ans Training.',
    'Right Arm Paralyzed': 'Rechter Arm gelaehmt',
    'Royal Fleet, all units attack!': 'Reichsflotte, alle angreifen!',
    'Second Fleet report to Grig Orig.': 'Die 2. Flotte meldet an Grig Orig.',
    'Select Dragon Type': 'Drachentyp waehlen',
    'Send this monster back to its grave!': 'Zurueck ins Grab, Vieh!',
    'Shift to Level 2 Attack Mode!': 'Wechsel Angriffs-Modus 2!',
    'Shoot until you hit': 'Bis es trifft.',
    'Sixth Fleet.  Intercept!': '6. Flotte: Abfangen!',
    'So, this is the infamous dragon...': 'So, der beruechtigte Drache...',
    "Target entering the cannon's range!": 'Ziel in Reichweite der Kanone!',
    'Target is approaching Grig Orig.': 'Ziel naeht sich Grig Orig.',
    'Target moving to the side. Rotate!!': 'Ziel seitlich: drehen!!',
    'That attack will only make it grow.': 'Diese Attacke waechst es!',
    'That bastard Vaiman, he tricked us!': 'Vaiman hat uns reingelegt!',
    'That last attack really hurt it.': 'Der letzte Hieb tat weh.',
    'That thing was horrible!': 'Sowas Grauenhaftes!',
    "That's for my friends!": 'Fuer meine Freunde!',
    "That's... Craymen's ship!!": 'Das ist Craymens Schiff!!',
    'The Divine Visitor has come.': 'Der Goettliche ist gekommen.',
    'The bridge is damaged!': 'Die Bruecke ist defekt!',
    'The dragon annihilated our fleet...': 'Er vernichtete unsere Flotte...',
    'The dragon approaches.': 'Der Drache ist da.',
    'The dragon is approaching fast!': 'Der Drache kommt schnell!',
    'The output level is not going up...': 'Die Leistung steigt nicht...',
    'The reason why the Empire came here.': 'Deshalb kam das Reich hierher.',
    'Then I must swat this pest myself...': 'Dann schlag ich die Plage',
    'There are no enemies to attack.': 'Hier gibt es keinen Feind.',
    'There it is.': 'Da ist es.',
    'They are sharing energy!': 'Sie teilen Energie!',
    'They unearthed a great evil': 'Sie gruben ein Uebel aus,',
    'This day is ours. Obliterate the fool!': 'Heute gehoert uns alles: Los!',
    'This is bad. It called reinforcements.': 'Schlecht: Es holt Verstaerkung.',
    'This is no different than before.': 'Das gleiche wie vorher.',
    'This is worse than I thought!': 'Schlimmer als gedacht!',
    'This one looks different...': 'Der sieht anders aus...',
    'This... is the power of the dragon!?': 'Das ist Drachenmacht!?',
    'Through The Heart': 'Mitten ins Herz',
    'Use another attack.': 'Andere Attacke!',
    "We can't hit it from down here.": 'Hier unten treffen wir nicht.',
    'We cannot fail before his highness.': 'Vor seiner Hoheit keine Pleite.',
    'We should head back to camp.': 'Wir sollten zum Lager.',
    "We shouldn't have destroyed the nest.": 'Das Nest haetten wir lassen.',
    'We will attempt to intercept.': 'Wir greifen ab.',
    "We've come this far.": 'So weit sind wir.',
    "We've failed!  Abandon ship!": 'Verloren! Von Bord!',
    "We've got to head for the exit.": 'Wir muessen zum Ausgang.',
    "We've reached takeoff speed. Launch!": 'Startspeed erreicht: Los!',
    'What is this blue creature!?': 'Was ist so ein Ding!?',
    'What was that blast!?': 'Was war der Knall!?',
    "What!?  They're mythical...": 'Die sind mythisch...',
    "What's that!?": 'Was ist das!?',
    "What's this?": 'Was ist das?',
    'With a human...': 'Mit einem...',
    'You did it, Edge!': 'Geschafft, Edge!',
    'You disobey the ancient ones...': 'Du missachtest die Alten...',
    'You do not have any item.': 'Du hast kein Item.',
    'You do not have any parts.': 'Du hast kein Teil.',
    'You do not know how to berserk.': 'Du kannst nicht berserken.',
    'You have already done so.': 'Schon gemacht.',
    'You have chosen a different path...': 'Du waehltest einen andern Weg...',
    'You ignore your duty...': 'Pflicht ignoriert...',
    'You should use the shield, Edge!': 'Nutze den Schild, Edge!',
    "You've fed them too much power...": 'Ihnen zu viel Kraft...',
    "You've got to find the weak spot.": 'Finde die Schwachstelle!',
    'Your Dragon can only move.': 'Dein Drache bewegt sich.',
    'Zoah will pay for its disobedience.': 'Zoah zahlt fuer den Trotz.',
    'from the monsters directly.': 'direkt von den Monstern.',
    'slain by a dragon long ago.': 'vom Drachen getoetet.',
    'the will of the ancients.': 'den Willen der Alten.',
    'until they fulfill their purpose.': 'bis ihre Pflicht erfuellt ist.',
    "we're all doomed.": 'Alle verloren.',
    "you'd expect nastier monsters...": 'Haertere Monster erwartet.',
}

# builds per-file rows from extract_menu_full's _en.csv list.
FILES = ['BTL_A3_FNT', 'BTL_A32_FNT', 'BTL_A53_FNT', 'BTL_A5_2_PRG',
         'BTL_A7_FNT', 'BTL_A72_FNT', 'BTL_B2_FNT', 'BTL_B53_FNT',
         'BTL_B5_2_PRG', 'BTL_B6_FNT', 'BTL_B62_FNT', 'BTL_C22_FNT',
         'BTL_C4_FNT', 'BTL_C5_FNT', 'BTL_C8_FNT', 'BTL_C82_FNT',
         'BTL_D2_FNT', 'BTL_D22_FNT', 'BTL_D4_FNT', 'BTL_D5_FNT']


def esc(t):
    return t.replace('\\', '\\\\').replace('\n', '\\n')


total_rows = 0
over = []
written = []
for name in FILES:
    enp = '_work/menu_de/%s_en.csv' % name
    outp = '_work/menu_de/%s_de2.csv' % name
    rows = []
    for ln in io.open(enp, encoding='latin1'):
        q = ln.rstrip('\r\n').split(';', 1)
        if len(q) < 5 or ';' not in ln:
            continue
        head, rest = ln.rstrip('\r\n').split(';', 4) if False else (None, None)
    # easier: use csv reader with ';' delim
    import csv as c2
    rd = c2.reader(io.open(enp, encoding='latin1'), delimiter=';')
    header = next(rd, None)
    for r in rd:
        if len(r) < 5:
            continue
        fname, off, prefix, slen, en = r[0], r[1], r[2], r[3], r[4]
        key = en.strip()
        if key not in FIX:
            continue
        de = FIX[key]
        dnb = len(de.replace('\\n', '\n').encode('latin1'))
        enb = len(en.replace('\\n', '\n').encode('latin1'))
        if dnb > enb:
            over.append((name, en[:40], dnb, enb))
            continue
        rows.append('%s;%s;%s;%d;%s;%s' % (fname, off, prefix, int(slen) if slen.isdigit() else len(en),
                                           esc(en), esc(de)))
        total_rows += 1
    with io.open(outp, 'w', encoding='latin1', newline='\n') as fh:
        fh.write('file;off;prefix;len;en;de\n')
        fh.write('\n'.join(rows) + '\n')
    written.append((name, len(rows)))
print('files touched:', len(written), 'total rows:', total_rows)
for n, c in written:
    if c:
        print(' ', n, c)
print('over:', len(over))
for x in over:
    print('  OVER', x)
