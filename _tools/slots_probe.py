# Read exact slot boundaries for the remaining EN strings found live on disc1.
import csv
import re
import sys
sys.stdout.reconfigure(encoding='latin1')

SECT = 2352
DATA = 2048


def read_file(binpath, lba, size):
    with open(binpath, 'rb') as fh:
        out = bytearray()
        need = size
        s = lba
        while need > 0:
            fh.seek(s * SECT + 16)
            chunk = fh.read(min(DATA, need))
            if len(chunk) < min(DATA, need):
                break
            out += chunk
            need -= len(chunk)
            s += 1
    return bytes(out[:size])


idx = {r['name']: (int(r['lba']), int(r['size']))
       for r in csv.DictReader(open('_work/fs_records_all.csv', encoding='latin1'),
                               delimiter=';') if int(r['lba']) > 0}
NEEDLES = {
    'CHILDMP.MCB': ['YES', 'NO'],
    'FLD_A3.MCB': ['(Imperial piece of crap.)'],
    'FLD_B6.MCB': ['The Institute', 'regarding the Light Wing', 'record and seal',
                   'them throughout', 'more than a dragon'],
    'FLD_A7.FNT': ["The dragon's forms", 'armor will slow'],
    'MENU.SCB': ['From upper floors', 'From middle floors'],
    'MERUKABA.MCB': ['back now.', 'man nimmt sie', 'Was... man'],
}
for name, needles in NEEDLES.items():
    if name not in idx:
        print('%s missing' % name)
        continue
    lba, size = idx[name]
    data = read_file('_work/patched_disc1.bin', lba, size)
    print('=====', name, 'size', size)
    for nd in needles:
        for m in re.finditer(re.escape(nd.encode('latin1')), data):
            p = m.start()
            # slot start: scan back over prefix bytes >= 0x80 to previous NUL
            s = p
            while s > 0 and data[s - 1] >= 0x80:
                s -= 1
            if s > 0 and data[s - 1] not in (0, 0xFF):
                # include until previous NUL for context display
                t = s
                while t > 0 and data[t - 1] not in (0, 0xFF):
                    t -= 1
                s = t
            e = data.find(b'\x00', p)
            seg = data[s:e]
            print('off=%d len=%d' % (s, e - s))
            print('   hex-prefix=%s' % data[s:min(s + 40, p)].hex())
            print('   seg=%r' % seg[:220])
