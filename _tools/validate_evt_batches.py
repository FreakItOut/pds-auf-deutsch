#!/usr/bin/env python3
"""
Validate EVT translation batches: checks EN keys exist in the disc offsets
JSON, len(DE) <= len(EN), ASCII-only DE, and reports coverage.

Usage: python validate_evt_batches.py
"""
import json, glob, sys

EN_FILE = '_work/evt_subtitle_strings_en.txt'
en_set = set()
for l in open(EN_FILE, encoding='latin1').read().splitlines():
    if not l:
        continue
    en_set.add(l.rsplit(',', 2)[0].strip())
json_entries = {}
for d in (1, 2, 3, 4):
    try:
        j = json.load(open(f'_work/evt_offsets_disc{d}.json', encoding='utf-8'))
        json_entries[d] = {e['text'] for e in j['entries']}
    except FileNotFoundError:
        pass

all_en_on_disc = set.intersection(*json_entries.values()) if json_entries else set()

total, bad_len, bad_ascii, not_en = 0, 0, 0, 0
for path in sorted(glob.glob('_work/evt_batch*.csv')):
    for n, line in enumerate(open(path, encoding='latin1'), 1):
        line = line.rstrip('\r\n')
        if not line or line.startswith('#'):
            continue
        en, de = line.split(';', 1)
        en, de = en.strip(), de.strip()
        total += 1
        ok = True
        if len(de) > len(en):
            print(f"{path}:{n} TOO LONG ({len(de)}>{len(en)}): {de}")
            bad_len += 1; ok = False
        if any(ord(c) > 126 or c == '#' for c in de):
            print(f"{path}:{n} NON-ASCII in DE")
            bad_ascii += 1; ok = False
        if en not in en_set or en not in all_en_on_disc:
            print(f"{path}:{n} EN not on disc: {en[:60]}")
            not_en += 1; ok = False
    # done file
print(f"\nBatches validated: {total} entries, "
      f"too_long={bad_len}, non_ascii={bad_ascii, }, unknown_en={not_en}")
