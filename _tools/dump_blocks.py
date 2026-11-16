# Exact rows with len budgets for the misaligned blocks
def dump(fn, lo, hi):
    rows = []
    for line in open('_work/subtitles/' + fn, encoding='latin1'):
        p = line.rstrip('\r\n').split(';')
        if len(p) >= 6:
            rows.append(p)
    print('#### %s' % fn)
    for p in rows:
        uid = int(p[0])
        if lo <= uid <= hi:
            print('%4d len=%2d | %r' % (uid, len(p[4]), p[4]))
            print('           de=%r' % p[5])

dump('TWN_CAMP_PRG_de.csv', 545, 585)
dump('TWN_RUIN_PRG_de.csv', 262, 335)
dump('TWN_RUIN_PRG_de.csv', 415, 425)
dump('TWN_RUIN_PRG_de.csv', 500, 512)
print()
# JIRI + E022 length check for planned fixes
for fn in ['TWN_JIRI_PRG_de.csv']:
    rows = []
    for line in open('_work/subtitles/' + fn, encoding='latin1'):
        p = line.rstrip('\r\n').split(';')
        if len(p) >= 6:
            rows.append(p)
    for p in rows:
        print('%s len=%2d | %r | de=%r' % (p[0], len(p[4]), p[4][:50], p[5][:50]))
