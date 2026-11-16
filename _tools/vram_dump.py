# -*- coding: utf-8 -*-
# Dumpt 0x80000 Bytes VDP2-VRAM ab Treffer-0x200 des laufenden Prozesses.
import ctypes
import ctypes.wintypes as wt
import sys

sys.stdout.reconfigure(encoding='latin1')
k32 = ctypes.WinDLL('kernel32', use_last_error=True)
PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_VM_READ = 0x0010


def find_pid(name):
    import subprocess
    r = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq ' + name,
                        '/FO', 'CSV', '/NH'], capture_output=True,
                       text=True)
    for line in r.stdout.splitlines():
        p = [x.strip('"') for x in line.split('","')]
        if len(p) > 1 and p[0].lower() == name.lower():
            return int(p[1])
    return None


pid = None
if len(sys.argv) > 3:
    pid = int(sys.argv[3])
else:
    pid = find_pid('pds-recompile.exe')
print('pid', pid)
h = k32.OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ,
                    False, pid)
base = int(sys.argv[1], 16)
size = int(sys.argv[2], 16) if len(sys.argv) > 2 else 0x80000
buf = ctypes.create_string_buffer(size)
got = ctypes.c_size_t(0)
ok = k32.ReadProcessMemory(h, ctypes.c_void_p(base), buf, size,
                           ctypes.byref(got))
print('read ok', bool(ok), 'got', got.value)
if ok:
    open('_work/review_fixes/vram_full.bin', 'wb').write(
        buf.raw[:got.value])
    print('saved _work/review_fixes/vram_full.bin')
