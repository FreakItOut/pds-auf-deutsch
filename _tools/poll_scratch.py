# -*- coding: utf-8 -*-
"""Pollt den Untertitel-Scratch (VRAM+0x6000) und dumpet ihn, sobald
etwas gezeichnet wurde."""
import ctypes
import ctypes.wintypes as wt
import subprocess
import sys
import time

sys.stdout.reconfigure(encoding='latin1')
k32 = ctypes.WinDLL('kernel32', use_last_error=True)
PQI, PVM = 0x0400, 0x0010
MEM_COMMIT = 0x1000


class MBI(ctypes.Structure):
    _fields_ = [('BaseAddress', ctypes.c_void_p),
                ('AllocationBase', ctypes.c_void_p),
                ('AllocationProtect', wt.DWORD),
                ('RegionSize', ctypes.c_size_t),
                ('State', wt.DWORD),
                ('Protect', wt.DWORD),
                ('Type', wt.DWORD)]


def find_pid():
    r = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq pds-recompile.exe',
                        '/FO', 'CSV', '/NH'], capture_output=True)
    for line in r.stdout.decode('latin1', 'ignore').splitlines():
        p = [x.strip('"') for x in line.split('","')]
        if len(p) > 1 and p[0].lower() == 'pds-recompile.exe':
            return int(p[1])
    return None


pid = find_pid()
print('pid', pid)
if not pid:
    sys.exit(1)
h = k32.OpenProcess(PQI | PVM, False, pid)


def rd(a, n):
    buf = ctypes.create_string_buffer(n)
    got = ctypes.c_size_t(0)
    ok = k32.ReadProcessMemory(h, ctypes.c_void_p(a), buf, n,
                               ctypes.byref(got))
    return buf.raw[:got.value] if ok else None


raw = open('_work/ascii_cgz/font_de.raw', 'rb').read()
sig = raw[0x200:0x240]
addr = 0
hits = []
while True:
    mbi = MBI()
    if not k32.VirtualQueryEx(h, ctypes.c_void_p(addr), ctypes.byref(mbi),
                              ctypes.sizeof(mbi)):
        break
    base = mbi.BaseAddress or 0
    size = mbi.RegionSize or 0
    if mbi.State == MEM_COMMIT and size:
        data = rd(base, size)
        if data:
            p = data.find(sig)
            while p != -1:
                hits.append(base + p)
                if len(hits) >= 8:
                    break
                p = data.find(sig, p + 1)
        if len(hits) >= 8:
            break
    addr = base + size
    if addr == 0:
        break
print('hits', [hex(x) for x in hits])
# VRAM-Kandidat: Scratch bei +0x6000
best = None
for hit in hits:
    vram = hit - 0x200
    s = rd(vram + 0x6000, 0x40)
    if s:
        nz = sum(1 for b in s if b)
        print('cand', hex(vram), 'scratch nz', nz)
        if best is None or nz > best[1]:
            best = (vram, nz)

print('polling for subtitles (max 120 s)...')
vram = hits[0] - 0x200 if hits else None
found = None
t0 = time.time()
while time.time() - t0 < 120:
    for hit in hits:
        v = hit - 0x200
        s = rd(v + 0x6000, 0x800)
        if s and sum(1 for b in s if b) > 64:
            found = (v, s)
            break
    if found:
        break
    time.sleep(0.2)
if found:
    v, s = found
    print('SUBTITLE at vram', hex(v))
    open('_work/review_fixes/scratch_dump.bin', 'wb').write(s)
    # Tiles 8x16 (32 B) ausgeben
    shown = 0
    for t in range(64):
        g = s[t * 32:(t + 1) * 32]
        ink = sum(1 for b in g for nib in (b >> 4, b & 15) if nib)
        if ink > 6:
            print('tile', t, 'ink', ink)
            for y in range(16):
                row = ''
                for x in range(16):
                    b = g[y * 2 + x // 8]
                    bit = (b >> (7 - (x % 8))) & 1
                    row += '#' if bit else '.'
                print('   ' + row)
            shown += 1
            if shown >= 4:
                break
else:
    print('kein Untertitel gesehen')
