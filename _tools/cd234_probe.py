# context probe for the remaining CD2-4 items
import csv
import re
import sys
sys.stdout.reconfigure(encoding='latin1')

SECT, DATA = 2352, 2048


def read_file(bp, lba, size):
    with open(bp, 'rb') as fh:
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


PROBES = {
    (2, 'CHILDMP.MCB'): ['3 LASER EQUIP CHANGE', 'Not Use'],
    (2, 'TWN_CAMP.PRG'): ['Quit Game'],
    (2, 'TWN_E057.PRG'): ['Buy Gun Part', 'Buy Item', 'Sell Gun Part'],
    (2, 'TWN_RUIN.PRG'): ['How long?'],
    (2, 'FLD_A5.MCB'): ['A:LOAD, B:NOT LOAD', 'NO USE'],
    (2, 'FLD_A3.MCB'): ['NO USE'],
    (2, 'FLD_C4_6.MCB'): ['NO USE'],
    (2, 'FLD_B6.MCB'): ['NO USE'],
    (4, 'TWN_CARA.PRG'): ['All the valuable items', 'relic from the Ancient Age',
                          'An object from the Ancient Age'],
    (4, 'TWN_SEEK.PRG'): ['for the power of Goettern.'],
    (3, 'TWN_E120.PRG'): ['Buy Gun Part', 'Buy Item', 'Sell Gun Part'],
    (3, 'TWN_E121.PRG'): ['Buy Gun Part', 'Buy Item', 'Sell Gun Part'],
}
for (d, f), needles in PROBES.items():
    fs = '_work/fs_records_cd%d.csv' % d
    idx = {r['name']: (int(r['lba']), int(r['size']))
           for r in csv.DictReader(open(fs, encoding='latin1'), delimiter=';')
           if int(r['lba']) > 0}
    if f not in idx:
        print(' disc%d %s missing' % (d, f))
        continue
    lba, size = idx[f]
    data = read_file('_work/patched_disc%d.bin' % d, lba, size)
    print('===== disc%d %s (size %d)' % (d, f, size))
    for nd in needles:
        for m in list(re.finditer(re.escape(nd.encode('latin1')), data))[:3]:
            p = m.start()
            e = data.find(b'\x00', p)
            head = p
            while head > 0 and data[head - 1] >= 0x80:
                head -= 1
            seg = data[p:e].decode('latin1')
            print('  off=%s %-34s len=%d  head_hex=%s' % (p, repr(seg[:50]), e - p, data[p:min(p + 8, head + 8)].hex()))
