# Spot-check a sample of quality-fixed strings directly in the patched disc images.
import json
import os

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

CHECK = [
    'Why did you attack me?',
    'Damn!  Come back... here...',
    'lead anything.',
    "It's you!",
    "I've got to find my Captain. ",
    'where I awoke.',
    'No one would suspect a man like me to',
    "Now, Divine One,",
    'Those bastards...',
    'This is bad... ',
    'forever.',
    "Isn't that why you kept me here?",
]

EXPECTED = {
    'Why did you attack me?': 'Warum attackierst du?',
    'Damn!  Come back... here...': 'Halt! Komm zurueck! Sofort!',
    'lead anything.': 'fuehren kann.',
    "It's you!": "Du bist's",
    "I've got to find my Captain. ": 'Ich muss meinen Chef finden.',
    'where I awoke.': 'erwachte.',
    'No one would suspect a man like me to': 'Niemand glaubt, dass ich',
    "Now, Divine One,": 'Nun, Goettlicher',
    'Those bastards...': 'Dieses Pack...',
    'This is bad... ': 'Das wird uebel.',
    'forever.': 'ewig.',
    "Isn't that why you kept me here?": 'Haeltst du mich deswegen hier?',
}

by_disc = {}
for d in (1, 2, 3, 4):
    j = json.load(open('_work/evt_offsets_disc%d.json' % d, encoding='utf-8'))
    for e in j['entries']:
        by_disc.setdefault(e['text'], []).append((d, e['off']))

bad = 0
for en in CHECK:
    if en not in by_disc:
        print('MISSING OFFSETS:', repr(en))
        bad += 1
        continue
    for d, off in by_disc[en]:
        with open('_work/patched_disc%d.bin' % d, 'rb') as fh:
            fh.seek(off)
            raw = fh.read(len(en) + 8)
        got = raw.split(b'\x00', 1)[0].decode('ascii', 'replace')
        status = 'OK ' if got == EXPECTED[en] else 'BAD'
        if got != EXPECTED[en]:
            bad += 1
        print('%s d%d %-38r -> %r' % (status, d, en, got))
print('spot-check problems:', bad)
