# probe: replicate patch_evt_subtitles' exact logic for the entry at foff 8180
import sys, json, struct
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


ents = json.load(open('_work/evt_offsets_disc1.json', encoding='utf-8'))['entries']
dat_e = [e for e in ents if e['src'].startswith('MOVIE.DAT')]
e0 = dat_e[0]
k0 = e0['foff']
lba = (e0['off'] - HDR - (k0 % 2048)) // SECTOR_SIZE - (k0 // 2048)
print('derived lba:', lba)
print('e0 foff%2048:', k0 % 2048, 'foff//2048:', k0 // 2048)
size = 27856
nsec = (size + DATA_SIZE - 1) // DATA_SIZE
f = open('_work/patched_disc1.bin', 'r+b')
dat = bytearray(b''.join(read_sector(f, lba + i) for i in range(nsec))[:size])
print('dat size', len(dat))
en = 'and ambition to war.'
for e in dat_e:
    if e['text'] == en:
        fo = e['foff']
        cur = dat[fo:fo + 30]
        print('fo', fo, 'cur:', cur.hex(), repr(cur.decode('latin1')))
        new = 'aus Ehrgeiz Krieg.'
        end = dat.find(b'\x00', fo)
        print('find NUL at', end)
        buf = new.encode('latin1') + b'\x00'
        dat[fo:fo + len(buf)] = buf
        print('after:', dat[fo:fo + 30].hex())
        # writeback sectors and verify
        pos = 0
        for i in range(nsec):
            chunk = dat[pos:pos + DATA_SIZE]
            if not chunk:
                break
            f.seek(lba * SECTOR_SIZE + HDR + i * SECTOR_SIZE)
            f.write(chunk)
            pos += len(chunk)
        f.flush()
        # manual absolute-offset read
        e1 = [x for x in dat_e if x['foff'] == fo][0]
        f.seek(e1['off'])
        print('manual abs read:', repr(f.read(24)))
f.close()
