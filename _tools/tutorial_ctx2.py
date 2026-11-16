# print disc context for specific tutorial offsets
import csv
SECT, DATA = 2352, 2048


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
       for r in csv.DictReader(open('_work/fs_records_all.csv',
                                    encoding='latin1'), delimiter=';')
       if int(r['lba']) > 0 and int(r['size']) > 0}
lba, size = idx['TUTORIAL.CGB']
data = read_file('_work/patched_disc1.bin', lba, size)

blocks = []
off = 0
for part in data.split(b'\x00'):
    if part:
        blocks.append((off, part))
    off += len(part) + 1

TARGETS = [60497, 60748, 61052, 61541, 61909, 62343, 63532, 55575, 55688,
           66525, 68902, 69404, 69752, 70631, 70731, 70777, 72321, 46, 57035,
           57065, 58139, 60497, 60748, 61052, 61541, 61909, 62343, 63399,
           63429, 66204, 66416, 67075, 67175, 67902, 68123, 68490, 68560]
tset = set(TARGETS)
import sys
sys.stdout.reconfigure(encoding='latin1')
for k, (o, p) in enumerate(blocks):
    if o in tset:
        print('### off=%d EN=%r' % (o, p.decode('latin1')[:90]))
        for j in range(max(0, k - 4), min(len(blocks), k + 5)):
            mo, mp = blocks[j]
            mark = ' <<<' if mo == o else ''
            print('   %6d %r%s' % (mo, mp.decode('latin1')[:80], mark))
