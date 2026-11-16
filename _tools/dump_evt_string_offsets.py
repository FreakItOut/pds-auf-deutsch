#!/usr/bin/env python3
"""
Dump every EVT subtitle string with its EXACT disc-absolute byte offset.

Reuses the same parsing logic (opcodes / pointer resolution) as
pds-tools/tools/extract_subtitles.py, but instead of writing SRTs,
records for each subtitle string:
    { src, disc_offset (absolute byte in .bin), file_offset, text }

This is the basis for pointer-accurate in-place patching (no blind
string scanning, no false positives).

Usage:
    python dump_evt_string_offsets.py --iso <disc.bin> --out <json>
"""
import os
import sys
import struct
import json
import re
import argparse
from collections import Counter

PDS_TOOLS = r"C:\Users\FreakItOut\Downloads\pds-tools-master\pds-tools-master\tools"
sys.path.insert(0, PDS_TOOLS)
sys.path.insert(0, os.path.join(PDS_TOOLS, "common"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from iso9660 import ISO9660Reader, SECTOR_SIZE, DATA_SIZE, read_sector

# ---- binary helpers (same as extract_subtitles.py) ----
def read_u32_be(d, o): return struct.unpack('>I', d[o:o+4])[0]
def read_s16_be(d, o): return struct.unpack('>h', d[o:o+2])[0]
def align2(o): return (o + 1) & ~1
def align4(o): return (o + 3) & ~3
def read_cstring(d, o):
    if o < 0 or o >= len(d): return ''
    e = o
    while e < len(d) and d[e] != 0: e += 1
    try: return d[o:e].decode('ascii', errors='strict')
    except Exception: return d[o:e].decode('ascii', errors='replace')

# ---- opcode table (from extract_subtitles.py / townScript.cpp) ----
OP_END=1; OP_CALL_NATIVE=7; OP_DRAW_STRING=27; OP_DISPLAY_TIMED=36
OP_CUTSCENE_SYNC=46

def detect_prg_base(data):
    cand = Counter()
    for i in range(0, min(len(data)-4, 0x2000), 4):
        v = read_u32_be(data, i)
        if 0x06000000 <= v <= 0x060FFFFF or 0x00200000 <= v <= 0x002FFFFF:
            cand[v & 0xFFFF0000] += 1
    return cand.most_common(1)[0][0] if cand else None

def resolve_str_offset(data, ptr_val, base):
    """Return (text, file_offset, base) or None. Double-indirection first."""
    bases = ([base] if base else []) + \
        [b for b in (0x06050000,0x06040000,0x06010000,0x06060000,0x00250000,0x00200000) if b != base]
    for b in bases:
        fo = ptr_val - b
        if not (0 <= fo < len(data) - 4):
            continue
        inner = read_u32_be(data, fo)
        io = inner - b
        if 0 <= io < len(data):
            t = read_cstring(data, io)
            if t and len(t) >= 2 and t.isprintable():
                return (t, io, b)
        t = read_cstring(data, fo)
        if t and len(t) >= 2 and t.isprintable():
            return (t, fo, b)
    return None

def find_script_regions(data):
    # identical clustering logic to extract_subtitles.py
    syncs = []
    for i in range(len(data)-3):
        if data[i] == 0x2E:
            a = align2(i+1)
            if a+2 <= len(data):
                f = read_s16_be(data, a)
                if 0 <= f <= 15000: syncs.append(i)
    if not syncs: return []
    clusters, cur = [], [syncs[0]]
    for p in syncs[1:]:
        if p - cur[-1] < 300: cur.append(p)
        else:
            if len(cur) >= 2: clusters.append(cur)
            cur = [p]
    if len(cur) >= 2: clusters.append(cur)
    regions = []
    for c in clusters:
        start = c[0]
        for s in range(c[0], max(0, c[0]-4096), -1):
            if data[s] in (0x07, 0x19): start = s; break
        else: start = max(0, c[0]-256)
        end = c[-1] + 64
        for s in range(c[-1], min(len(data), c[-1]+4096)):
            if data[s] == 0x01: end = s+1; break
        regions.append((start, end))
    return regions

def parse_region_strs(data, base, rstart, rend):
    """Parse one script region, return subtitle strings with file offsets."""
    out, pos, errs = [], rstart, 0
    def fail():
        nonlocal errs
        errs += 1
        return errs > 3
    while pos < min(rend, len(data)):
        op = data[pos]; pos += 1
        if op == 0: continue
        if op == OP_END: break
        elif op == 2: pos = align2(pos); pos += 2
        elif op in (3, 5, 6): pos = align4(pos); pos += 4
        elif op == OP_CALL_NATIVE:
            if pos >= len(data): break
            n = data[pos]; pos += 1
            pos = align4(pos)
            if pos+4+n*4 > len(data): break
            pos += 4 + n*4
        elif 8 <= op <= 13: pos = align2(pos); pos += 2
        elif op in (15, 17): pos = align2(pos); pos += 2
        elif op == 18: pos += 1; pos = align2(pos); pos += 2
        elif op == 20: pos += 1; pos = align2(pos); pos += 4
        elif op == 21:
            if pos >= len(data): break
            arg = struct.unpack('>b', data[pos:pos+1])[0]; pos += 1
            pos = align4(pos)
            if pos >= len(data): break
            cnt = data[pos]
            sk = max(arg, cnt)
            if sk <= 0 or sk > 64:
                if fail(): return out
                continue
            if pos + sk*4 > len(data): break
            pos += sk*4
        elif op == 27:  # drawString
            pos = align4(pos)
            if pos+4 > len(data): break
            pv = read_u32_be(data, pos); pos += 4
            r = resolve_str_offset(data, pv, base)
            if r: out.append({'kind': 'draw', **{'text': r[0], 'off': r[1]}})
        elif op == 29: pass
        elif op == 31:
            if pos >= len(data): break
            n = data[pos]; pos += 1
            pos = align4(pos)
            if pos+4+n*4 > len(data): break
            pos += 4 + n*4
        elif op in (32, 25, 26, 24): pass
        elif op in (33, 34): pos += 1
        elif op == OP_DISPLAY_TIMED:  # 36
            pos = align2(pos)
            if pos+2 > len(data): break
            pos += 2; pos = align4(pos)
            if pos+4 > len(data): break
            pv = read_u32_be(data, pos); pos += 4
            r = resolve_str_offset(data, pv, base)
            if r: out.append({'kind': 'timed', 'text': r[0], 'off': r[1]})
        elif op == 39:
            if pos >= len(data): break
            a = struct.unpack('>b', data[pos:pos+1])[0]; pos += 1
            if a > 0:
                pos = align4(pos)
                if pos+a*4 > len(data): break
                pos += a*4
        elif op == 41: pos = align2(pos); pos += 2
        elif op == 43: pos += 1; pos = align2(pos); pos += 2
        elif op == OP_CUTSCENE_SYNC: pos = align2(pos); pos += 2
        elif op == 48: pos = align2(pos); pos += 6
        else:
            if fail(): return out
            continue
    return out

def disc_offset_for(lba, k, hdr):
    sector = lba + (k // DATA_SIZE)
    return sector * SECTOR_SIZE + hdr + (k % DATA_SIZE)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--iso', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--disc', type=int, default=1)
    args = ap.parse_args()

    iso = ISO9660Reader(args.iso)
    files = iso.list_files()

    # detect data offset within raw sector (Mode1=16, Form1=24)
    with open(args.iso, 'rb') as f:
        raw = read_sector(f, 16)
    hdr = 24 if raw[len(raw)-1] != 0 or True else 16  # detect below properly
    # detect via mode byte of sector 16
    with open(args.iso, 'rb') as f:
        f.seek(16 * SECTOR_SIZE)
        s = f.read(SECTOR_SIZE)
    hdr = 24 if s[15] == 2 else 16
    print(f"sector mode={s[15]}, data header offset={hdr}")

    entries = []
    seen = {}

    # --- MOVIE.DAT ---
    dat = next((e for e in files if e['name'].upper() == 'MOVIE.DAT'), None)
    if dat:
        d = iso.extract_file(dat['lba'], dat['size'])
        base = detect_movie_dat_base(d)
        print(f"MOVIE.DAT lba={dat['lba']} size={dat['size']} base=0x{base:08X}")
        i, group = 0, 0
        while i < len(d) - 8:
            if d[i:i+2] == b'\xFF\xFF':
                group += 1; i += 8; continue
            ptr = read_u32_be(d, i+4)
            if base <= ptr < base + len(d):
                so = ptr - base
                t = read_cstring(d, so)
                if t and len(t) >= 2:
                    entries.append({
                        'src': f'MOVIE.DAT g{group}', 'disc': args.disc,
                        'off': disc_offset_for(dat['lba'], so, hdr),
                        'foff': so, 'text': t})
                i += 8
            else:
                break
        print(f"  -> {len([e for e in entries if e['src'].startswith('MOVIE.DAT')])} strings from MOVIE.DAT")

    # --- PRG overlays ---
    for entry in files:
        nm = entry['name'].upper()
        if not nm.endswith('.PRG') or nm == 'MOVIE.PRG':
            continue
        pd = iso.extract_file(entry['lba'], entry['size'])
        if not re.search(rb'\.[Cc][Pp][Kk]', pd):
            continue
        base = detect_prg_base(pd)
        regs = find_script_regions(pd)
        if not regs: continue
        allstrs = []
        for rs, re_ in regs:
            allstrs.extend(parse_region_strs(pd, base, rs, re_))
        for s in allstrs:
            key = (entry['lba'], s['off'])
            if key in seen: continue
            seen[key] = True
            entries.append({
                'src': entry['name'], 'disc': args.disc,
                'off': disc_offset_for(entry['lba'], s['off'], hdr),
                'foff': s['off'], 'text': s['text']})
        print(f"PRG {entry['name']}: {len(allstrs)} strings")

    with open(args.out, 'w', encoding='utf-8') as f:
        json.dump({'disc': args.disc, 'entries': entries}, f, ensure_ascii=False, indent=1)
    print(f"TOTAL {len(entries)} subtitle strings -> {args.out}")

def detect_movie_dat_base(data):
    for known in (b"What's up, Edge", b"Thousands of years",
                  b"The age started anew", b"the Empire"):
        so = data.find(known)
        if so == -1: continue
        cand = Counter()
        for i in range(0, min(len(data)-4, 0x2000), 4):
            v = read_u32_be(data, i)
            pb = v - so
            if (0x06000000 <= pb <= 0x060FFFFF or 0x00200000 <= pb <= 0x002FFFFF) and pb % 0x10 == 0:
                cand[pb] += 1
        if cand:
            if 0x00250000 in cand: return 0x00250000
            return cand.most_common(1)[0][0]
    return 0x00250000

if __name__ == '__main__':
    main()
