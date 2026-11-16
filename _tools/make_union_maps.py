# Build union maps for the remaining disc-specific groups:
# 1) BTL_T0/C2/C52/X0/B5 (identical across discs 2-4) -> one union map
# 2) TWN_E059_d2 + TWN_CARA_d4 (same content, both 56 unique)
import csv
import os

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def load_todo(path):
    out = []
    for ln in open(path, encoding='latin1'):
        ln = ln.rstrip('\r\n')
        if ln and not ln.startswith('file;'):
            out.append(ln)
    return out


# 1) BTL union
btl_union = {}
for name in ('BTL_T0_FNT_d2', 'BTL_C2_FNT_d2', 'BTL_C52_FNT_d2',
             'BTL_X0_FNT_d2', 'BTL_B5_FNT_d2'):
    p = f'_work/menu_de/{name}_map_todo.csv'
    if not os.path.exists(p):
        continue
    for ln in load_todo(p):
        en = ln[:-1]  # strip trailing ';'
        btl_union.setdefault(en, True)
out = '_work/menu_de/BTL_REST_map_todo.csv'
with open(out, 'w', encoding='latin1', newline='') as fh:
    for en in sorted(btl_union):
        fh.write('%s;\n' % en)
print('BTL union unique:', len(btl_union), '->', out)

# 2) TWN_E059_d2 == TWN_CARA_d4 ?
a = {ln[:-1] for ln in load_todo('_work/menu_de/TWN_E059_PRG_d2_map_todo.csv')}
b = {ln[:-1] for ln in load_todo('_work/menu_de/TWN_CARA_PRG_d4_map_todo.csv')}
print('TWN_E059_d2 == TWN_CARA_d4 sets:', a == b, len(a), len(b))
if a != b:
    u = a | b
    with open('_work/menu_de/TWN_E059CARA_map_todo.csv', 'w',
              encoding='latin1', newline='') as fh:
        for en in sorted(u):
            fh.write('%s;\n' % en)
    print('union ->', len(u))

# 3) SNB.MCB sample (small)
for ln in load_todo('_work/menu_de/SNB_MCB_d2_map_todo.csv')[:5]:
    print('SNB sample:', repr(ln))
