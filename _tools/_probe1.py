rows = []
f = open('_work/menu_de/TWN_SEEK_PRG_d4_map.csv', encoding='latin1')
next(f)
for line in f:
    if not line.strip():
        continue
    p = line.rstrip('\r\n').split(';')
    if len(p) >= 2:
        en, de = p[0], p[1]
        if len(de.encode('latin1')) > len(en.encode('latin1')):
            rows.append((en, de))
f.close()
print('too long:', len(rows))
for en, de in rows[:25]:
    print('%3d>%3d  %r -> %r' % (len(de), len(en), en[:60], de[:60]))
