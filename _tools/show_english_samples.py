import csv
import collections

rows = [r for r in csv.DictReader(open('_work/english_remaining_disc1.csv',
                                       encoding='latin1'), delimiter=';')]
seen = collections.Counter(r['text'] for r in rows)
for f in ('MENUEN.FNT', 'TUTORIAL.CGB', 'TWN_SEEK.PRG', 'FLD_A7.FNT',
          'MENU.SCB', 'ITEM.FNT', 'SAVE.FNT', 'SHOP.FNT', 'WORLDMAP.FNT',
          'MENUBK.FNT'):
    rr = [r for r in rows if r['file'] == f and seen[r['text']] <= 3
          and ' ' in r['text'].strip()]
    print('=== %s (unique-ish with spaces: %d) ===' % (f, len(rr)))
    for r in rr[:45]:
        print('  %r' % r['text'])
    print()
