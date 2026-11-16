# -*- coding: utf-8 -*-
"""Ersetzt die noch englischen Spieltexte in allen vier Discs.

Die Fundstellen stammen aus _work/review_fixes/english_candidates.txt
(Datei + Offset je Disc). Ersetzt wird nur, wenn dort exakt der
englische Text steht und der deutsche Text nicht laenger ist.
"""
import collections
import csv as _csv
import io
import sys

sys.stdout.reconfigure(encoding='latin1')
SECT, DATA = 2352, 2048

T = {
    # --- CHILDMP.MCB: Speichern/Laden ---
    'You may save your game.': 'Du kannst speichern.',
    'Will erase old file. Execute?': 'Alte Datei loeschen?',
    'Saving:  Do not power down.': 'Speichern: Nicht abschalten',
    'Not enough space to save.': 'Nicht genug Platz.',
    'The data has been saved.': 'Daten gespeichert.',
    'Load Game From Internal RAM': 'Spielstand aus Intern-RAM',
    'Load Game From Cartridge RAM': 'Spielstand aus Cartridge-RAM',
    'Load Game From Expanded Memory': 'Spielstand aus Erw.-Speicher',
    'Not used': 'Frei',
    'Not Use': 'Frei',
    'It is incorrect data.': 'Daten ungueltig.',
    'Above the Excavation': 'Ueber der Ausgrabung',
    'Now Loading !!': 'Lade...',
    'No File!!': 'Kein Save',
    'NO ENCOUNT AREA': 'KEINE KAMPFZONE',
    'FRAME OVER': 'GAME OVER',
    # --- CHILDMP.MCB: Item-Beschreibungen ---
    'Single detonation.': 'Einzel-Detonation.',
    'Double detonation.': 'Doppel-Detonation.',
    'Triple detonation.': 'Dreifach-Detonat.',
    'Mesmerizes enemies.': 'Betaeubt Gegner.',
    'Replenishes BP by 50.': 'BP +50.',
    'Replenishes BP by 100.': 'BP +100.',
    'Replenishes BP by 250.': 'BP +250.',
    'Replenishes BP by 500.': 'BP +500.',
    'Cures SLOW condition.': 'Heilt LANGSAM.',
    'Cures STOP condition.': 'Heilt STOP.',
    'Cures PAIN condition.': 'Heilt SCHMERZ.',
    'Cures BIND condition.': 'Heilt BINDEN.',
    'Increases rounds fired.': 'Mehr Schuesse.',
    'Absorbs life force, maximum BP.': 'Lebenskraft: max. BP.',
    'Absorbs life force, minimum BP.': 'Lebenskraft: min. BP.',
    'Tracks three targets.': 'Drei Ziele folgen.',
    'BP is at maximum.': 'BP ist voll.',
    'Equipping.': 'Anlegen...',
    'Requires higher Gauge charge.': 'Braucht mehr Anzeige.',
    # --- TWN_RUIN.PRG: Themenmenue ---
    'About Gash': 'Ueber Gash',
    'About Azel': 'Ueber Azel',
    # --- E021.EPK ---
    "From here, I'll go on my own.": 'Von hier geh ich allein.',
    "Thanks to you, I'll live": 'Dank dir lebe ich',
    "You see, seekers don't take chances.": 'Sucher gehen kein Risiko.',
    "Anyone who doesn't show up on time,": 'Wer nicht puenktlich kommt,',
    'is presumed dead.': 'gilt als tot.',
    "I've got something for you, kid.": 'Ich hab was fuer dich.',
    'Take this and go east.': 'Nimm das, geh ost.',
    'You should see a caravan there.': 'Dort ist eine Karawane.',
    "Show that, and they'll help you out.": 'Zeig es, sie helfen dir.',
    "As long as they don't find out": 'Solange sie nicht merken,',
    'about your dragon.': 'wegen des Drachen.',
    "I'll always consider you my friend.": 'Du bleibst mein Freund.',
    'You can count on me,': 'Zaehl auf mich,',
    'if you need anything.': 'wenn du was brauchst.',
    'Communications are down!': 'Funk ist ausgefallen!',
    'All of our battleships are destroyed.': 'Unsere Schlachtschiffe sind weg.',
    'Is the Imperial Cannon ready yet!?': 'Ist die Reichskanone bereit!?',
    "Captain! It's not holding!": 'Captain! Es haelt nicht!',
    "We're trapped! Aaaagghh!": 'Falle! Aaaagghh!',
    "No! We're going down!!": 'Nein! Wir fallen!!',
    'Were you successful, Edge?': 'Warst du erfolgreich?',
    'Vaiman, you didn\'t...': 'Vaiman, du nicht...',
    'No need to go here...': 'Hier nicht noetig...',
    'Fleet on the Lake': 'Flotte am See',
    'Here, something like this.': 'Hier, so etwas.',
    'or Devils to fear them,': 'oder Teufel fuerchten',
    "it's all religious propaganda.": 'alles religioese Propaganda.',
    "Let's see, where did I...": 'Mal sehen, wo war...',
    'Here it is!': 'Da ist es!',
    'You see...': 'Also...',
    'is done.': 'fertig.',
    'them out.': 'sie raus.',
    'can we do?': 'was nun?',
    'paid off.)': 'gelohnt.)',
    'after all.': 'doch noch.',
    'need me.': 'braucht.',
    'that girl?': 'das Kind?',
    # --- CADRO.MCB / FLD_B6.MCB: Kaiser-Bericht ---
    'A waterway gate must': 'Ein Wassertor muss',
    "they'll find us.": 'finden sie uns.',
    'I can feel his presence nearby...': 'Ich spuere ihn ganz nah...',
    "<We'll soon have permission to>": '<Wir erhalten bald Erlaubnis,>',
    '<implant that mechanism.>': '<den Mechanismus setzen.>',
    '<With it, we should easily clear>': '<Damit schaffen wir leicht>',
    '<the targeted value.>': '<den Zielwert.>',
    '<However, there is a serious defect.>': '<Doch es gibt einen Defekt.>',
    '<Our latest subject is doing fine.>': '<Unser Proband ist wohlauf.>',
    '<That problem has already been solved>': '<Das Problem ist schon geloest>',
    '<by manipulating its life span.>': '<durch Lebensspannen-Trick.>',
    '<We shall name this drone Azel.>': '<Die Drohne heisst Azel.>',
    '<A week has passed since the attack.>': '<Eine Woche seit dem Angriff.>',
    '<The drone has not been found.>': '<Drohne nicht gefunden.>',
    '<She has not been completed yet.>': '<Sie ist noch nicht fertig.>',
    '<I only hope she does not become>': '<Hoffentlich wird sie nicht>',
    '<the development of %c6Light Wing%c0>':
        '<Entwicklung von %c6Light Wing%c0>',
    '<a renegade project, has ordered>': '<ein Abtrunniges Projekt befahl>',
    '<us to delete all records>': '<alle Daten zu loeschen>',
    '<But we have decided to>': '<Doch wir beschlossen,>',
    '<into one memory plate,>': '<auf eine Platte,>',
    '<divided it into 12 pieces>': '<teilten sie in 12 Stuecke>',
    '<called %c5D Units%c0, and scatter>': '<die %c5D Units%c0, verteilten>',
    '<hoping one day>': '<einst dereinst>',
    '<would inherit our work...>': '<erbt unser Werk...>',
    '<Report regarding the %c6Light Wing%c0>':
        '<Bericht ueber %c6Light Wing%c0>',
    '<We have at last>': '<Endlich ist uns>',
    '<succeeded in developing the>': '<die Entwicklung der>',
    '<ultimate form of the dragon.>': '<ultimativen Drachenform.>',
    '<It is a being far different...>': '<Ein ganz anderes Wesen...>',
    '<A Messenger of the Gods.>': '<Ein Bote der Goetter.>',
    "...Alright, let's go.": '...Also los.',
    "They've mutated,": 'Sie mutieren,',
    "They've mutated!?": 'Sie mutieren!?',
    "Craymen's Fleet's been through here?": 'Craymens Flotte war hier?',
    "Let's hurry!!": 'Beeilung!!',
    '...Even wipe my nose.': '...Sogar Nase putzen.',
    # --- FLD_C4_6.MCB / CAMPOBJ.MCB ---
    'is already open.': 'ist schon offen.',
    'Craymen used is blocked.': 'Craymen-Weg blockiert.',
    'Azel... promise me.': 'Azel... versprich.',
    "Let's go, Edge.": 'Los, Edge.',
    'I think I got it.': 'Ich habs.',
    'I thought I saw another one,': 'Ich sah noch einen,',
    "then let's go!!": 'dann los!!',
    "There's got to be a way.": 'Es muss einen Weg geben.',
    "...Azel? What's wrong?": '...Azel? Was ist?',
    "You're wrong!": 'Du irrst!',
    'Azel, I think...': 'Azel, ich...',
    "you're becoming human...": 'du wirst menschlich...',
    'it might be a good idea to': 'es waere gut, zu',
    'if it exists...': 'falls vorhanden',
    'we can return.': 'heimwaerts.',
    "You're determined to go": 'Du willst wirklich hin',
    'We did it together.': 'Wir schafften es.',
    "we'll be overwhelmed.": 'wir unterliegen.',
    # --- MENUEN.FNT / Bestiarium ---
    'Sestren is able to': 'Sestren kann sich',
    'morph itself into': 'in alles wandeln,',
    'In this later stage,': 'In dieser Phase ist',
    'Sestren is deadly.': 'Sestren ist fatal.',
    'and one day they will leave.': 'einst werden sie gehen.',
    'a battle squadron could annihilate us.':
        'ein Geschwader vernichtet uns.',
    'This town is protected by the Gods.':
        'Die Stadt schuetzen die Goetter.',
    # --- BTL_*: Kampf-Zwischenrufe ---
    'They look at you before they shoot.':
        'Sie zielen, bevor sie schiessen.',
    'Stay behind them and show no mercy!':
        'Bleib hinter ihnen, keine Gnade!',
    'Look out!': 'Vorsicht!',
    'Just shoot and move!': 'Feuer und lauf!',
    'Watch out for spit!': 'Vorsicht, Spucke!',
    "It's weakening.": 'Es schwaechert.',
    'I can still... Aaaaagghhh...': 'Ich kann noch... Aaaah...',
    'There must be a nest up there.': 'Da oben muss ein Nest sein.',
    "There must be a way... It's coming.": 'Ein Weg muss her... Er kommt.',
    "It's getting away!": 'Er entkommt!',
    'Just let it go.': 'Lass ihn!',
    "It's like squashing little bugs.)": 'Wie kleine Kaefer zerquetschen.)',
    "We've got him!": 'Wir haben ihn!',
    'Well, get it working!!!': 'Bring es zum Laufen!!!',
    "They've breached our defensive line.":
        'Sie durchbrachen unsere Linie.',
    'His enemy is my enemy.': 'Sein Feind mein Feind.',
    'Atolm without hurting her.': 'Atolm nicht verletzen.',
    # --- Feld / Karawane ---
    "they'll leave us alone.": 'lassen sie uns in Ruhe.',
    'It fell into a sand trap...': 'Es fiel in eine Falle...',
    '(I know I can do better!!)': '(Ich kann es besser!!)',
    '(Try again?)': '(Nochmal?)',
    'A:SAVE, B:NOT SAVE': 'A:SICHERN, B:NEIN',
    'If you accumulate three': 'Bei drei aufgeladenen',
    'will be activated according,': 'Anzeigen wird je nach',
    'It seems to want': 'Es will wohl',
    'A Tobitama is following me.': 'Ein Tobitama folgt mir.',
    'I guess he wants his mother.': 'Wohl zu seiner Mutter.',
    'somewhere before...': 'Irgendwo vorher...',
    # --- Abschluss / Credits ---
    '  But more quests are awaiting you.': '  Doch weitere Aufgaben warten.',
    '  There is much you have not seen.': '  Vieles blieb dir verborgen.',
    "    You've lived the adventure": '    Du erlebtest das Abenteuer',
    '  Your quest shall live forever': '  Deine Reise bleibt ewig.',
}

