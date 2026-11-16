# Reconcile pass 2: few remaining RUIN spots; patch every listed offset on all discs.
import csv

SECT, DATA = 2352, 2048

FORCE = {
    # pass 1
    ('TWN_E022_PRG', 0): 'Ausgrabungsort',
    ('TWN_E022_PRG', 6): 'Motor eines Kampfschiffs.)',
    ('TWN_E022_PRG', 8): '(...Alles Wertvolle ist weg.)',
    ('TWN_E022_PRG', 37): 'Bin nie zu Fuss gelaufen.',
    ('TWN_E022_PRG', 46): 'und sein Blut entleert.)',
    ('TWN_E022_PRG', 50): 'Wenigstens kaempfend.)',
    ('TWN_E022_PRG', 53): 'Er starb als Jaeger.)',
    ('TWN_JIRI_PRG', 9): 'Verschlossen, bewegt nicht...',
    ('TWN_JIRI_PRG', 23): 'Verschlossen, bewegt nicht.',
    ('TWN_RUIN_PRG', 293): 'Wusste nie, dass die echte Welt',
    ('TWN_RUIN_PRG', 331): 'Keine Sorge.',
    ('TWN_RUIN_PRG', 370): 'Sie soll weg sein...',
    ('TWN_RUIN_PRG', 372): 'Das kann nicht sein...',
    ('TWN_RUIN_PRG', 373): 'All die Kaempfe umsonst.',
    ('TWN_RUIN_PRG', 374): 'Tut mir leid, ich half nicht.',
    ('TWN_RUIN_PRG', 375): 'Niemand ist je',
    ('TWN_RUIN_PRG', 376): 'bereit, das erste Mal zu kaempfen.',
    ('TWN_RUIN_PRG', 377): 'Was, wenn ich nicht kaempfen kann?',
    ('TWN_RUIN_PRG', 378): 'Setz auf Ladhas Heilkunst.',
    ('TWN_RUIN_PRG', 379): 'Keine Sorge, entspann dich und',
    ('TWN_RUIN_PRG', 380): 'lenk deine Energie auf Heilung.',
    # pass 2
    ('TWN_RUIN_PRG', 99): 'Es ist mein Fehler.',
    ('TWN_RUIN_PRG', 365): 'Schade.',
    ('TWN_RUIN_PRG', 483): 'Ueber die Vorzeit',
    ('TWN_RUIN_PRG', 244): 'findest du?',
}
ACCEPT = {('TWN_RUIN_PRG', 298)}   # none left (dummy)


def fs_index(disc):
    fs = ('_work/fs_records_all.csv' if disc == 1 else '_work/fs_records_cd%d.csv' % disc)
    return {r['name']: (int(r['lba']), int(r['size']))
            for r in csv.DictReader(open(fs, encoding='latin1'), delimiter=';') if int(r['lba']) > 0}


def read_file(binp, lba, size):
    out = bytearray()
    need, s = size, lba
    with open(binp, 'rb') as f:
        while need > 0:
            f.seek(s * SECT + 16)
            c = f.read(min(DATA, need))
            if not c:
                break
            out += c
            need -= len(c)
            s += 1
    return bytes(out[:size])


def write_file_regions(binp, lba, filedata):
    with open(binp, 'r+b') as f:
        for k in range((len(filedata) + DATA - 1) // DATA):
            f.seek((lba + k) * SECT + 16)
            f.write(filedata[k * DATA:(k + 1) * DATA])


def actual_str(data, o):
    end = o
    while end < len(data) and data[end] not in (0x00, 0xFF):
        end += 1
    return bytes(data[o:end]).decode('latin1'), end


patched = synced = skipped = 0
errors, csv_sync = [], []
for stem in ('TWN_E022_PRG', 'TWN_JIRI_PRG', 'TWN_RUIN_PRG'):
    name = stem.replace('_PRG', '.PRG')
    files = {}
    for d in (1, 2, 3, 4):
        idx = fs_index(d)
        if name in idx:
            lba, size = idx[name]
            files[d] = (lba, size, read_file('_work/patched_disc%d.bin' % d, lba, size))
    rows = []
    for line in open('_work/subtitles/%s_de.csv' % stem, encoding='latin1'):
        p = line.rstrip('\r\n').split(';')
        if len(p) >= 6:
            rows.append((int(p[0]), p))
    for uid, p in rows:
        offs = [int(x) for x in p[3].split('|') if x] or [int(p[2])]
        want_force = (stem, uid) in FORCE
        want_accept = (stem, uid) in ACCEPT
        vals = []
        for d, (lba, size, data) in files.items():
            for o in offs:
                if o >= len(data):
                    errors.append('%s d=%d uid=%d off=%d OOB' % (stem, d, uid, o))
                    continue
                act, nend = actual_str(data, o)
                if want_force:
                    new = FORCE[(stem, uid)]
                    if act != new:
                        if len(new.encode('latin1')) > len(p[4].encode('latin1')):
                            errors.append('%s d=%d uid=%d TOO LONG' % (stem, d, uid))
                            continue
                        se = nend + 1
                        while se < len(data) and data[se] == 0xFF:
                            se += 1
                        nb = new.encode('latin1')
                        data = bytearray(data)
                        data[o:o + len(nb)] = nb
                        fill = o + len(nb)
                        for k in range(fill, se):
                            data[k] = 0x00 if k == fill else 0xFF
                        write_file_regions('_work/patched_disc%d.bin' % d, lba, bytes(data))
                        files[d] = (lba, size, read_file('_work/patched_disc%d.bin' % d, lba, size))
                        chk = files[d][2]
                        if actual_str(chk, o)[0] != new:
                            errors.append('%s d=%d uid=%d off=%d READBACK %r' % (stem, d, uid, o, actual_str(chk, o)[0]))
                        patched += 1
                    else:
                        skipped += 1
                    vals.append(new)
                else:
                    vals.append(act)
        if vals:
            from collections import Counter
            mode, cnt = Counter(vals).most_common(1)[0]
            csv_sync.append((uid, mode))
            if want_accept and mode != p[5].rstrip():
                p[5] = mode
                synced += 1
            elif want_accept:
                skipped += 1
            # CSV sync from FORCE/disc for these rows
            if not want_accept and p[5].rstrip() != mode:
                p[5] = mode
                synced += 1
        if want_force or want_accept:
            print('uid %d force=%s accept=%s vals=%r csv=%r' % (uid, want_force, want_accept, sorted(set(vals)), p[5]))
    lines = open('_work/subtitles/%s_de.csv' % stem, encoding='latin1').read().split('\n')
    out = []
    sync_map = dict(csv_sync)
    for line in lines:
        p = line.rstrip('\r').split(';')
        if len(p) >= 6:
            uid = int(p[0])
            new = sync_map.get(uid)
            if new is not None and p[5] != new:
                p[5] = new
            out.append(';'.join(p))
        else:
            out.append(line)
    with open('_work/subtitles/%s_de.csv' % stem, 'w', encoding='latin1', newline='\n') as f:
        f.write('\n'.join(out) + '\n')

print('patched=%d synced=%d skipped=%d errors=%d' % (patched, synced, skipped, len(errors)))
for x in errors[:30]:
    print('  ' + x)
