# -*- coding: utf-8 -*-
# Scannt den laufenden pds-recompile.exe nach dem geladenen Font/VRAM.
import ctypes
import ctypes.wintypes as wt
import os
import sys
import time

sys.stdout.reconfigure(encoding='latin1')

k32 = ctypes.WinDLL('kernel32', use_last_error=True)
PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_VM_READ = 0x0010
MEM_COMMIT = 0x1000
PAGE_NOACCESS = 0x01
PAGE_GUARD = 0x100


class MEMORY_BASIC_INFORMATION(ctypes.Structure):
    _fields_ = [('BaseAddress', ctypes.c_void_p),
                ('AllocationBase', ctypes.c_void_p),
                ('AllocationProtect', wt.DWORD),
                ('RegionSize', ctypes.c_size_t),
                ('State', wt.DWORD),
                ('Protect', wt.DWORD),
                ('Type', wt.DWORD)]


def find_pid(name):
    import subprocess
    r = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq ' + name,
                        '/FO', 'CSV', '/NH'], capture_output=True)
    for line in r.stdout.decode('latin1', 'ignore').splitlines():
        p = [x.strip('"') for x in line.split('","')]
        if len(p) > 1 and p[0].lower() == name.lower():
            return int(p[1])
    return None


def read_mem(h, addr, size):
    buf = ctypes.create_string_buffer(size)
    got = ctypes.c_size_t(0)
    ok = k32.ReadProcessMemory(h, ctypes.c_void_p(addr), buf, size,
                               ctypes.byref(got))
    if not ok:
        return None
    return buf.raw[:got.value]


def scan(h, sig, max_hits=5):
    hits = []
    addr = 0
    mbi = MEMORY_BASIC_INFORMATION()
    while k32.VirtualQueryEx(h, ctypes.c_void_p(addr),
                             ctypes.byref(mbi), ctypes.sizeof(mbi)):
        base = mbi.BaseAddress or 0
        size = mbi.RegionSize or 0
        if (mbi.State == MEM_COMMIT and size and
                not (mbi.Protect & PAGE_NOACCESS) and
                not (mbi.Protect & PAGE_GUARD)):
            data = read_mem(h, base, size)
            if data:
                p = data.find(sig)
                while p != -1:
                    hits.append(base + p)
                    if len(hits) >= max_hits:
                        return hits
                    p = data.find(sig, p + 1)
        addr = base + size
        if addr == 0:
            break
    return hits


def main():
    pid = int(sys.argv[1]) if len(sys.argv) > 1 else find_pid(
        'pds-recompile.exe')
    if not pid:
        print('Prozess nicht gefunden')
        return 1
    print('pid', pid)
    h = k32.OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ,
                        False, pid)
    if not h:
        print('OpenProcess fehlgeschlagen', ctypes.get_last_error())
        return 1
    sig = bytes.fromhex('00000000000000000000000000000000'
                        'fffffff0faaaaaf0fffffff0')
    # Signatur: unveraenderter Fontbereich ab 0x200
    raw = open('_work/ascii_cgz/font_de.raw', 'rb').read()
    sig2 = raw[0x200:0x240]
    for attempt in range(30):
        hits = scan(h, sig2, 3)
        if hits:
            print('font hits:', [hex(x) for x in hits])
            base = hits[0]
            for off in range(-0x200, 0x2100, 0x1000):
                a = base + off
                # rueckwaerts auf Regionsanfang ist nicht noetig
                blob = read_mem(h, a, 0x1000)
                if blob:
                    open('_work/review_fixes/vram_%x.bin' % a,
                         'wb').write(blob)
                    print('dump %x (%d)' % (a, len(blob)))
            return 0
        time.sleep(1)
    print('keine Font-Signatur gefunden')
    return 1


if __name__ == '__main__':
    sys.exit(main())
