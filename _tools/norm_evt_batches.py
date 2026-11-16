#!/usr/bin/env python3
"""
Normalize EVT batch CSV keys against the exact on-disc MOVIE.DAT string set:
- fixes EN keys (comma variants) by unique prefix/normal match,
- reports entries still unmatched and DE lines that are too long,
- writes normalized files as _work/evt_batchN_fixed.csv.
"""
import json, glob, sys, os

disc = set()
for d in (1, 2, 3, 4):
    try:
        j = json.load(open(f'_work/evt_offsets_disc{d}.json', encoding='utf-8'))
        disc |= {e['text'] for e in j['entries']}
    except FileNotFoundError:
        pass

def norm(en):
    if en in disc:
        return en
    for cand in (en.rstrip(','), en + ','):
        if cand in disc:
            return cand
    # fuzzy: compare without commas
    key = en.replace(',', '').replace('  ', ' ')
    hits = [t for t in disc if t.replace(',', '').replace('  ', ' ') == key]
    if len(hits) == 1:
        return hits[0]
    # prefix match
    hits = [t for t in disc if t.startswith(en[:min(20, len(en))])]
    if len(hits) == 1:
        return hits[0]
    return None

for path in sorted(glob.glob('_work/evt_batch*.csv')):
    if path.endswith('_norm.csv') or path.endswith('_norm_norm.csv'):
        continue
    # never overwrite existing normalized output (protects downstream fixes)
    out_path = path.replace('.csv', '_norm.csv')
    if os.path.exists(out_path):
        print(f'{path}: SKIP -> {out_path} exists')
        continue
    miss, toolong, ok = [], [], 0
    out = []
    for ln, line in enumerate(open(path, encoding='latin1'), 1):
        line = line.rstrip('\r\n')
        if not line or line.startswith('#'):
            out.append(line)
            continue
        if line.count(';') < 1:
            miss.append((ln, line, 'no separator ;'))
            continue
        en, de = line.split(';', 1)
        en, de = en.strip(), de.strip()
        real = norm(en)
        if real is None:
            miss.append((ln, en[:70], 'no disc match'))
            out.append(line)
            continue
        if len(de) > len(real):
            toolong.append((ln, len(de), len(real), de))
        ok += 1
        out.append(f'{real};{de}')
    open(out_path, 'w', encoding='latin1', newline='').write(
        '\n'.join(out) + '\n')
    print(f'{path}: ok={ok} miss={len(miss)} toolong={len(toolong)} -> {out_path}')
    for m in miss:
        print(f'   MISS line {m[0]}: {m[1]}" | {m[2]}')
    for t in toolong:
        print(f'   LONG line {t[0]}: de_len={t[1]} en_len={t[2]} "{t[3]}"')
