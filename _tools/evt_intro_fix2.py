# Intro/CD1-FMV quality pass 2: shorten the 45 values flagged TOO LONG in
# pass 1 so every key now fits its real EN budget. Cosmetic no-gain keys are
# deliberately dropped. The loop reports any remaining overage.
import sys, io
sys.stdout.reconfigure(encoding='latin1')

FIX = {
    'As for the hunter,': 'Der Jaeger, bei',
    'Asking too many questions,': 'Wer viele Fragen stellt,',
    "But that's not all.": 'Das reicht nicht.',
    "But that's...": 'Aber das...',
    "But we're not really living.": 'So richtig leben wir nicht.',
    'But...': 'Aber',
    'Craymen will pay...': 'Craymen zahlt dafuer',
    'Edge, can I count on you?': 'Edge, kann ich dir trauen?',
    'Enjoy the peace while it lasts, kid.': "Geniesse den Frieden, solange's geht",
    'Food for the monsters you awakened.': 'Futter jener Monster, die du weckst',
    'For a new beginning.': 'Fuer neuen Anfang.',
    'Go on...': 'Erzaehl.',
    'He killed my friends.': 'Er mordete Freunde.',
    "He's a lunatic with a plan": 'Verrueckter mit Plan,',
    'How is she?': 'Gings ihr?',
    'I am not...': 'Nicht ich.',
    'I am... the only one...': 'Ich bin der Einzige',
    "I don't know who is right anymore.": 'Weiss nicht mehr, wer recht hat.',
    'I expected no less from you,': 'Mehr hatte ich nicht von dir,',
    'I merely set the stage.': 'Die Buehne setzte ich.',
    'I must stay here.': 'Muss hier bleiben',
    'I need to be alone... for now...': 'Ich will allein sein...',
    'I need to find out why.': 'Ich muss wissen, warum.',
    'I want the truth...': 'Die Wahrheit!',
    "I'll guide you and the dragon": 'Ich fuehre euch samt Drachen',
    "I'm afraid... it's him...": 'Ich fuerchte: es ist er.',
    "I'm... Edge.": 'Ich... Edge',
    'If you can control a dragon,': 'Kannst du Drachen fuehren,',
    'It is now with me...': 'Jetzt hab ich ihn...',
    'Only my powers are different.': 'Nur die Kraefte sind anders.',
    'Prepare the report': 'Bereite den Report',
    'Pursue at once...': 'Verfolgt sofort',
    "That, I don't know.": 'Das weiss ich nicht',
    "The 'Divine Visitor'...": "Der 'Goettliche'...",
    'The monsters killed Craymen.': 'Craymen starb an Monstern.',
    'Then the Empire rose to power': 'Das Reich stieg zur Macht',
    'They cannot even handle': 'Sie koennen nicht mal',
    'You can control the dragon,': 'Drachen kontrollierst du,',
    'and half of them are crazy.': 'und halb davon verrueckt.',
    'attacked by those monsters.': 'von Monstern angegriffen.',
    'been fighting.': 'wir bekriegen.',
    'confirmed...': 'bestaetigt',
    'destroy this Tower.': 'den Turm zerstoeren.',
    'from my eternal sleep.': 'mich aus ewigem Schlaf',
    'have been ripped to pieces': 'Doerfler in Fresslust nicht',
    'is the dragon itself!': 'ist der Drache selbst!',
    'lead anything.': 'fuehren kann.',
    'lower the weapon or not.': 'Waffe halte oder senke.',
    'message in his own blood.': 'Nachricht aus Eigenblut.',
    'neighboring nations, but they': 'Nachbarn den Krieg, doch diese',
    'restore this world.': 'heile diese Welt.',
    'ruins and towers.': 'aktiven Ruinen.',
    'that can destroy the Tower.': 'der den Turm loeschen kann.',
    'the ancient ones': 'Alten gebaut,',
    'we need Azel.': 'braucht Azel.',
    'who the real enemy is.': 'wer der Feind ist.',
    'No one would suspect a man like me to': 'Niemand glaubt, dass ich',
    'lower the weapon or notX': None,  # marker/dup guard
    'from the past,': 'der Vorzeit,',
    'Wanna bite?': 'Hunger?',
}
FIX.pop('lower the weapon or notX')

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
