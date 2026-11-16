# Fix the CD1-CD4 intro texts:
#  * FLD_D5.FNT name-entry screen: the DE translation of the first line had
#    grown to 27 bytes and overwrote the 0x00 separator before the second
#    line, so both lines were displayed as one block.  Rewrite the whole
#    46-byte region with a grammatical 26-byte line plus the separator, and
#    complete the "No, it is not." answer.
#  * TWN_JIRI.PRG: translate the "Don't Ride" prompt at offset 2868.
#
# All four discs carry identical copies of both files, so all four get the
# same patch.  Offset-based and readback-verified; safe to run repeatedly.
#
# usage: python fix_intro_texts.py [dry|apply]
import csv
import sys

SECT, DATA = 2352, 2048
MODE = sys.argv[1] if len(sys.argv) > 1 else 'dry'
DRY = MODE != 'apply'

# --- FLD_D5.FNT name-entry screen -----------------------------------------
NAME_OFF = 11456
NAME_OLD = (b'Derjenige der Edge steuert,'      # 27 bytes (oversized)
            b'wie ist dein Name?' + b'\x00')    # 18 + NUL
NAME_NEW = (b'Derjenige, der Edge lenkt,'       # 26 bytes, fits the slot
            b'\x00'
            b'wie ist dein Name?' + b'\x00')    # 18 + NUL
assert len(NAME_OLD) == len(NAME_NEW) == 46, (len(NAME_OLD), len(NAME_NEW))

OPT_OFF = 11533
OPT_OLD = b'Nein.'
OPT_NEW = b'Nein, nicht.'
OPT_SLOT = 15  # "No, it is not." (14) + NUL, padded with 0xFF up to 11547


def opt_region(text):
    return text + b'\x00' + b'\xff' * (OPT_SLOT - 1 - len(text))


assert len(opt_region(OPT_OLD)) == OPT_SLOT
assert len(opt_region(OPT_NEW)) == OPT_SLOT

# --- TWN_JIRI.PRG elevator prompt -----------------------------------------
JIRI_OFF = 2868
JIRI_OLD = b"Don't Ride"   # 10 bytes
JIRI_NEW = b'Bleib hier'   # 10 bytes
assert len(JIRI_OLD) == len(JIRI_NEW) == 10


def fs_index(disc):
    fs = ('_work/fs_records_all.csv' if disc == 1
          else '_work/fs_records_cd%d.csv' % disc)
    return {r['name']: (int(r['lba']), int(r['size']))
            for r in csv.DictReader(open(fs, encoding='latin1'),
                                    delimiter=';') if int(r['lba']) > 0}


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


def write_file_regions(binp, lba, data):
    with open(binp, 'r+b') as f:
        for k in range((len(data) + DATA - 1) // DATA):
            f.seek((lba + k) * SECT + 16)
            f.write(data[k * DATA:(k + 1) * DATA])


def patch_file(disc, name, edits):
    """edits: list of (label, off, old_bytes, new_bytes, region_size).

    old_bytes may be a tuple of accepted current states.  A region whose
    current bytes already equal new_bytes is counted as already_ok.
    """
    idx = fs_index(disc)
    lba, size = idx[name]
    binp = '_work/patched_disc%d.bin' % disc
    data = bytearray(read_file(binp, lba, size))
    changed = False
    for label, off, old, new, span in edits:
        old_states = old if isinstance(old, tuple) else (old,)
        cur = bytes(data[off:off + span])
        if cur == new:
            print('disc %d %-12s %-10s already_ok' % (disc, name, label))
            continue
        if cur not in old_states:
            print('disc %d %-12s %-10s ABORT unexpected bytes %r' % (
                disc, name, label, cur[:40]))
            continue
        data[off:off + span] = new
        changed = True
        print('disc %d %-12s %-10s patched' % (disc, name, label))
    if changed and not DRY:
        write_file_regions(binp, lba, bytes(data))
    # readback
    if not DRY and changed:
        chk = read_file(binp, lba, size)
        for label, off, old, new, span in edits:
            if chk[off:off + span] != new:
                print('disc %d %-12s %-10s READBACK MISMATCH' % (
                    disc, name, label))
        data = bytearray(chk)
    return changed


for d in (1, 2, 3, 4):
    patch_file(d, 'FLD_D5.FNT', [
        ('name-line', NAME_OFF, NAME_OLD, NAME_NEW, 46),
        ('name-no', OPT_OFF, opt_region(OPT_OLD), opt_region(OPT_NEW),
         OPT_SLOT),
    ])
    patch_file(d, 'TWN_JIRI.PRG', [
        ('dont-ride', JIRI_OFF, (JIRI_OLD, JIRI_NEW), JIRI_NEW, 10),
    ])

print('mode=%s done' % MODE)
