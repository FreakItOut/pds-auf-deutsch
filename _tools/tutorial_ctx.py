# context dump: for each kept-EN tutorial fragment (52970..76000), print
# surrounding disc lines (previous 2, next 2) so translations can continue
# the dialogue naturally.
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


def strings():
    out = []
    off = 0
    for part in data.split(b'\x00'):
        if part:
            out.append((off, part))
        off += len(part) + 1
    return out


blocks = strings()

targets = []
for x in open('_work/review_fixes/tutorial_en_left.txt',
              encoding='latin1').read().split('\n')[1:]:
    x = x.strip()
    if x and x[0].isdigit():
        v = int(x.split(';')[0])
        if v < 80000:
            targets.append(v)
tset = set(targets)

with open('_work/review_fixes/tutorial_context.txt', 'w',
          encoding='latin1', newline='\n') as f:
    for k, (off, part) in enumerate(blocks):
        lo, hi = max(0, k - 3), min(len(blocks), k + 4)
        # only dump context around target blocks
        near = any(blocks[j][0] in tset for j in range(lo, hi)) if False else None
        if off not in tset:
            continue
        f.write('### off=%d EN=%r\n' % (off, part.decode('latin1')))
        for j in range(max(0, k - 3), min(len(blocks), k + 4)):
            o, p = blocks[j]
            mark = ' <<<' if o == off else ''
            f.write('   %6d %r%s\n' % (o, p.decode('latin1')[:80], mark))
print('targets:', len(targets))
