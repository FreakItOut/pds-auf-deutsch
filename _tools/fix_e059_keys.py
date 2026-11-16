import io
p = '_work/menu_de/TWN_E059_PRG_d2_map.csv'
s = io.open(p, encoding='latin1').read()
fixes = [
    ('(...All the valuable items are gone.;', '(...All the valuable items are gone.'),
    ("(It's a relic from the Ancient Age.;", "(It's a relic from the Ancient Age."),
    ('themselves this time.;', 'themselves this time.'),
    ("(It's Radgam, the hunter.;", "(It's Radgam, the hunter."),
]
for old, new in fixes:
    if old in s:
        s = s.replace(old, new)
    else:
        print('NOT FOUND:', repr(old[:40]))
io.open(p, 'w', encoding='latin1', newline='').write(s)
print('done')
