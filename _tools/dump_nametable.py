# -*- coding: utf-8 -*-
"""Liest die VDP2-Nametabelle (VRAM+0x6000) aus dem laufenden Spiel und
dekodiert sie mit dem ASCII.CGZ-Font (Basis-Muster 3 = 8x8, 0x63 = 8x16)."""
import ctypes
import ctypes.wintypes as wt
import io
import subprocess
import sys

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
                if len(hits) >= 6:
                    break
                p = data.find(sig, p + 1)
        if len(hits) >= 6:
            break
    addr = base + size
    if addr == 0:
        break
print('font hits', [hex(x) for x in hits])
for hit in hits[:4]:
    vram = hit - 0x200
    nt = rd(vram + 0x6000, 0x1000)
    if not nt:
        continue
    vals = [nt[i] | (nt[i + 1] << 8) for i in range(0, len(nt), 2)]
    printable = sum(1 for v in vals if 0xC000 <= (v & 0xFFFC) <= 0xC0FF)
    print('cand', hex(vram), 'printable PN %d/%d' % (printable, len(vals)))
    if printable < 30:
        continue
    text = ''
    for v in vals:
        pn = v & 0x0FFF
        if 0x20 <= pn <= 0x60:
            text += chr(pn + 0x20)
    print('SMALL:', text[:120])
    text = ''
    for v in vals:
        pn = v & 0x0FFF
        if 0x63 <= pn <= 0x1E2:
            text += chr((pn - 0x63) // 2 + 0x20)
    print('LARGE:', text[:120])
