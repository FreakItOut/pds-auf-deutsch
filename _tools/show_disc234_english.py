import csv
import collections

for d in (2, 3, 4):
    rows = [r for r in csv.DictReader(open(f'_work/english_remaining_disc{d}.csv',
                                           encoding='latin1'), delimiter=';')]
    seen = collections.Counter(r['text'] for r in rows)
    per = collections.defaultdict(list)
    for r in rows:
        if seen[r['text']] <= 3 and ' ' in r['text'].strip():
            per[r['file']].append(r['text'])
    print('=== disc %d: files with unique-ish spaced English ===' % d)
    for f, texts in sorted(per.items(), key=lambda kv: -len(kv[1]))[:18]:
        print('  %-16s %4d  e.g. %r' % (f, len(texts), texts[0][:48]))
    print()
