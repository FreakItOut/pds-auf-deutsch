# -*- coding: utf-8 -*-
import ast
import io
import pprint
import sys

sys.stdout.reconfigure(encoding='latin1')
src = io.open('_tools/patch_extra.py', encoding='utf-8').read()
tree = ast.parse(src)
T = None
for node in tree.body:
    if isinstance(node, ast.Assign):
        for t in node.targets:
            if isinstance(t, ast.Name) and t.id == 'T':
                T = ast.literal_eval(node.value)
assert T
out = io.open('_tools/extra_de.py', 'w', encoding='utf-8', newline='\n')
out.write('# -*- coding: utf-8 -*-\n')
out.write('# EN -> DE der nachtraeglich uebersetzten Texte.\n')
out.write('T = ' + pprint.pformat(T, width=78) + '\n')
out.close()
print('entries', len(T))
