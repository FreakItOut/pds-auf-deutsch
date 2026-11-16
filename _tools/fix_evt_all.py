# -*- coding: utf-8 -*-
# Vollstaendige EVT-Korrekturen (alle Filme) - EN-Key -> neues DE.
import io
import subprocess
import sys

sys.stdout.reconfigure(encoding='latin1')
MAP = '_work/evt_de_map.csv'
FIX = {
    'Not much... at all.': 'Gar nicht viel...',
    'The surprise we left at the Capital':
        'Die Ueberraschung in der Hauptstadt',
    "I've got to find my Captain. ": 'Muss meinen Captain finden.',
    'Captain, what is this?': 'Captain, was ist das?',
    'Captain!': 'Captain!',
    'Captain?': 'Captain?',
    'Captain!!': 'Captain!!',
    'Our side?': 'Wirklich?',
    "he killed my Captain and my friends!":
        'Er toetete Captain und Freunde!',
    'If we control the Tower, we will': 'Herrscht der Turm, dann wird',
    'control the world.': 'die Welt unser.',
    'Crush him before he reaches the Tower.':
        'Zerquetscht ihn vor seiner Ankunft.',
    'our Capital was reduced to dust.':
        'wurde die Hauptstadt zu Staub.',
    'You survived... I saw you fall...':
        'Du lebst... ich sah dich fallen.',
    'They are heading north,': "Sie geh'n nach Norden,",
    'Special Force of the Empire...':
        'Spezialkraefte des Reichs...',
    "I've heard of a renegade officer":
        'Hoerte von einem Offizier,',
    'who leads the Black Fleet...':
        'der die Flotte fuehrt...',
    "I'm afraid... it's him...": 'Ich fuerchte: er ist es.',
    'In... my pocket...': 'Meine Tasche...',
    'This is the work of those monsters.':
        'Das ist das Werk jener Monster.',
    'So that\'s how you met': 'So trafst du deinen',
    'your dragon...': 'Drachen...',
    'Of course, if there were': 'Natuerlich, gaebe es',
    "Gods, these villagers wouldn't":
        'Goetter, waeren diese Leute',
    'have been ripped to pieces': 'nicht zerfetzt worden',
    'in a feeding frenzy.': 'im Fressrausch.',
    'that dragons have another origin.':
        'dass Drachen anders entstanden.',
    'They believe dragons are demons':
        'Sie glauben, Drachen sind',
    'that rose from hell and': 'Daemonen der Hoelle,',
    'left the Ancient Age in ruins.':
        'die die Vorzeit zerstoerten.',
    'Folklore can be twisted to trick':
        'Sagen verdreht man, damit',
    'people into fearing their saviors?':
        'Menschen ihre Retter fuerchten?',
    'He killed my friends.': 'Er toetete Freunde.',
    'and half of them are crazy.':
        'die Haelfte ist verrueckt.',
    'known only as the Divine Visitor.':
        'bekannt als Goettlicher Besucher.',
    'in the ancient records anyway.':
        'in den alten Schriften.',
    "Sorry, but that's all I can say...":
        'Leider, mehr kann ich nicht sagen.',
    'An Imperial squadron!?': 'Eine Reichsstaffel!?',
    'A lesser man would have talked...':
        'Ein Schwaechterer haette geredet.',
    "It's time.": 'Jetzt.',
    'Can you stand?': 'Aufstehen?',
    "You're tougher than you look.":
        'Staerker als du aussiehst.',
    "We'll get out through the deck.":
        "Wir steigen uebers Deck aus.",
    'Thanks for activating': 'Danke, du wecktest',
    "Don't shoot!": 'Halt!',
    'lower the weapon or not.': 'sie senke oder nicht.',
    "if you're willing to show": 'wenn du mir den Pfad',
    'me the way to the Tower.': 'zum Turm zeigst.',
    'is already sealed.': 'ist versiegelt.',
    'I suggest you concentrate': 'Ich rate dir, dich aufs',
    'on getting out of here alive.':
        'Rauskommen zu konzentrieren.',
    'My legs are pinned, so': 'Beine stecken fest,',
    'but when we get out of here,':
        'und wenn wir hier raus sind,',
    'I want some answers.': 'Ich will Antworten.',
    'More of those creatures are coming.':
        'Noch mehr Kreaturen kommen.',
    'you can handle this.': 'schaffst du das.',
    "We're safe now,": 'Jetzt sicher,',
    "to the creatures we've": 'den Kreaturen, die',
    'been fighting.': 'wir jagen.',
    'But as soon as you were found,':
        'Kaum warst du gefunden,',
    'we were betrayed.': 'verriet man uns.',
    'by our own fleet...': 'durch eigene...',
    'You are supposed to apologize':
        'In so einer Zeit sollte man',
    'at a time like this.': 'sich entschuldigen.',
    'They are not creatures': 'Sie sind keine Wesen,',
    'easily handled by ordinary men.':
        'die Maenner leicht zaehmen.',
    'you are the dragon rider that':
        'du bist der Drachenreiter,',
    'has caused me so much trouble.':
        'der mir so viel Aerger machte.',
    'then you must also remember': 'dann weisst du auch,',
    'You murdered everyone!!': 'Du brachtest alle um!!',
    'To obtain the key element, Azel...':
        'Um das Element Azel zu holen...',
    'Again, I am in your debt.': 'Wieder schulde ich dir.',
    'No man should wield': 'Niemand darf solche',
    'such power...': 'Macht tragen',
    'or what we call the Tower.': 'oder was wir Turm nennen.',
    'mankind from extinction.': 'der Menschheit.',
    'you must have learned': 'hast du gelernt,',
    "It's nearly impossible to destroy": 'Kaum zerstoerbar:',
    'the Tower from the outside.': 'der Turm von aussen.',
    'was one of those monsters.': 'eines der Monster war.',
    'As for the hunter,': 'Fuer den Jaeger',
    "It's a trap!": 'Die Falle!',
    'Azel is still...': 'Azel bleibt...',
    'I will destroy this Tower.': 'Ich zerstoere den Turm!',
    "I won't let you.": 'Nicht mit mir!',
    'I am... the only one...': 'Ich bin die Einzige...',
    'that can destroy the Tower.':
        'die den Turm loeschen kann.',
    "I promise... I'll come back for you!":
        'Versprochen... Ich komm wieder!',
    "Aren't you the Divine Visitor?": 'Bist du der Goettliche?',
    'Es ist Zeit.': 'Es ist Zeit.',
    'A voyage without a destination...':
        'Reise ohne Ziel...',
}

lines = io.open(MAP, encoding='latin1').read().split('\n')
out = []
done = 0
budget = []
for ln in lines:
    q = ln.rstrip('\r\n')
    if ';' not in q or q.startswith('#'):
        out.append(ln)
        continue
    en, de = q.split(';', 1)
    if en in FIX and FIX[en] != de:
        new = FIX[en]
        if len(new.encode('latin1')) > len(en.encode('latin1')):
            budget.append((en, new, len(new), len(en)))
            out.append(ln)
            continue
        out.append(en + ';' + new)
        done += 1
    else:
        out.append(ln)
io.open(MAP, 'w', encoding='latin1', newline='').write('\n'.join(out))
print('evt fixes', done)
for b in budget:
    print('BUDGET %r -> %r %d>%d' % b)
r = subprocess.run([sys.executable, '_tools/patch_evt_subtitles.py',
                    '--disc', 'all', '--csv', MAP])
print('patch rc=%d' % r.returncode)
