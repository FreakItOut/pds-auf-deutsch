# Reconcile: remaining shifted/stale rows in TWN_E022/JIRI/RUIN/CAMP.
# FORCE uids get patched on all discs with the given German text.
# All other rows whose disc text differs from the CSV get the CSV synced
# from the disc value (they are already good on disc).
import csv

SECT, DATA = 2352, 2048

FORCE = {
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
}

STEMS = ('TWN_E022_PRG', 'TWN_JIRI_PRG', 'TWN_CAMP_PRG', 'TWN_RUIN_PRG')


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


def slot_end(data, nend):
    s = nend + 1
    while s < len(data) and data[s] == 0xFF:
        s += 1
    return s


errors, patched, synced, skipped = [], 0, 0, 0
for stem in STEMS:
    rows = []
    with open('_work/subtitles/%s_de.csv' % stem, encoding='latin1') as f:
        for line in f:
            p = line.rstrip('\r\n').split(';')
            if len(p) >= 6:
                rows.append((int(p[0]), p))
    # disc actuals per disc: offset -> actual
    disc_data = {}
    for d in (1, 2, 3, 4):
        idx = fs_index(d)
        name = stem.replace('_PRG', '.PRG')
        if name in idx:
            lba, size = idx[name]
            disc_data[d] = (lba, size, bytearray(read_file('_work/patched_disc%d.bin' % d, lba, size)))
    # determine mismatch rows and force rows
    sync_by_offset = {}   # offset -> disc text (authoritative: disc1)
    force_todo = {}       # (d, o) -> new text
    for uid, p in rows:
        offs = [int(x) for x in p[3].split('|') if x] or [int(p[2])]
        d1 = disc_data.get(1)
        for o in offs:
            a1 = actual_str(d1[2], o)[0] if d1 else None
            csv_de = p[5].rstrip()
            if (stem, uid) in FORCE:
                new = FORCE[(stem, uid)]
                for d, (lba, size, data) in disc_data.items():
                    act, nend = actual_str(data, o)
                    if act != new:
                        force_todo.setdefault((d, o), (uid, new))
                if a1 != new and d1 is not None:
                    if o is not None:
                        sync_by_offset.setdefault(o, ('FORCE', new))
            elif a1 is not None and a1 != csv_de:
                if o in sync_by_offset and sync_by_offset[o][1] != a1:
                    errors.append('%s uid=%d off=%d: ambig disc=%r vs %r' % (stem, uid, o, a1, sync_by_offset[o][1]))
                else:
                    sync_by_offset.setdefault(o, ('DISC', a1))
    # patch FORCE entries
    for (d, o), (uid, new) in sorted(force_todo.items()):
        lba, size, data = disc_data[d]
        # find matching csv row for en/len check
        match = [p2 for u2, p2 in rows if u2 == uid and (o in ([int(x) for x in p2[3].split('|') if x] or [int(p2[2])]))]
        if not match:
            errors.append('%s d=%d uid=%d off=%d: csv row missing' % (stem, d, uid, o))
            continue
        p2 = match[0]
        en_b = p2[4].encode('latin1')
        new_b = new.encode('latin1')
        if len(new_b) > len(en_b):
            errors.append('%s d=%d uid=%d TOO LONG %d>%d' % (stem, d, uid, len(new_b), len(en_b)))
            continue
        act, nend = actual_str(data, o)
        se = slot_end(data, nend)
        data[o:o + len(new_b)] = new_b
        for k in range(o + len(new_b), se):
            data[k] = 0x00 if k == o + len(new_b) else 0xFF
        write_file_regions('_work/patched_disc%d.bin' % d, lba, bytes(data))
        chk = read_file('_work/patched_disc%d.bin' % d, lba, size)
        a2 = actual_str(chk, o)[0]
        if a2 != new:
            errors.append('%s d=%d uid=%d off=%d: READBACK %r != %r' % (stem, d, uid, o, a2, new))
        patched += 1
        if d == 1:
            sync_by_offset[o] = ('FORCE', new)
    # sync csv from disc values
    for uid, p in rows:
        offs = [int(x) for x in p[3].split('|') if x] or [int(p[2])]
        hits = {}
        for o in offs:
            if o in sync_by_offset:
                hits[o] = sync_by_offset[o][1]
        if not hits:
            continue
        vals = set(hits.values())
        if len(vals) > 1:
            errors.append('%s uid=%d: per-offset sync differs %r' % (stem, uid, hits))
            continue
        new = vals.pop()
        if new == 'FORCE':
            continue
        if p[5].rstrip() == new:
            skipped += 1
            continue
        idx_in = [i for i, x in enumerate(offs) if x in hits]
        # put disc value into de (p[5])
        p[5] = new
        synced += 1

    # write csv back
    out = []
    seen_uids = {}
    with open('_work/subtitles/%s_de.csv' % stem, encoding='latin1') as f:
        for line in f:
            out.append(line.rstrip('\r\n'))
    for i, line in enumerate(out):
        p = line.split(';')
        if len(p) >= 6:
            uid = int(p[0])
            offs = [int(x) for x in p[3].split('|') if x] or [int(p[2])]
            vals = set(sync_by_offset[o][1] for o in offs if o in sync_by_offset)
            if len(vals) == 1:
                v = vals.pop()
                if v != 'FORCE' and p[5] != v:
                    p[5] = v
                    out[i] = ';'.join(p)
    with open('_work/subtitles/%s_de.csv' % stem, 'w', encoding='latin1', newline='\n') as f:
        f.write('\n'.join(out) + '\n')

print('patched=%d synced=%d skipped=%d' % (patched, synced, skipped))
if errors:
    print('ERRORS (%d):' % len(errors))
    for x in errors[:40]:
        print('  ' + x)
else:
    print('ERRORS: none')
