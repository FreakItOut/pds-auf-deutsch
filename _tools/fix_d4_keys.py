import io

p = '_work/menu_de/TWN_SEEK_PRG_d4_map.csv'
s = io.open(p, encoding='latin1').read()

fixes = [
    ("(It's a step ladder.;", "(It's a step ladder.)"),
    ("(It's a dingy looking hammock.;", "(It's a dingy looking hammock.)"),
    ("(It is full of grain.;", "(It is full of grain.)"),
    ("(It's a waterproof box.;", "(It's a waterproof box.)"),
    ("(Never seen this type of nut before.;", "(Never seen this type of nut before.)"),
    ("This neutralizes the monsters' acid.);", "This neutralizes the monsters' acid.)"),
    ("(Only the pedestal remains.;", "(Only the pedestal remains.)"),
    ("(It's made from a monster's shell.;", "(It's made from a monster's shell.)"),
    ("(That pot is big!;", "(That pot is big!)"),
]
for old, new in fixes:
    if old in s:
        s = s.replace(old, new)
    else:
        print('NOT FOUND:', repr(old[:40]))

io.open(p, 'w', encoding='latin1', newline='').write(s)
print('done')