SKIP_EXT = ('.PNB', '.CGB', '.SND', '.PCM', '.WAV', '.MOV', '.CPK',
            '.ADX')

recs = {r['name']: (int(r['lba']), int(r['size']))
        for r in _csv.DictReader(open('_work/fs_records_all.csv',
                                      encoding='latin1'), delimiter=';')
        if r['lba'].isdigit() and int(r['lba']) > 0}

hits = collections.defaultdict(list)
for ln in io.open('_work/review_fixes/english_candidates.txt',
                  encoding='latin1'):
    p = ln.rstrip('\n').split(';', 3)
    if len(p) != 4:
        continue
    d, name, off, t = p
    if t in T:
        hits[(int(d[1:]), name)].append((int(off, 16), t))

files = {}
done = 0
skipped = 0
for (d, name), items in sorted(hits.items()):
    if name not in recs:
        continue
    lba, size = recs[name]
    key = (d, name)
    if key not in files:
        out = bytearray()
        need, s = size, lba
        with open('_work/patched_disc%d.bin' % d, 'rb') as f:
            while need > 0:
                f.seek(s * SECT + 16)
                c = f.read(min(DATA, need))
                if not c:
                    break
                out += c
                need -= len(c)
                s += 1
        files[key] = [lba, bytearray(out[:size])]
    data = files[key][1]
    for off, t in items:
        de = T[t]
        eb = t.encode('latin1')
        db = de.encode('latin1')
        if len(db) > len(eb):
            print('BUDGET %r -> %r (%d>%d)' % (t, de, len(db), len(eb)))
            skipped += 1
            continue
        if bytes(data[off:off + len(eb)]) != eb:
            skipped += 1
            continue
        end = off + len(eb)
        data[off:off + len(db)] = db
        fill = off + len(db)
        for k in range(fill, end):
            data[k] = 0x00 if k == fill else 0xFF
        done += 1
for (d, name), (lba, data) in files.items():
    with open('_work/patched_disc%d.bin' % d, 'r+b') as f:
        for k in range((len(data) + DATA - 1) // DATA):
            f.seek((lba + k) * SECT + 16)
            f.write(data[k * DATA:(k + 1) * DATA])
print('replaced=%d skipped=%d files=%d' % (done, skipped, len(files)))
