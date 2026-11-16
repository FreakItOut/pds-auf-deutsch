# dump specific chain contexts into a review file (CAMP/RUIN/SEEK broken filter)
import sys
import io
import re
sys.stdout.reconfigure(encoding='latin1')
t = open('_work/review_fixes/chain_context.txt',
         encoding='latin1').read().split('====')
suspects = []
for blk in t:
    if not blk.strip():
        continue
    # look for specific patterns that hint broken compositions
    lines = [x for x in blk.splitlines() if x.strip()]
    de_lines = []
    for l in lines:
        if l.startswith(('  A(', '  B(')) and '/ ' in l:
            de = l.split('/ ', 1)[1].strip().strip(chr(39))
            de_lines.append(de.strip() if isinstance(de, str) else str(de))
    if len(de_lines) == 2:
        a, b = de_lines
        # criterion 1: DE2 shorter than 6 chars (likely truncated)
        if len(b) < 6 and b and not b.endswith(('!', '?', '.', '-', ',')):
            suspects.append(blk)
            continue
        # criterion 2: DE2 ends with a trailing article-word (no noun)
        if b.split() and b.split()[-1].lower() in ('das', 'der', 'die', 'dem',
                                                  'den', 'ein', 'eine', 'fuer',
                                                  'mit', 'von', 'aus', 'zu'):
            suspects.append(blk)
            continue
        # criterion 3: DE2 begins lowercase and DE1 ends with a dot
        if a and a[-1] in '.!?' and b and b[0].islower():
            suspects.append(blk)
            continue
        # criterion 4: DE1 ends with a dangling prep and DE2 does not continue
        if a and a.split()[-1].lower() in ('fuer', 'mit', 'von', 'aus', 'zu',
                                           'durch', 'imm', 'in', 'ueber',
                                           'unter') and not b:
            suspects.append(blk)
            continue
with open('_work/review_fixes/broken_chain2.txt', 'w',
          encoding='latin1', newline='\n') as f:
    for blk in suspects:
        f.write('=====' + blk + '\n')
print('suspicious blocks:', len(suspects))
for blk in suspects[:40]:
    print('=====' + blk[:500])
    print('---')
