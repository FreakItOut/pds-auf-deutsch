# -*- coding: utf-8 -*-
import ctypes
import ctypes.wintypes as wt
import subprocess
import sys
import time

sys.stdout.reconfigure(encoding='latin1')
k32 = ctypes.WinDLL('kernel32', use_last_error=True)
u32 = ctypes.WinDLL('user32', use_last_error=True)
g32 = ctypes.WinDLL('gdi32', use_last_error=True)
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


class BIH(ctypes.Structure):
    _fields_ = [('biSize', wt.DWORD), ('biWidth', wt.LONG),
                ('biHeight', wt.LONG), ('biPlanes', wt.WORD),
                ('biBitCount', wt.WORD), ('biCompression', wt.DWORD),
                ('biSizeImage', wt.DWORD), ('biXPelsPerMeter', wt.LONG),
                ('biYPelsPerMeter', wt.LONG), ('biClrUsed', wt.DWORD),
                ('biClrImportant', wt.DWORD)]


class BI(ctypes.Structure):
    _fields_ = [('bmiHeader', BIH), ('bmiColors', wt.DWORD * 3)]


def find_pid():
    r = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq pds-recompile.exe',
                        '/FO', 'CSV', '/NH'], capture_output=True)
    for line in r.stdout.decode('latin1', 'ignore').splitlines():
        p = [x.strip('"') for x in line.split('","')]
        if len(p) > 1 and p[0].lower() == 'pds-recompile.exe':
            return int(p[1])
    return None


def find_window(pid):
    found = []

    @ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
    def cb(hwnd, lp):
        p = wt.DWORD()
        u32.GetWindowThreadProcessId(hwnd, ctypes.byref(p))
        if p.value == pid and u32.IsWindowVisible(hwnd):
            found.append(hwnd)
        return True

    u32.EnumWindows(cb, 0)
    return found[0] if found else None


pid = find_pid()
print('pid', pid, flush=True)
if not pid:
    sys.exit(1)
hwnd = find_window(pid)
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
                if len(hits) >= 4:
                    break
                p = data.find(sig, p + 1)
        if len(hits) >= 4:
            break
    addr = base + size
    if addr == 0:
        break
print('hits', [hex(x) for x in hits], flush=True)
bases = [x - 0x200 for x in hits]
print('bases', [hex(b) for b in bases], flush=True)
# groessten zusammenhaengenden Bereich um base0 ermitteln
target = bases[0]
start = target - 0x200000
size = 0x400000
blob = rd(start, size)
print('read', len(blob) if blob else 0, 'from', hex(start), flush=True)
if blob:
    open('_work/review_fixes/bigdump.bin', 'wb').write(blob)
    for t in (b'Geniesse', b'Frieden', b'falsch vor', b'solange'):
        i = blob.find(t)
        print('text', t, 'at', hex(start + i) if i >= 0 else -1, flush=True)
