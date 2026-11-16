def dump(fn, lo, hi):
    rows = []
    for line in open('_work/subtitles/' + fn, encoding='latin1'):
        p = line.rstrip('\r\n').split(';')
        if len(p) >= 6:
            rows.append(p)
    print('#### %s %d-%d' % (fn, lo, hi))
    for p in rows:
        uid = int(p[0])
        if lo <= uid <= hi:
            print('%4d len=%2d | %r' % (uid, len(p[4]), p[4]))
            print('           de=%r' % p[5])

dump('TWN_E022_PRG_de.csv', 0, 60)
dump('TWN_CAMP_PRG_de.csv', 20, 26)
dump('TWN_CAMP_PRG_de.csv', 35, 40)
dump('TWN_CAMP_PRG_de.csv', 50, 58)
dump('TWN_CAMP_PRG_de.csv', 109, 114)
dump('TWN_CAMP_PRG_de.csv', 160, 174)
dump('TWN_CAMP_PRG_de.csv', 344, 348)
dump('TWN_CAMP_PRG_de.csv', 376, 382)
dump('TWN_CAMP_PRG_de.csv', 500, 504)
