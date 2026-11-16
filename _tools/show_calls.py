# -*- coding: utf-8 -*-
# Zeigt Aufrufstellen von printf_small/printf_large mit geladenen String-
# Zeigern und liest den Text aus der Overlay-Datei.
import re
import sys

sys.stdout.reconfigure(encoding='latin1')
path = sys.argv[1]
fn = sys.argv[2]
lines = open(path, encoding='utf-8', errors='ignore').read().splitlines()
idx = [i for i, l in enumerate(lines) if fn in l]
print('calls', len(idx))
for i in idx[:8]:
    print('--- line', i + 1)
    for j in range(max(0, i - 22), i + 3):
        print('%5d %s' % (j + 1, lines[j]))
