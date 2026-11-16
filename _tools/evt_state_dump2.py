# CORRECT state dump: use the patcher's own sector-view math (lba from JSON)
import sys, json
sys.stdout.reconfigure(encoding='latin1')

SECTOR_SIZE, DATA_SIZE, HDR = 2352, 2048, 16


def read_sector(f, n):
    f.seek(n * SECTOR_SIZE)
    raw = f.read(SECTOR_SIZE)
    if len(raw) < SECTOR_SIZE:
        return b''
    mode = raw[15]
    if mode == 1:
        return raw[16:16 + 2048]
    elif mode == 2:
        sub = raw[18]
        return raw[24:24 + 2324] if (sub & 0x20) else raw[24:24 + 2048]
    return raw[16:16 + 2048]


dnum = int(sys.argv[1]) if len(sys.argv) > 1 else 1
ents = json.load(open('_work/evt_offsets_disc%d.json' % dnum, encoding='utf-8'))['entries']
dat_e = [e for e in ents if e['src'].startswith('MOVIE.DAT')]
e0 = dat_e[0]
k0 = e0['foff']
lba = (e0['off'] - HDR - (k0 % 2048)) // SECTOR_SIZE - (k0 // 2048)
size = 27856
nsec = (size + DATA_SIZE - 1) // DATA_SIZE
f = open('_work/patched_disc%d.bin' % dnum, 'rb')
dat = b''.join(read_sector(f, lba + i) for i in range(nsec))[:size]
f.close()

groups = {}
for e in dat_e:
    groups.setdefault(e['src'], []).append(e)
out = open('_work/review_fixes/evt_cd1_state2.txt', 'w', encoding='latin1', newline='\n')
tot = untr = 0
for src in sorted(groups, key=lambda s: int(s.split('g')[1])):
    out.write('===== %s\n' % src)
    for e in groups[src]:
        fo = e['foff']
        end = dat.find(b'\x00', fo)
        cur = dat[fo:end].decode('latin1', 'replace')
        tot += 1
        m = ' UNTR' if cur == e['text'] else ''
        if m:
            untr += 1
        out.write('%8d EN=%r\n' % (fo, e['text']))
        out.write('        DE=%r%s\n' % (cur, m))
out.close()
print('groups=%d entries=%d de==en=%d' % (len(groups), tot, untr))
