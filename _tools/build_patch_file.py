# Build the distributable German translation patch file for
# Panzer Dragoon Saga (Europe, Discs 1-4).
#
# The patch file contains ONLY:
#   - file offsets where text was changed
#   - length of each region
#   - the German replacement bytes
#   - a CRC32 of the original bytes in each region (integrity check only)
#   - SHA1 hashes of the four original track-1 images (a plain checksum of
#     the *whole* image, used only to identify the disc revision; the game
#     data itself is NOT included).
#
# No original game data is shipped.  Users must provide their own legally
# obtained copy of the original PAL-EU disc images.
#
# usage: python build_patch_file.py
#   reads:  Original_CD<n>/*"(Track n n)"... (Track 1).bin  + _work/patched_disc<n>.bin
#   writes: _dist/pds_deutsch_patch.pzp
#           _dist/pds_deutsch_patcher.py   (copy of _tools/apply_patch_file.py)
#           _dist/sha1_checkliste.txt
import glob
import hashlib
import os
import shutil
import struct
import sys
import zlib
from binascii import crc32

sys.stdout.reconfigure(encoding='latin1')

MAGIC = b'PDS_DE01'
FMTVER = 1
OUT_DIR = '_dist'
OUT_PATCH = os.path.join(OUT_DIR, 'pds_deutsch_patch.pzp')
OUT_TOOL = os.path.join(OUT_DIR, 'pds_deutsch_patcher.py')
OUT_SHA = os.path.join(OUT_DIR, 'sha1_checkliste.txt')
OUT_GUI = os.path.join(OUT_DIR, 'pds_deutsch_patcher_gui.py')

ORIG_GLOB = 'Original_CD%d/*(Track 1).bin'
PATCHED_GLOB = '_work/patched_disc%d.bin'


def readall(path):
    with open(path, 'rb') as f:
        return f.read()


def sha1(data):
    return hashlib.sha1(data).hexdigest()


def diff_runs(a, b, merge_gap=8):
    """Runs of differing bytes in two equally sized byte strings."""
    out = []

    def rec(lo, hi):
        if a[lo:hi] == b[lo:hi]:
            return
        if hi - lo <= 64:
            out.append((lo, hi - lo))
            return
        m = (lo + hi) // 2
        rec(lo, m)
        rec(m, hi)

    rec(0, len(a))
    out.sort()
    runs = []
    for off, ln in out:
        if runs and off - (runs[-1][0] + runs[-1][1]) < merge_gap:
            runs[-1][1] = off + ln - runs[-1][0]
        else:
            runs.append([off, ln])
    return [(o, l) for o, l in runs]


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    payload = bytearray()
    payload += MAGIC
    payload += struct.pack('<II', FMTVER, 4)
    stats = []
    for disc in (1, 2, 3, 4):
        g = glob.glob(ORIG_GLOB % disc)
        if len(g) != 1:
            sys.exit('Originalbild-Nicht gefunden eindeutig fuer Disc '
                     '%d: %r' % (disc, g))
        orig_path = g[0]
        patched_path = PATCHED_GLOB % disc
        a = readall(orig_path)
        b = readall(patched_path)
        if len(a) != len(b):
            sys.exit('Disc %d: Groesse differs (%d vs %d)' % (
                disc, len(a), len(b)))
        mva, mvb = memoryview(a), memoryview(b)
        runs = diff_runs(mva, mvb)
        changed = sum(l for _, l in runs)
        frac = changed / len(a) * 100
        print('disc %d: %d regionen, %d bytes (%.4f%%)  orig=%s '
              'patched=%s' % (disc, len(runs), changed, frac,
                              sha1(a)[:12], sha1(b)[:12]))
        if frac > 2.0:
            sys.exit('disc %d: zu grosser diff, vermutlich falsche '
                     'Basis (%.2f%%)' % (disc, frac))
        payload += struct.pack('<IQ', disc, len(a))
        payload += bytes.fromhex(sha1(a))
        payload += bytes.fromhex(sha1(b))
        payload += struct.pack('<I', len(runs))
        blob = bytearray()
        for off, ln in runs:
            payload += struct.pack('<QII', off, ln, crc32(a[off:off + ln]))
            blob += b[off:off + ln]
        payload += struct.pack('<I', len(blob)) + blob
        stats.append((disc, orig_path, sha1(a), sha1(b), len(a),
                      len(runs), changed))
        del a, b, mva, mvb

    # ---- self test: rebuild patched images from originals ------------- #
    raw = bytes(payload)
    pos = 8 + 8
    for _ in range(4):
        disc, p = struct.unpack_from('<IQ', raw, pos)
        pos += 12
        sha_o = raw[pos:pos + 20].hex()
        sha_n = raw[pos + 20:pos + 40].hex()
        pos += 40
        (nh,) = struct.unpack_from('<I', raw, pos)
        pos += 4
        hunks = []
        for _ in range(nh):
            off, ln, c = struct.unpack_from('<QII', raw, pos)
            pos += 16
            hunks.append((off, ln, c))
        (bl,) = struct.unpack_from('<I', raw, pos)
        pos += 4 + bl
        data = bytearray(readall(glob.glob(ORIG_GLOB % disc)[0]))
        ok = 0
        i = 0
        for off, ln, c in hunks:
            if crc32(data[off:off + ln]) == c:
                data[off:off + ln] = raw[pos - bl:pos - bl + bl][i:i + ln]
                ok += 1
            i += ln
        if sha1(data) != sha_n:
            sys.exit('disc %d: self test FAILED' % disc)
        print('disc %d: reapply self test ok (%d/%d)' % (disc, ok, nh))

    comp = zlib.compress(raw, 9)
    final = MAGIC + struct.pack('<I', len(raw)) + comp
    with open(OUT_PATCH, 'wb') as f:
        f.write(final)
    print('patch file: %s (%d bytes)' % (OUT_PATCH, len(final)))

    # ---- copy the user-facing tool ----------------------------------- #
    shutil.copyfile('_tools/apply_patch_file.py', OUT_TOOL)
    shutil.copyfile('_tools/pds_deutsch_patcher_gui.py', OUT_GUI)

    # ---- sha1 checklist ---------------------------------------------- #
    lines = ['Pruefsummen fuer die deutsche Fassung',
             'Panzer Dragoon Saga (Europe), Discs 1-4', '',
             'orig_sha1 = Pruefsumme deines UNBEARBEITETEN Track-1-Abbilds',
             'deutsch_sha1 = Pruefsumme NACH dem Patchen', '',
             '# disc;datei_groesse_bytes;orig_sha1;deutsch_sha1']
    for disc, orig_path, sha_o, sha_n, size, nh, ch in stats:
        lines.append('%d;%d;%s;%s' % (disc, size, sha_o, sha_n))
    with open(OUT_SHA, 'w', encoding='ascii', newline='\n') as f:
        f.write('\n'.join(lines) + '\n')
    print('wrote %s' % OUT_SHA)


if __name__ == '__main__':
    main()
