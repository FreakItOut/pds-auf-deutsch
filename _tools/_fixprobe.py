import sys
import ast
sys.stdout.reconfigure(encoding='latin1')
src = open('_tools/evt_intro_fix.py', encoding='latin1').read()
tree = ast.parse(src)
for node in ast.walk(tree):
    if isinstance(node, ast.Assign) and getattr(node.targets[0], 'id', '') == 'FIX':
        body = ast.get_source_segment(src, node)
        d = eval(body.replace('FIX = ', '', 1))
        print('len FIX:', len(d))
        for k in ('Go on...', 'Wanna bite?', 'have been ripped to pieces',
                  "He's a lunatic with a plan", 'Water?', 'of the Ancient Age.'):
            print(repr(k), 'in?', k in d, repr(d.get(k)))
