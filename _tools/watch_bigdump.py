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
base0 = bases[0]


def grab():
    r = wt.RECT()
    u32.GetWindowRect(hwnd, ctypes.byref(r))
    w = r.right - r.left
    ht = r.bottom - r.top
    if w <= 0 or ht <= 0:
        return None, 0, 0
    hdc = u32.GetWindowDC(hwnd)
    mdc = g32.CreateCompatibleDC(hdc)
    bmp = g32.CreateCompatibleBitmap(hdc, w, ht)
    g32.SelectObject(mdc, bmp)
    u32.PrintWindow(hwnd, mdc, 2)
    bi = BI()
    bi.bmiHeader.biSize = ctypes.sizeof(BIH)
    bi.bmiHeader.biWidth = w
    bi.bmiHeader.biHeight = -ht
    bi.bmiHeader.biPlanes = 1
    bi.bmiHeader.biBitCount = 32
    buf = ctypes.create_string_buffer(w * ht * 4)
    g32.GetDIBits(mdc, bmp, 0, ht, buf, ctypes.byref(bi), 0)
    g32.DeleteObject(bmp)
    g32.DeleteDC(mdc)
    u32.ReleaseDC(hwnd, hdc)
    return buf.raw, w, ht


def count(data, w, y0, y1, x0, x1):
    cnt = 0
    if not data:
        return 0
    for y in range(int(y0), int(y1), 2):
        off = (y * w + int(x0)) * 4
        for x in range(int(x0), int(x1), 2):
            b, g, r = data[off], data[off + 1], data[off + 2]
            if r > 150 and g > 150 and b > 150:
                cnt += 1
            off += 8
    return cnt


t0 = time.time()
while time.time() - t0 < 240:
    data, w, ht = grab()
    band = count(data, w, ht * 0.82, ht * 0.90, w * 0.15, w * 0.85)
    above = count(data, w, ht * 0.70, ht * 0.80, w * 0.15, w * 0.85)
    if band > 120 and above < band * 0.6:
        print('subtitle band=%d above=%d' % (band, above), flush=True)
        stamp = int(time.time())
        open('_work/review_fixes/sub3_%d.raw' % stamp, 'wb').write(data)
        start = base0 - 0x100000
        blob = rd(start, 0x200000)
        if blob:
            open('_work/review_fixes/bigdump_%d.bin' % stamp, 'wb').write(blob)
            print('dump', len(blob), hex(start), flush=True)
            for t in (b'Geniesse', b'Frieden', b'falsch', b'solange',
                      b'Phase'):
                i = blob.find(t)
                print('  text', t, hex(start + i) if i >= 0 else -1,
                      flush=True)
        sys.exit(0)
    time.sleep(0.3)
print('kein Untertitel', flush=True)
