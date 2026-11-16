import sys, io
sys.stdout.reconfigure(encoding='latin1')
src = open('_tools/evt_intro_fix.py', encoding='latin1').read()
tree = ast_tree = __import__('ast')
for node in tree.walk(tree.parse(src)):
    if isinstance(node, tree.Assign) and getattr(node.targets[0], 'id', '') == 'FIX':
        FIX = eval(tree.get_source_segment(src, node).replace('FIX = ', '', 1))
        break

path = '_work/evt_de_map.csv'
lines = io.open(path, encoding='latin1').read().split('\n')
tested = {}
for line in lines:
    if ';' not in line:
        continue
    en, de = line.split(';', 1)
    k = en.rstrip()
    for probe in ('Go on...', 'Water?', 'have been ripped to pieces',
                  "He's a lunatic with a plan", 'of the Ancient Age.'):
        if k == probe:
            tested[probe] = (de, FIX.get(probe))
for k, (de, want) in tested.items():
    print(repr(k), 'disc_de=%r' % de, 'FIX=%r' % want, 'eq' if de == want else 'DIFF')
print('lines total', len(lines))
