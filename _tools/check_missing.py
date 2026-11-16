import os
os.chdir(r'C:\Users\FreakItOut\Documents\Panzer Dragoon Saga Übersetzung')

missing_keys = ["(It's a step ladder.", "(It's a dingy looking hammock.", "(It is full of grain.", "(It's a waterproof box.", "Never seen this type of nut before.", "This neutralizes the monsters' acid.)", "(Only the pedestal remains.", "It's made from a monster's shell.", "(That pot is big!"]

with open('_work/menu_de/TWN_SEEK_PRG_d4_map.csv', encoding='latin1') as f:
    map_lines = f.read().splitlines()

map_ens = [line.split(';')[0] for line in map_lines if ';' in line]

for mk in missing_keys:
    mk_stripped = mk.strip().rstrip('.)').strip()
    found = False
    for en in map_ens:
        en_stripped = en.strip().rstrip('.)').strip()
        if en_stripped == mk_stripped:
            found = True
            print('MATCH: %r -> %r' % (en, mk))
            break
    if not found:
        print('NO MATCH: %r' % mk)
        # show close candidates
        for en in map_ens:
            if mk_stripped[:20] in en or en[:20] in mk_stripped:
                print('   CAND: %r' % en)
                break