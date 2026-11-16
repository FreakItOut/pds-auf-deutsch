import json

disc = set()
for d in (1, 2, 3, 4):
    j = json.load(open('_work/evt_offsets_disc%d.json' % d, encoding='utf-8'))
    disc |= {e['text'] for e in j['entries']}

OUT = {
    'Edge, can I count on you?': 'kann ich dir vertrauen?',
    'Edge, do you remember the village': 'Edge, erinnerst du das Dorf,',
    'Edge, my boy,': 'Mein Junge,',
    'Empire, the better off you are.': 'Je groesser das Imperium, desto',
}

out_lines = []
for key, de in OUT.items():
    if key in disc and len(de) <= len(key):
        out_lines.append(f'{key};{de}')
open('_work/evt_batch15_norm.csv', 'w', encoding='latin1', newline='').write('\n'.join(out_lines) + '\n')
print('written batch15_norm:', len(out_lines))

bad = 0
for line in out_lines:
    en, de = line.split(';', 1)
    if en not in disc:
        print('NOEN', repr(en))
        bad += 1
    if len(de) > len(en):
        print('LONG', repr(de))
        bad += 1
print('batch15 problems:', bad)
