# -*- coding: utf-8 -*-
# Vergleicht den im laufenden Prozess geladenen Font mit font_de.raw.
import ctypes
import ctypes.wintypes as wt
import subprocess
import sys

sys.stdout.reconfigure(encoding='latin1')
k32 = ctypes.WinDLL('kernel32', use_last_error=True)
PQI, PVM = 0x0400, 0x0010
MEM_COMMIT = 0x1000
PAGE_NOACCESS = 0x01
PAGE_GUARD = 0x100


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
    if (mbi.State == MEM_COMMIT and size and
            not (mbi.Protect & (PAGE_NOACCESS | PAGE_GUARD))):
        data = rd(base, size)
        if data:
            p = data.find(sig)
            while p != -1:
                hits.append(base + p)
                if len(hits) >= 4:
                    break
                p = data.find(sig, p + 1)
        if len(hits) >= 4:
            break
    addr = base + size
    if addr == 0:
        break
print('hits', [hex(x) for x in hits])
for x in hits[:3]:
    start = x - 0x200
    blob = rd(start, len(raw))
    if not blob:
        print('read fail', hex(start))
        continue
    same = sum(1 for a, b in zip(blob, raw) if a == b)
    print('hit', hex(x), 'start', hex(start), 'match %d/%d' % (same, len(raw)))
    open('_work/review_fixes/mem_%x.bin' % start, 'wb').write(blob)
