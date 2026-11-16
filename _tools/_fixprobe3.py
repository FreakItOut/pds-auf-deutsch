# instrumented re-run of the evt_intro_fix loop for failing keys
import sys, io
sys.stdout.reconfigure(encoding='latin1')
src = open('_tools/evt_intro_fix.py', encoding='latin1').read()
tr = __import__('ast')
FIX = None
for node in tr.walk(tr.parse(src)):
    if isinstance(node, tr.Assign) and getattr(node.targets[0], 'id', '') == 'FIX':
        FIX = eval(tr.get_source_segment(src, node).replace('FIX = ', '', 1))
        break

path = '_work/evt_de_map.csv'
lines = io.open(path, encoding='latin1').read().split('\n')
want = {'Go on...', 'Wanna bite?', 'Water?', "He's a lunatic with a plan",
        'have been ripped to pieces', 'the utopian civilization.'}
out = []
report = []
for n, line in enumerate(lines):
    if ';' not in line:
        out.append(line)
        continue
    en, de = line.split(';', 1)
    k = en.rstrip()
    if k in want:
        new = FIX.get(k)
        applied = False
        if new is not None and len(new.encode('latin1')) <= len(k.encode('latin1')) and de.strip() != new:
            line = en + ';' + new
            applied = True
        report.append((n, en.rstrip(), repr(de), applied))
    out.append(line)
io.open(path, 'w', encoding='latin1', newline='\n').write('\n'.join(out) + '\n')
for r in report:
    print(r)
