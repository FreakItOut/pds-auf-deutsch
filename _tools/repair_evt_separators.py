#!/usr/bin/env python3
"""
Generic repair for batch CSVs where lines were written as 'EN,DE' (comma
instead of ';'). Uses the known EN string list to find the EN prefix,
inserts the missing ';', rewrites the batch file, and reports.
"""
import glob, json

# build EN set from the offsets json (authoritative)
disc = set()
for d in (1, 2, 3, 4):
    try:
        j = json.load(open('_work/evt_offsets_disc%d.json' % d, encoding='utf-8'))
        disc |= {e['text'] for e in j['entries']}
    except FileNotFoundError:
        pass
en_sorted = sorted(disc, key=len, reverse=True)


def fix_line(line):
    """Return fixed 'EN;DE' line or None if unrepairable."""
    # try exact EN prefix match (longest first)
    for en in en_sorted:
        if line.startswith(en):
            rest = line[len(en):]
            rest = rest.lstrip(',').lstrip(' ') if rest.startswith(',') or rest.startswith(' ') else rest
            if rest:
                return f'{en};{rest.strip()}'
            return None
    # try normalized match (strip trailing commas from EN side)
    for en in en_sorted:
        cand = en.rstrip(',') + ','
        if line.startswith(cand):
            rest = line[len(cand):].strip()
            if rest:
                return f'{en};{rest}'
    return None


import sys
total_fixed = 0
for path in sorted(glob.glob('_work/evt_batch*.csv')):
    if path.endswith('_norm.csv'):
        continue
    lines = open(path, encoding='latin1').read().splitlines()
    fixed = 0
    for i, line in enumerate(lines):
        if not line or line.startswith('#') or ';' in line:
            continue
        r = fix_line(line)
        if r:
            lines[i] = r
            fixed += 1
        else:
            print(f'  UNFIXABLE {path}:{i+1}: {line[:60]}')
    if fixed:
        open(path, 'w', encoding='latin1', newline='').write('\n'.join(lines) + '\n')
    total_fixed += fixed
    if fixed:
        print(f'{path}: fixed {fixed} separator lines')
print(f'total fixed: {total_fixed}')
