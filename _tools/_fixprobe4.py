# For every FIX key not yet applied (de != FIX), print exact EN budget so the
# final shortened DE can be crafted against real numbers.
import sys, io
sys.stdout.reconfigure(encoding='latin1')
src = open('_tools/evt_intro_fix.py', encoding='latin1').read()
tr = __import__('ast')
FIX = None
for node in tr.walk(tr.parse(src)):
    if isinstance(node, tr.Assign) and getattr(node.targets[0], 'id', '') == 'FIX':
        FIX = eval(tr.get_source_segment(src, node).replace('FIX = ', '', 1))
        break
del FIX['I was taught']  # wrong key spelling; real EN has '...'
lines = io.open('_work/evt_de_map.csv', encoding='latin1').read().split('\n')
by = {}
for line in lines:
    if ';' not in line:
        continue
    en, de = line.split(';', 1)
    by.setdefault(en.rstrip(), de)
pending = {k: v for k, v in FIX.items() if k in by and by[k] != v}
print('pending:', len(pending))
for k in sorted(pending):
    print('%3d | %3d->%3d | %r' % (len(k), len(k), len(pending[k]), k))
