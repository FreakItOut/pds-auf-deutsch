# -*- coding: utf-8 -*-
import ctypes
import ctypes.wintypes as wt
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
for hit in hits[:5]:
    vram = hit - 0x200
    blob = rd(vram, 0x8000)
    if not blob:
        continue
    vals = [blob[i] | (blob[i + 1] << 8) for i in range(0, len(blob) - 1, 2)]
    best = (0, 0)
    for start in range(0, len(vals) - 64, 16):
        cnt = 0
        for v in vals[start:start + 64]:
            if 0xC020 <= (v & 0xFFFC) <= 0xC0FF:
                cnt += 1
        if cnt > best[0]:
            best = (cnt, start)
    print('cand', hex(vram), 'best window', best[0], 'at', hex(best[1] * 2))
    if best[0] >= 8:
        s = best[1]
        txt = ''
        for v in vals[s:s + 200]:
            pn = v & 0x0FFF
            txt += chr((pn - 3) + 0x20) if 3 <= pn <= 0x62 else '.'
        print('   ', txt[:150])
        txt = ''
        for v in vals[s:s + 200]:
            pn = v & 0x0FFF
            txt += chr((pn - 0x63) // 2 + 0x20) if 0x63 <= pn <= 0x1E2 else '.'
        print('   large:', txt[:150])
