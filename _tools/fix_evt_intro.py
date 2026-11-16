# -*- coding: utf-8 -*-
# Kuratierte Korrekturen der Intro-FMV-Untertitel (EN-Key -> DE).
import io
import subprocess
import sys

sys.stdout.reconfigure(encoding='latin1')
MAP = '_work/evt_de_map.csv'
FIX = {
    'of the action?': 'des Trubels?',
    'We were hired by the Empire': 'Das Reich engagierte uns,',
    'will only get you killed.': 'kostet dich das Leben.',
    'The survivors live in fear': 'Die Ueberlebenden leben in',
    'of the biological weapons': 'Angst vor Biowaffen,',
    'created by ancient technologies.': 'die alte Technik schuf.',
    'with the technology of the lost': 'mit der Technik der verlorenen',
    'civilization on their side.': 'Kultur auf ihrer Seite.',
    'ancient weapons excavated from': 'Waffen aus den',
    'the dormant ruins.': 'schlafenden Ruinen',
    'The people rejoiced, believing that': 'Die Leute jubelten: Menschen',
    'humans could live without fear.': 'koennen ohne Angst leben.',
    'The Empire declared war on its': 'Das Reich erklaerte seinen',
    'too discovered the ancient weapons.': 'auch sie fanden die alten Waffen.',
    'The battles became epic struggles.': 'Die Kaempfe wurden episch.',
    'Arwen, now is the time for rebellion.':
        'Arwen, nun ist die Zeit zum Aufstand.',
    'Run for your life!': 'Renn! Schnell weg!',
    "This isn't the usual half-breed.":
        'Kein gewoehnlicher Mischling!',
    'Our side?': 'Wirklich?',
    'Zastava, leave them be.': 'Zastava, lass sie.',
    'You saw her?': 'Sie gesehen?',
    'Hurry!  The Command Fleet': 'Beeil dich! Die Flotte',
    'Damn!  Come back... here...': 'Komm zurueck... hierher...',
    'The Capital of the Empire.': 'Des Reiches Hauptstadt.',
    'In a blinding flash,': 'In grellem Blitz,',
    'The Academy reported that the': 'Die Akademie meldete: Die',
    'underground ruins were created with':
        'unterirdischen Ruinen entstanden',
    'technologies beyond our understanding.':
        'mit unbegreiflicher Technik.',
    'It was Craymen!': "Craymen war's!",
    'If you remember me,': 'Erinnerst du dich,',
    'You look surprised to see me here.':
        'Du schaust wohl ueberrascht.',
}

lines = io.open(MAP, encoding='latin1').read().split('\n')
out = []
done = 0
for ln in lines:
    q = ln.rstrip('\r\n')
    if ';' not in q or q.startswith('#'):
        out.append(ln)
        continue
    en, de = q.split(';', 1)
    if en in FIX:
        new = FIX[en]
        if len(new.encode('latin1')) > len(en.encode('latin1')):
            print('BUDGET %r %d>%d' % (en, len(new), len(en)))
            out.append(ln)
            continue
        out.append(en + ';' + new)
        done += 1
    else:
        out.append(ln)
io.open(MAP, 'w', encoding='latin1', newline='').write('\n'.join(out))
print('evt intro fixes', done)
r = subprocess.run([sys.executable, '_tools/patch_evt_subtitles.py',
                    '--disc', 'all', '--csv', MAP])
print('patch rc=%d' % r.returncode)
