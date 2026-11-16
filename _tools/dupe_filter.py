# quick filter: seek duplication in chain_context
import io
import re
import sys
sys.stdout.reconfigure(encoding='latin1')
txt = open('_work/review_fixes/chain_context.txt',
           encoding='latin1').read().split('====')
for block in txt:
    if not block.strip():
        continue
    lines = [l for l in block.splitlines() if l.strip()]
    if len(lines) < 3:
        continue
    de_pairs = [l for l in lines if l.startswith('  A(') or l.startswith('  B(')]
    if len(de_pairs) != 2:
        continue

    def get_de(l):
        return l.split('/ ', 1)[-1].strip()
    de_a, de_b = get_de(de_pairs[0]).rstrip('.'), get_de(de_pairs[1]).rstrip('.')
    if len(de_a) > 6 and len(de_b) > 3:
        # test if de_b is a substring / duplicate of de_a
        if de_b[:5].lower() in de_a.lower() and de_a != de_b:
            print(repr(block[:400]))
            print('---')
