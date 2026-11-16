#!/usr/bin/env python3
"""
Pointer-accurate in-place patcher for PDS MOVIE.DAT FMV subtitles.

- Reads per-string disc-absolute offsets from _work/evt_offsets_discN.json
  (produced by dump_evt_string_offsets.py; uses exact pointer arithmetic,
  NOT blind string scanning).
- Applies German translations from a CSV (format:  en;de  per line, latin1,
  '#' as comment) only when len(de) <= len(en).
- Patches the MOVIE.DAT file view (sector-reassembled 2048-byte data),
  then writes back sector-wise into the disc image (Mode 1: data at +16).
- Readback-verify every applied string.

Usage:
    python patch_evt_subtitles.py --disc 1 --csv _work/evt_de_map.csv
    python patch_evt_subtitles.py --disc all --csv _work/evt_de_map.csv
"""
import os
import sys
import argparse
import struct

sys.path.insert(0, r"C:\Users\FreakItOut\Downloads\pds-tools-master\pds-tools-master\tools\common")

SECTOR_SIZE = 2352
DATA_SIZE = 2048
HDR = 16  # PDS data track is Mode 1

def read_sector(f, n):
    f.seek(n * SECTOR_SIZE)
    raw = f.read(SECTOR_SIZE)
    if len(raw) < SECTOR_SIZE:
        return b''
    mode = raw[15]
    if mode == 1:
        return raw[16:16+2048]
    elif mode == 2:
        sub = raw[18]
        return raw[24:24+2324] if (sub & 0x20) else raw[24:24+2048]
    return raw[16:16+2048]

def load_de_map(path):
    m = {}
    with open(path, 'r', encoding='latin1') as f:
        for ln, line in enumerate(f, 1):
            line = line.rstrip('\r\n')
            if not line or line.startswith('#'):
                continue
            if ';' not in line:
                print(f"  WARN csv line {ln} has no ';' -> skipped")
                continue
            en, de = line.split(';', 1)
            # NB: do NOT strip EN - trailing spaces are part of the disc key
            en, de = en, de.strip()
            if en and de:
                m[en] = de
    return m

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--disc', required=True)  # 1..4 or 'all'
    ap.add_argument('--csv', required=True)
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    de_map = load_de_map(args.csv)
    print(f"Loaded {len(de_map)} DE translations from {args.csv}")

    discs = [1, 2, 3, 4] if args.disc.lower() == 'all' else [int(args.disc)]

    for dnum in discs:
        out_bin = f'_work/patched_disc{dnum}.bin'
        off_json = f'_work/evt_offsets_disc{dnum}.json'
        import json
        with open(off_json, 'r', encoding='utf-8') as f:
            entries = json.load(f)['entries']

        dat_entries = [e for e in entries if e['src'].startswith('MOVIE.DAT')]
        if not dat_entries:
            print(f"disc {dnum}: no MOVIE.DAT entries — skip")
            continue
        lba = dat_entries[0].get('lba')
        # re-derive lba from disc offset formula (sector-wise)
        # foff of MOVIE.DAT strings is in-file; we stored disc offset; reparse:
        import json as _j
        # find MOVIE.DAT lba by scanning: use first entry's disc offset & foff
        e0 = dat_entries[0]
        # disc_offset = sector*2352 + HDR + (foff % 2048), sector = lba + foff//2048
        # invert:
        k0 = e0['foff']
        lba = (e0['off'] - HDR - (k0 % 2048)) // SECTOR_SIZE - (k0 // 2048)
        size = 27856  # confirmed constant on all 4 discs

        with open(out_bin, 'r+b') as f:
            # sector-reassemble the file view
            nsec = (size + DATA_SIZE - 1) // DATA_SIZE
            dat = bytearray(b''.join(read_sector(f, lba + i) for i in range(nsec))[:size])

            applied, skipped_long, skipped_node, notfound = 0, 0, 0, 0
            for e in dat_entries:
                en = e['text']
                de = de_map.get(en)
                if de is None:
                    notfound += 1
                    continue
                if len(de.encode('latin1')) > len(en.encode('latin1')):
                    skipped_long += 1
                    continue
                fo = e['foff']
                end = dat.find(b'\x00', fo)
                orig_len = end - fo
                if orig_len < len(en.encode('latin1')):
                    orig_len = len(en.encode('latin1'))
                buf = de.encode('latin1') + b'\x00'
                if fo + len(buf) > size:
                    continue
                dat[fo:fo+len(buf)] = buf
                applied += 1

            print(f"disc {dnum}: applied={applied} no-de={notfound} "
                  f"too-long={skipped_long}")

            if not args.dry_run:
                # write back sector-wise
                pos = 0
                for i in range(nsec):
                    chunk = dat[pos:pos+DATA_SIZE]
                    if not chunk:
                        break
                    f.seek(lba * SECTOR_SIZE + HDR + i * SECTOR_SIZE)
                    f.write(chunk)
                    pos += len(chunk)
                f.flush()
                # readback verify
                f.seek(0)
                dat2 = b''.join(read_sector(f, lba + i) for i in range(nsec))[:size]
                diffs = 0
                for e in dat_entries:
                    fo, end = e['foff'], dat2.find(b'\x00', e['foff'])
                    s = dat2[fo:end].decode('latin1', errors='replace')
                    en = e['text']
                    de = de_map.get(en)
                    if de is None:
                        continue
                    if len(de.encode('latin1')) <= len(en.encode('latin1')) and s != de:
                        diffs += 1
                print(f"disc {dnum}: readback verify done, mismatches={diffs}")

if __name__ == '__main__':
    main()
